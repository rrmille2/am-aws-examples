#!/usr/bin/python3
import sys
import boto3
import datetime

cloudtrail = boto3.client('cloudtrail')

def get_cloudtrail_events(minutes):

    start = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes)

    kwargs = {
        'StartTime': start,
        'MaxResults': 50,
        'LookupAttributes': [{
            'AttributeKey': 'EventName',
            'AttributeValue': 'StartNotebookInstance'
         }]
    }

    response = cloudtrail.lookup_events(**kwargs)
    events = response['Events']

    while 'NextToken' in response:
        try:
            response = cloudtrail.lookup_events(**kwargs)
            events.extend(response['Events'])
        except Exception as e:
            print(e)
            print('Unable to retrieve CloudTrail events')
            raise(e)

    return events

# how many minutes back to look at cloudtrail
minutes=300

print(f'getting events from previous {minutes} minutes')
events = get_cloudtrail_events(minutes)

for event in events:
    print(f'{event}\n')


