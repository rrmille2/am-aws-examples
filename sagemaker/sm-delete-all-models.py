#!/usr/bin/python3
# this python script will delete all your SageMaker Models

import json
import boto3

session = boto3.session.Session()
sm = session.client('sagemaker')

response = sm.list_models()
while True:

    num = len(response['Models'])
    print(f'deleting {num} models...')
    for mod in response['Models']:
        try:
            print(mod['ModelName'])
            delresp = sm.delete_model(
                ModelName = mod['ModelName']
            )
        except:
            pass

    if 'NextToken' in response:
        response = sm.list_models(NextToken = response['NextToken'])
    else:
        break
        

print('done')

