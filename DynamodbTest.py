import boto3

def main():
    print("Minnie Mouse wears army boots!")

    # Get Service Resource
    ddb = boto3.resource('dynamodb',
                          endpoint_url='http://localhost:8000',
                          region_name='dummy',
   
                          aws_access_key_id='dummy',
                          aws_secret_access_key='dummy')

    # Delete table if exists
    #table = ddb.Table('Transactions')
    #table.delete()
    #table.wait_until_not_exists()
    #print("table deleted!")
    
    # Create table
    ddb.create_table(TableName='Transactions',
                     AttributeDefinitions=[
                        {
                            'AttributeName': 'TransactionId',
                            'AttributeType': 'S'
                        }
                     ],
                     KeySchema=[
                        {
                            'AttributeName': 'TransactionId',
                            'KeyType': 'HASH'
                        }
                     ],
                     ProvisionedThroughput={
                            'ReadCapacityUnits': 10,
                            'WriteCapacityUnits': 10
                     }
    )                      

    print("DynamoDB table created!")

    table = ddb.Table('Transactions')


    input = {'TransactionId': '876', 'State:': 'Pending', 'Amount': 50 }
    table.put_item(Item=input)
    input = {'TransactionId': '878', 'State:': 'Done!', 'Amount': 88 }
    table.put_item(Item=input)
    input = {'TransactionId': '888', 'State:': 'Messy!', 'Amount': 365 }
    table.put_item(Item=input)

    print("Successfully put item(s)")

    print("View items in table-->")
    scanReponse = table.scan(TableName='Transactions')
    items = scanReponse['Items']
    for item in items:
        print(item)

main()

