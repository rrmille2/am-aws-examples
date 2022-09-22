#!/usr/bin/env python
import boto3

# get the phone numbers from dynamodb
def GetPhoneNumbers():
  ddb = boto3.resource('dynamodb')
  table = ddb.Table('SALaunchPhones')
  response = table.scan()
  items = response['Items']
  phones = []
  for item in items:
    phones.append(item['PhoneNumber'])
  return phones

def main():
  testFlag = 1

  # for testing
  if testFlag == 1:
    # fixed array of phone numbers for testing
    phones = ['8138423093', '2062950634', '8326475811', '2019166260', '4254457155', '3039192088']
    phones = ['8138423093']
  else:
    # get the phone numbers from dynamodb
    phones = GetPhoneNumbers() 

    # the lines below are for testing
    phones = ['8138423093']
    #phones = ['6469277461', '2062950634', '2199283973', '3144984485', '8326475811', '8138423093', '6786121391', '2158348813', '7789458135', '2067654203', '4254457155', '7039156159', '9148046926', '3039192088', '2019166260', '8325457253', '2532188643', '6136008510']

  # make the outbound call
  conn = boto3.client('connect')
  for phone in phones:
    phone = '+1' + phone
    print(phone)
    response = conn.start_outbound_voice_contact( \
      DestinationPhoneNumber=phone, \
      ContactFlowId='49f1fbd9-b8f0-4c89-b5d1-9556cda2b912', \
      InstanceId='5db54d7c-252a-4669-a948-9861273b8b9d', \
      SourcePhoneNumber='+18327810124')

if __name__ == "__main__":
    main()




