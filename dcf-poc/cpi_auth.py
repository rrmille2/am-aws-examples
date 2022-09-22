# DCF Connect Prototype
# Lambda Function: cpi_send_address
# Ashley Miller <rrmille@amazon.com>
import boto3

# get the phone numbers from dynamodb
def GetPhoneNumbers():
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('cpi_AuthorizedPhoneNumbers')
    response = table.scan()
    phones = response['Items']
    return phones
  
def lambda_handler(event, context):
    
    caller = event['Details']['ContactData']['CustomerEndpoint']['Address']

    # assume the phone won't be found
    AuthFlag = "False"
    FirstName = ''
    
    # get the phone numbers from dynamodb
    phones = GetPhoneNumbers() 

    for phone in phones:
        if phone['PhoneNumber'] == caller:
            AuthFlag = "True"
            FirstName = phone['FirstName']

    if AuthFlag:
        print(caller, FirstName)
    else:
        print(caller, 'Unverified')

    resultMap = {"AuthFlag":AuthFlag, "FirstName":FirstName}
    return resultMap;

