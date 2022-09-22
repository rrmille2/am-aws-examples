# DCF Connect Prototype
# Lambda Function: cpi_list_new_cases
# Ashley Miller <rrmille@amazon.com>
import boto3

def withHyphens(sNum):
    rval = ''
    for i, c in enumerate(sNum):
        rval = rval + c + '-'
    rval = rval[:-1]
    return rval
    
# does this case number exist in the db?
def CheckCase(case_number, caller):
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('cpi_NewCases')
    response = table.scan()
    items = response['Items']
    
    # assume the case won't be found
    rval = -1
    for item in items:
        if item['CaseNumber'] == case_number:
            rval = -2
            if item['PhoneNumber'] == caller:
                rval = 0
            break
    
    return rval
    
def lambda_handler(event, context):
    
    print(event)
    
    caller = event['sessionAttributes']['CustomerNumber']
    spokenCaseNumber = event['currentIntent']['slots']['CaseNumber']

    chk = CheckCase(spokenCaseNumber, caller)
    SelCaseNumber = ''
    if chk == -1:
        answer = 'Case ' + withHyphens(spokenCaseNumber) + ' does not exist'
    elif chk == -2:
        answer = 'You are not the owner of case ' + withHyphens(spokenCaseNumber)
    elif chk == 0:
        answer = 'Okay'
        SelCaseNumber = spokenCaseNumber
    else:
        answer = 'Error ' + str(chk) + ' has occurred.'
    
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

