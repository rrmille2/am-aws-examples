#!/usr/bin/python3

# the equivalent of:
# aws sagemaker list-notebook-instances

import csv
import boto3

client = boto3.client('sagemaker', region_name='us-east-1')

notebooks = []
while True:
    response = client.list_notebook_instances()
    for notebook in response['NotebookInstances']:
        notebooks.append(notebook)
    if 'NextToken' in response:
        NextToken = response['NextToken']
    else:
        break

print("Total Number of Notebook Instances ----->", len(notebooks))
for notebook in notebooks:
    print(notebook)
