import boto3
import logging
import datetime

maxNotebooks = {
'ml.m5.xlarge': 2,
'ml.t3.medium': 1,
'ml.t2.medium': 1,
'ml.t3.large': 1,
'ml.t3.xlarge': 1,
'ml.m5.4xlarge': 1
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
            raise(e)

    return events


def terminateNotebookInstances():

    client = boto3.client('sagemaker')
    
    # get a list of all SageMaker Notebooks that are running (aka, 'InService')
    notebooks = []
    while True:
        response = client.list_notebook_instances(StatusEquals='InService')
        for notebook in response['NotebookInstances']:
            notebooks.append(notebook)
        if 'NextToken' in response:
            NextToken = response['NextToken']
        else:
            break
    
    # sort the list of notebooks by LastModifiedTime
    notebooks = sorted(notebooks, key=lambda x: x['LastModifiedTime'])
    
    # the last notebook in the list is the one most recently modified
    InstanceType = notebooks[-1]['InstanceType']
    
    # count number of notebooks with this InstanceType and if the count exceeds the specified maximum,
    # then put in a list to terminate
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
    
    if len(names):
        msg = 'stopping notebook instances:'
        for name in names:
            msg += f' {name}'
            client.stop_notebook_instance(NotebookInstanceName=name)
    else:
        msg = 'no instances to stop'
        
    logger.info(msg)
    
#===== event handlers for the specific event types

def handleEndpoint(detail):
    EndpointArn = detail['EndpointArn']
    EndpointStatus = detail['EndpointStatus']
    logger.info(f'handleEndpoint(): EndpointARN={EndpointArn}, EndpointStatus={EndpointStatus}')

def handleNotebook(detail):
    # only take action if a notebook is now running (aka, InService)
    if detail['NotebookInstanceStatus'] == 'InService':
        terminateNotebookInstances()

#===== main lambda handler 

def lambda_handler(event, context):
    #logger.info(f'event: {event}')
    detail_type = event['detail-type']
    detail = event['detail']
    
    if detail_type == "SageMaker Endpoint State Change":
        handleEndpoint(detail)
        
    elif detail_type == "SageMaker Notebook Instance State Change":
        handleNotebook(detail)
        
    else:
        logger.info(f'unrecognized event: {event}')
    

