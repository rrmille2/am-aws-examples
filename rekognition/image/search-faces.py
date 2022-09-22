#!/usr/bin/python
import boto3

BUCKET = "am-buck1"
KEY = "search.jpg"
COLLECTION = "am-collection-id"

def search_faces_by_image(bucket, key, collection_id, threshold=80, region="eu-west-1"):
  rekognition = boto3.client("rekognition", region)
  response = rekognition.search_faces_by_image(
    Image={
      "S3Object": {
        "Bucket": bucket,
        "Name": key,
      }
    },
    CollectionId=collection_id,
    FaceMatchThreshold=threshold,
  )
  return response['FaceMatches']

for record in search_faces_by_image(BUCKET, KEY, COLLECTION):
  face = record['Face']
  print "Matched Face ({}%)".format(record['Similarity'])
  print "  FaceId : {}".format(face['FaceId'])
  print "  ImageId : {}".format(face['ExternalImageId'])


"""
  Expected output:

  Matched Face (96.6647949219%)
    FaceId : dc090f86-48a4-5f09-905f-44e97fb1d455
    ImageId : test.jpg

"""
