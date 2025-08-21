import boto3
# To add conditions for scanning table --> need below import
from boto3.dynamodb.conditions import Key, Attr
import sys

########################################################
# NOTE: Run this docker command on CMD window to 
# instantiate a local Dynamodb database (that is active
# as long as the docker container is running).
# !!! "docker run -p 8000:8000 amazon/dynamodb-local"
########################################################


def queryTable(table, keyName, keyValue):

    #### table.query works even when keyValue does not exist --> no Exception
    print("in queryTable function")
    #print(f"keyName:{keyName} keyValue:{keyValue}")

    response = table.query(
        KeyConditionExpression=Key(keyName).eq(keyValue)
    )
    items = response['Items']

    return items


def scanTable(table, attrName, attrValue):
    
    #### table.query works even when keyValue does not exist --> no Exception
    print("in queryTable function")
    print(f"keyName:{attrName} keyValue:{attrValue}")

    response = table.scan(
        FilterExpression=Attr(attrName).eq(attrValue)
    )
    items = response['Items']
    print(items)
    return items


def scanTable2(table, attrName, attrValue, attrName2, attrValue2):
    
    #### table.query works even when keyValue does not exist --> no Exception
    print("in scanyTable2 function")
    print(f"keyName:{attrName} keyValue:{attrValue}")
    print(f"keyName:{attrName2} keyValue:{attrValue2}")

    response = table.scan(
        #FilterExpression=Attr(attrName).begins_with(attrValue) & Attr(attrName2).contains(attrValue2)
        FilterExpression=Attr(attrName2).contains(attrValue2)
    )
    items = response['Items']
    print(items)
    return items


def batchInserts(table):

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'username': 'cbaranoski',
                'lastname': 'baranoski',
                'address': {
                    'road': '1 Jefferson Street',
                    'city': 'Los Angeles',
                    'state': 'CA',
                    'zipcode': 90001
                }
            }
        )
        batch.put_item(
            Item={
                'username': 'janedoering',
                'lastname': 'Doering',
                'address': {
                    'road': '2 Washington Avenue',
                    'city': 'Seattle',
                    'state': 'WA',
                    'zipcode': 98109
                }
            }
        )
        batch.put_item(
            Item={
                'username': 'bobsmith',
                'lastname':  'Smith',
                'address': {
                    'road': '3 Madison Lane',
                    'city': 'Louisville',
                    'state': 'KY',
                    'zipcode': 40213
                }
            }
        )
        batch.put_item(
            Item={
                'username': 'alicedoe',
                'lastname': 'Doe',
                'address': {
                    'road': '1 Jefferson Street',
                    'city': 'Los Angeles',
                    'state': 'CA',
                    'zipcode': 90001
                }
            }
        )    
        batch.put_item(
            Item={
                'username': 'RickyBobby',
                'lastname':  'Bobby',
                'address': {
                    'road': '3 Can`t Drive Slow Hwy',
                    'city': 'Have2DriveFast',
                    'state': 'KY',
                    'zipcode': 40213
                }
            }            
        )


def batchInserts2(table):

    with table.batch_writer() as batch:
        for i in range(50):
            batch.put_item(
                Item={
                    'username': 'user' + str(i),
                    'lastname': 'unknown' + str(i),
                    'address': {
                        'road': '1313 Mockingbird Lane',
                        'city': 'Mockingbird Heights',
                        'state': 'NY',
                        'zipcode': 66600
                    }
                }
            )

def batchInserts3(table):

    with table.batch_writer(overwrite_by_pkeys=['username', 'lastname']) as batch:
        batch.put_item(
            Item={
                'username': 'alicedoe',
                'lastname': 'Doe',
                'address': {
                    'road': '1 Jefferson Street',
                    'city': 'Los Angeles',
                    'state': 'CA',
                    'zipcode': 90001
                }
            }
        )    
        batch.put_item(
            Item={
                'username': 'bobsmith',
                'lastname':  'Smith',
                'address': {
                    'road': '3 Madison Lane',
                    'city': 'Louisville',
                    'state': 'KY',
                    'zipcode': 40213
                }
            }
        )
        # delete item
        batch.delete_item(
            Key={
                'username': 'bobsmith',
                'lastname':  'Smith',
            }
        )
        batch.put_item(
            Item={
                'username': 'RickyBobby',
                'lastname':  'Bobby',
                'address': {
                    'road': '3 Can`t Drive Slow Hwy',
                    'city': 'Have2DriveFast',
                    'state': 'KY',
                    'zipcode': 40213
                }
            }
        )


