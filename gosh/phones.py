#!/usr/bin/python
import sys, json;

data = json.load(sys.stdin)
allItems =  data['Items']
for item in allItems:
  print item['PhoneNumber']['S']


