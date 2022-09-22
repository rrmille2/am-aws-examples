import boto3
import os

##
# All this does is read in the service urls and populate the service table in Dynamo
# Should only need one run, or if we change the attributes in the service table
##

def main():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    service_table = dynamodb.Table('nc-zip-region-reference')
    
    with open('myexport.csv') as f:
        data = f.read()
        
    for line in data.split('\n'):
        try:
            zip_code, county, region = line.split(',')
            
            print(f"Inserting\n{zip_code},{county},{region}")
            service_table.put_item(\
                Item={
                    'zipcode':zip_code,
                    'county':county,
                    'region':region,
                }
            )
        except IndexError:
            pass

main()