###################################
# Main Function
###################################
def main():

    print("Minnie Mouse wears army boots!")

    
    # Get Service Resource
    ddb = boto3.resource('dynamodb',
                          endpoint_url='http://localhost:8000',
                          region_name='dummy',
   
                          aws_access_key_id='dummy',
                          aws_secret_access_key='dummy')

    ###################################
    # Delete table if exists
    ###################################
    try:

        table = ddb.Table('Users')
        table.delete()
        table.wait_until_not_exists()
        print("table deleted!")

    except Exception as e:
        #ignore
        pass

    ###############################    
    # Create table
    ###############################
    table = ddb.create_table(TableName='Users',
                     AttributeDefinitions=[
                        {
                            'AttributeName': 'username',
                            'AttributeType': 'S'
                        },
                        {
                            'AttributeName': 'lastname',
                            'AttributeType': 'S'
                        }

                     ],
                     KeySchema=[
                        {
                            'AttributeName': 'username',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'lastname',
                            'KeyType': 'RANGE'
                        }


                     ],
                     ProvisionedThroughput={
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                     }
    )                      

    table.wait_until_exists()

    print("DynamoDB table created!")
    print(f"NOF rows in newly created table: {table.item_count}")

    print(f"table created on {table.creation_date_time}")

    batchInserts(table)
    #batchInserts2(table)
    #batchInserts3(table)

    input = {'username': 'pbaranoski', 'lastname': 'baranoski', 'title': "Programmer", "languages": "Python, COBOL" }
    table.put_item(Item=input)
    input = {'username': 'sgayam', 'lastname': 'gayam', 'title': 'Project Lead', "languages": "Informatica, COBOL" }
    table.put_item(Item=input)
    input = {'username': 'vkhanna', 'lastname': 'Khanna', 'title': 'Programmer', "languages": "Informatica, COBOL" }
    table.put_item(Item=input)
    input = {'username': 'jturner', 'lastname': 'turner', 'title': 'Programmer', "languages": "Informatica, COBOL" }
    table.put_item(Item=input)
    input = {'username': 'bozoClown', 'lastname': 'Bozo', 'title': 'DingDong', "languages": "Pig Latin" }
    table.put_item(Item=input)
    
    # get an updated Table object for table.
    table = ddb.Table('Users')

    print("Successfully put item(s)")
    print(f"Table has {table.item_count} items!" )

    #########################################
    # Get a specific item
    #########################################
    try:
        rec = table.get_item(
            Key={
                'username': 'pbaranoski',
                'lastname': 'baranoski'
            }
        )
        #print(rec)
        # Get just the info we are interested in
        item = rec['Item']
        print(f"Here is specific item from table: {item}")

    except Exception as e:
        #ignore update error
        print("Ignoring exception on get_item! Ha Ha! ")
        pass    

    #########################################
    # Update an item
    #########################################
    # If item does not exist --> it is added
    table.update_item(
        Key={
            'username': 'pbaranoski',
            'lastname': 'baranoski'
        },
        UpdateExpression='SET languages = :val1',
        ExpressionAttributeValues={
            ':val1': "Python, java, bourne shell, REXX, COBOL"
        }
    )

    #########################################
    # Delete an item
    #########################################
    # if item does not exist --> no error
    table.delete_item(
        Key={
            'username': 'bozoClown',
            'lastname': 'Bozo'
        }
    )

    #########################################
    # View all items in table
    #########################################
    print(f"Total NOF rows in table: {table.item_count}")
    print("View items in table-->")
    scanReponse = table.scan(TableName='Users')
    items = scanReponse['Items']
    for item in items:
        print(item)

    #########################################
    # Query table
    #########################################
    #qryItems = queryTable(table, 'username', 'pbaranoski')
    #print(f"\n\nHere is the results from queryTable: {qryItems}")

    """
    qryItems = scanTable(table, 'lastname', 'Bobby')
    print(f"\n\nHere is the results from scanTable: {qryItems}")

    qryItems = scanTable(table, 'address.city', 'Have2DriveFast')
    print(f"\n\nHere is the results from scanTable: {qryItems}")
    """

    qryItems = scanTable2(table, 'lastname', 'baranoski', 'languages', 'COBOL')
    print(f"\n\nHere is the results from scanTable: ")
    for item in qryItems:
        print(item)
        print(item['lastname'])
        #print(type(item))

#########################################
# program starts HERE
#########################################
main()

