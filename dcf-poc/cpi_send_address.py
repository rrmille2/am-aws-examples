# DCF Connect Prototype
# Lambda Function: cpi_send_address
# Ashley Miller <rrmille@amazon.com>
import boto3
import urllib

def withHyphens(sNum):
    rval = ''
    for i, c in enumerate(sNum):
        rval = rval + c + '-'
    rval = rval[:-1]
    return rval

def SendTextMessage(caller, message):
    sns = boto3.client('sns')
    sns.publish(PhoneNumber = caller, Message = message)
    
# does this case number exist in the db?
def GetCase(case_number):
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('cpi_NewCases')
    response = table.scan()
    items = response['Items']
    
    # assume the case won't be found
    rval = None
    for item in items:
        if item['CaseNumber'] == case_number:
            rval = item
            break

    return rval
    
def lambda_handler(event, context):
    
    print(event)
    caller = event['sessionAttributes']['CustomerNumber']
    
    try:
        SelCaseNumber = event['sessionAttributes']['SelCaseNumber']
    except:
        answer = 'No case has been selected.'
    else:
        if SelCaseNumber == '':
            answer = 'Please select a case number.'
        else:
            case = GetCase(SelCaseNumber)
            if case == None:
                answer = 'The selected case does not exist.'
            else:
                answer = 'A text message with the address for case ' + withHyphens(SelCaseNumber) + ' has been sent to your phone.'
                message = 'Address for Case ' + SelCaseNumber + ': '
                message = message + 'https://www.google.com/maps/dir/?api=1&destination='
                message = message + urllib.quote_plus(case['Address'])
                print(message)
                SendTextMessage(caller, message)
                
    results = {
        "sessionAttributes": {
        "SelCaseNumber": SelCaseNumber,
        "key2": "value2"
      },
      "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
            "contentType": "PlainText",
            "content": answer
        }
      }
    }
    
    return results

