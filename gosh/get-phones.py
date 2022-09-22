#!/usr/bin/env python
import boto3

ddb = boto3.resource('dynamodb')
table = ddb.Table('SALaunchPhones')
response = table.scan()
items = response['Items']
for item in items:
  print (item['PhoneNumber'])




