# DCF Connect Prototype
# Lambda Function: cpi_send_address
# Ashley Miller <rrmille@amazon.com>
import boto3

def withHyphens(sNum):
    rval = ''
    for i, c in enumerate(sNum):
        rval = rval + c + '-'
    rval = rval[:-1]
    return rval
    
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
                answer = 'Summary for Case ' + withHyphens(SelCaseNumber) + '. '
                answer = answer + 'Mother: ' + case['Mother'] + ' age ' + case['MotherAge'] + '. '
                answer = answer + 'Father: ' + case['Father'] + ' age ' + case['FatherAge'] + '. '
                answer = answer + 'Child: ' + case['Child'] + ' age ' + case['ChildAge'] + '. '
                answer = answer + 'Case Notes: ' + case['CaseNotes'] + '. '
    
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

