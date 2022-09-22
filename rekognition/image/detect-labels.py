#!/usr/bin/env python 
'''
  Author: amiller, aws
  Description: an example of using amazon rekognition image to extract labels from an image
'''
import json
import boto3

REGION='us-east-2'
BUCKET = 'am-buck2'
KEY = '20190508_183629.jpg'
PROFILE = 'rrmille-am-admin'

def detect_labels(session, region, bucket, key, max_labels=10, min_confidence=90):
    rekognition = session.client('rekognition', region)
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        MaxLabels = max_labels,
        MinConfidence = min_confidence,
    )
    return response['Labels']

session = boto3.Session(profile_name=PROFILE)
region = REGION

for label in detect_labels(session, region, BUCKET, KEY):
    print('{Name} - {Confidence}%'.format(**label))


