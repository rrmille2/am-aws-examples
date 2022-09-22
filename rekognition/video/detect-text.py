#!/usr/bin/env python3
'''
  Author: amiller, aws
  Description: an example of using amazon rekognition video to extract text from a video
'''

#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import json
import sys
import time

class VideoDetect:
    jobId = ''
    
    verbose = ''
    roleArn = ''
    bucket = ''
    video = ''

    rek = None
    sqs = None
    sns = None

    startJobId = ''

    sqsQueueUrl = ''
    snsTopicArn = ''
    processType = ''

    def __init__(self, role, bucket, video, profile, region, verbose):    
        self.roleArn = role
        self.bucket = bucket
        self.video = video
        self.verbose = verbose
        session = boto3.Session(profile_name=profile, region_name=region)
        self.rek = session.client('rekognition')
        self.sqs = session.client('sqs')
        self.sns = session.client('sns')

    def GetSQSMessageSuccess(self):

        jobFound = False
        succeeded = False
    
        dotLine=0
        while jobFound == False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.sqsQueueUrl, MessageAttributeNames=['ALL'], MaxNumberOfMessages=10) 

            if sqsResponse:
                if 'Messages' not in sqsResponse:
                    if self.verbose:
                        if dotLine<40:
                            print('.', end='')
                            dotLine=dotLine+1
                        else:
                            print()
                            dotLine=0    
                        sys.stdout.flush()
                    time.sleep(5)
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])

                    if self.verbose:
                        print(rekMessage['JobId'])
                        print(rekMessage['Status'])

                    if rekMessage['JobId'] == self.startJobId:
                        if self.verbose:
                            print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        if (rekMessage['Status']=='SUCCEEDED'):
                            succeeded=True

                        self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                       ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" + str(rekMessage['JobId']) + ' : ' + self.startJobId)
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                   ReceiptHandle=message['ReceiptHandle'])
        return succeeded

    def StartTextDetection(self):
        response=self.rek.start_text_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
            NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})

        self.startJobId=response['JobId']
        if self.verbose:
            print('Start Job Id: ' + self.startJobId)
  
    def GetTextDetectionResults(self):
        maxResults = 10
        paginationToken = ''
        finished = False

        # if not verbose, then print results in csv format
        if self.verbose == False:
            print('%s, %s' % ('detected-text', 'timestamp'))

        while finished == False:
            response = self.rek.get_text_detection(JobId=self.startJobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken)

            if self.verbose:
                print('Codec: ' + response['VideoMetadata']['Codec'])
                print('Duration: ' + str(response['VideoMetadata']['DurationMillis']))
                print('Format: ' + response['VideoMetadata']['Format'])
                print('Frame rate: ' + str(response['VideoMetadata']['FrameRate']))
                print()

            for textDetection in response['TextDetections']:
                text=textDetection['TextDetection']

                if self.verbose:
                    print("Timestamp: " + str(textDetection['Timestamp']))
                    print("   Text Detected: " + text['DetectedText'])
                    print("   Confidence: " +  str(text['Confidence']))
                    print ("      Bounding box")
                    print ("        Top: " + str(text['Geometry']['BoundingBox']['Top']))
                    print ("        Left: " + str(text['Geometry']['BoundingBox']['Left']))
                    print ("        Width: " +  str(text['Geometry']['BoundingBox']['Width']))
                    print ("        Height: " +  str(text['Geometry']['BoundingBox']['Height']))
                    print ("   Type: " + str(text['Type']) )
                    print()
                else:
                    # detected-text and timestamp (in seconds)
                    print('%s, %f' % (text['DetectedText'], textDetection['Timestamp']/1000.0))

                if 'NextToken' in response:
                    paginationToken = response['NextToken']
                else:
                    finished = True       
    
    def CreateTopicandQueue(self):
      
        millis = str(int(round(time.time() * 1000)))

        #Create SNS topic
        snsTopicName="AmazonRekognitionExample" + millis
        topicResponse=self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse['TopicArn']

        #create SQS queue
        sqsQueueName="AmazonRekognitionQueue" + millis
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)['QueueUrl']
 
        attribs = self.sqs.get_queue_attributes(QueueUrl=self.sqsQueueUrl,
                                                    AttributeNames=['QueueArn'])['Attributes']
                                        
        sqsQueueArn = attribs['QueueArn']

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(
            TopicArn=self.snsTopicArn,
            Protocol='sqs',
            Endpoint=sqsQueueArn)

        #Authorize SNS to write SQS queue 
        policy = """{{
  "Version":"2012-10-17",
  "Statement":[
    {{
      "Sid":"MyPolicy",
      "Effect":"Allow",
      "Principal" : {{"AWS" : "*"}},
      "Action":"SQS:SendMessage",
      "Resource": "{}",
      "Condition":{{
        "ArnEquals":{{
          "aws:SourceArn": "{}"
        }}
      }}
    }}
  ]
}}""".format(sqsQueueArn, self.snsTopicArn)
 
        response = self.sqs.set_queue_attributes(
            QueueUrl = self.sqsQueueUrl,
            Attributes = {
                'Policy' : policy
            })

    def DeleteTopicandQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)


def main():

    '''
    Note: Amazon Rekognition needs an IAM service role to give Rekognition access to your Amazon SNS topics.
    This example requires that the roleArn be created outside of this example code.
    '''

    # modify these variables to match your enviornment
    roleArn = 'arn:aws:iam::810190279255:role/amRekognitionServiceRole'
    bucket = 'am-buck2'
    video = 'video1.mp4'
    profile = 'rrmille-am-admin'
    region = 'us-east-2'
    verbose = False				# if verbose is false, then the results will be written in csv format

    analyzer=VideoDetect(roleArn, bucket, video, profile, region, verbose)
    analyzer.CreateTopicandQueue()

    analyzer.StartTextDetection()
    if analyzer.GetSQSMessageSuccess()==True:
        analyzer.GetTextDetectionResults()
    
    analyzer.DeleteTopicandQueue()


if __name__ == "__main__":
    main()
