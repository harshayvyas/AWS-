# Use the code snippet provided by Secrets Manager.
import boto3
from botocore.exceptions import ClientError
import pymysql
import json
def get_secret():
    # Provide the secret store name
    secret_name = "Testingdatabase"
    # The endpoint url are region specific
    endpoint_url = "https://secretsmanager.us-east-2.amazonaws.com"
    region_name = "us-east-2"

#Setup the client
    session = boto3.session.Session()
    client = session.client(
    service_name='secretsmanager',
    region_name=region_name,
    endpoint_url=endpoint_url
    )

#Use the client to retrieve the secret
    try:
        get_secret_value_response = client.get_secret_value(
        SecretId=secret_name)
        print(get_secret_value_response)
#Error handling to make it easier for your code to tolerate faults
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        else:
# Decrypted secret using the associated KMS CMK
# Depending on whether the secret was a string or binary, one of these fields will be populated
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                binary_secret_data = get_secret_value_response['SecretBinary']

# The below code is a sample to connect to RDS MYSQL using Secret Manager
# Notice the username password and connection url are extracted from Secret manager
# Nothing is hard coded

    username=get_secret_value_response['SecretString']
    # loading the secret string to json for easy retrieval
    dict = json.loads(username)
    user = dict['username']
    passw = dict['password']
    host=dict['host']
    db_name=dict['dbname']
    print(user,db_name,passw,host)
    try:
        conn = pymysql.connect(host, user=user,passwd=passw, db=db_name, connect_timeout=5)
        print('connected')
    except:
         print("ERROR: Unexpected error: Could not connect to MySql instance.")
    #   #  sys.exit()


if __name__=="__main__":
    get_secret()
    # print(l)