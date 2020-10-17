import json
import boto3
import datetime

session = boto3.Session(region_name = 'us-west-2')
s3 = session.resource("s3")
ddb = session.client("dynamodb")

def lambda_handler(event, context):
    ## full scan ddb
    #tests = ddb.scan(TableName='datalake-test-config')
    
    testid = event.get('test_id')
    if testid != None:
        item_old = ddb.get_item(
            TableName='datalake-test-config',
            Key = {'test_id' : {'S': testid},
            'active':{'N':'1'}})
        item_old['Item']['endedAt'] = {'S':str(datetime.datetime.now())}
        ddb.put_item(TableName='datalake-test-config', Item=item_old['Item'])
        item_new = ddb.get_item(
            TableName='datalake-test-config',
            Key = {'test_id' : {'S': str(int(testid)+1)},
            'active':{'N':'1'}})
        if item_new and item_new.get('Item'):
            item = item_new.get('Item')
        else:
            item = None
    else:
        ## pick the first item from the table
        first_item = ddb.get_item(
            TableName='datalake-test-config',
            Key = {'test_id' : {'S': '1'},
            'active':{'N':'1'}})
        item = first_item.get('Item')


    if None == item:
        return { 'job': 'null', 'test_id': testid}
    else:
        item['startedAt'] = {'S':str(datetime.datetime.now())}
        testid = item.get('test_id').get('S')
        
        ddb.put_item(TableName='datalake-test-config', Item=item)
        return { 'job' : item.get('job').get('S'),
            'TaskExecution': item.get('job_arn').get('S').split("/")[-1],
            'TaskValidation': item.get('validation_lambda_arn').get('S').split(":")[-1],
            'test_id': testid
        }
