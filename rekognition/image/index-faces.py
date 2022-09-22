#!/usr/bin/python
import sys
import boto3

BUCKET = "am-buck1"
COLLECTION = "am-collection-id"


def index_faces(bucket, key, collection_id, image_id=None, attributes=(), region="us-east-1"):
  rekognition = boto3.client("rekognition", region)

  # Note: you have to create the collection first!
  #rekognition.create_collection(CollectionId=COLLECTION)

  response = rekognition.index_faces(
    Image={
      "S3Object": {
        "Bucket": bucket,
        "Name": key,
      }
    },
    CollectionId=collection_id,
    ExternalImageId=image_id,
      DetectionAttributes=attributes,
  )
  return response['FaceRecords']


def main(argv):

  key = argv[1]
  image_id = key

  for record in index_faces(BUCKET, key, COLLECTION, image_id):
    face = record['Face']
    # details = record['FaceDetail']
    print "Face ({}%)".format(face['Confidence'])
    print "  FaceId: {}".format(face['FaceId'])
    print "  ImageId: {}".format(face['ImageId'])


"""
  Expected output:

  Face (99.945602417%)
    FaceId: dc090f86-48a4-5f09-905f-44e97fb1d455
    ImageId: f974c8d3-7519-5796-a08d-b96e0f2fc242

"""

if __name__== "__main__":
  main(sys.argv)
