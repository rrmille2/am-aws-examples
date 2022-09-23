#!/usr/bin/python3

# uses the equivalent of:
# aws sagemaker list-notebook-instances
# aws sagemaker stop-notebook-instance

import csv
import datetime
import boto3

maxNotebooks = {
'ml.m5.xlarge': 1,
'ml.t3.medium': 1,
'ml.t2.medium': 1,
'ml.t3.large': 1,
'ml.t3.xlarge': 1,
'ml.m5.4xlarge': 1
}

client = boto3.client('sagemaker', region_name='us-east-1')

notebooks = []
while True:
    response = client.list_notebook_instances(StatusEquals='InService')
    for notebook in response['NotebookInstances']:
        notebooks.append(notebook)
    if 'NextToken' in response:
        NextToken = response['NextToken']
    else:
        break

times = []
for notebook in notebooks:
    times.append(datetime.datetime.timestamp(notebook['LastModifiedTime']))

# sort the list of notebooks by each notebook's LastModifiedTime
notebooks = sorted(notebooks, key=lambda x: x['LastModifiedTime'])

# so the last notebook in the list is the one most recently modified
InstanceType = notebooks[-1]['InstanceType']
print(f'InstanceType of most recent notebook: {InstanceType}')

# count number of notebooks with this InstanceType
counter = maxNotebooks
counter = dict.fromkeys(counter, 0)

# now determine which notebooks to terminate
names = []
for notebook in notebooks:
    InstanceType = notebook['InstanceType']
    NotebookInstanceName = notebook['NotebookInstanceName']
    if InstanceType in counter.keys():
        counter[InstanceType] += 1
        if counter[InstanceType] > maxNotebooks[InstanceType]:
            names.append(NotebookInstanceName)
    else:
        # if the InstanceType is not in counter.keys(), then assume the maximum is zero
        names.append(NotebookInstanceName)

print('Maximum Notebook Instance Types:')
print(maxNotebooks)
print('Counted  Notebook Instance Types:')
print(counter)

if len(names):
    print('stopping notebook instances:', end='')
    for name in names:
        print(f' {name}', end='')
        client.stop_notebook_instance(NotebookInstanceName=name)
    print('\n')
else:
    print('no instances to stop')




