import json

"""
event = {
    "Records": [
        {
            "eventID": "1",
            "eventName": "INSERT",
            "eventVersion": "1.0",
            "eventSource": "aws:dynamodb",
            "awsRegion": "us-east-1",
            "dynamodb":{
                "NewImage": {
                    "playerId:" {
                        "S": "90a0fce1"
                    },
                    "date": {
                        "S": "Aug 13 2022 20:50:39"
                    },
                    "gameRoundId": {
                        "N": "1245678"
                    },
                    "score": {
                        "N","150"
                    }
                },
                "SequenceNumber": "111",
                "SizeBytes":26,
                "StreamViewType": "NEW_AND_OLD_IMAGES"
            },
            "eventSourceARN":"GameEventsARN"
        },
    ]
    
}

"""

def lambda_handler(event, context):

    try:
        # iterate over each record in events
        for record in event['Records']:
            if record['eventName'] == 'INSERT':
                handle_insert(record)
            elif record['eventName'] == 'MODIFY':
                handle_modify(record)
            elif record['eventName'] == 'REMOVE':
                handle_remove(record)

        print('---------------------') 
    
    except Exception as e:
        print(3)
        return "Oh, shit!"

def handle_insert(record):
    print('Handling INSERT event')

    newImage = record['dynamodb']['NewImage']
    newPlayerId = newImage['playerId']['S']

    print('New row added with playerId=' + newPlayerId)
    print('Done processing INSERT event')


def handle_modify(record):
    print('Handling MODIFY event')

    oldImage = record['dynamodb']['OldImage']
    oldScore = oldImage['score']['S']

    newImage = record['dynamodb']['NewImage']
    newScore = newImage['score']['S']

    if oldScore != newScore:
        print(f"Scores changed--> old score{oldScore} and new score{newScore}")


def handle_remove(record):
    print('Handling DELETE event')

    oldImage = record['dynamodb']['OldImage']
    oldPlayerId = oldImage['playerId']['S']

    print('Row removed with playerId=' + oldPlayerId)
    print('Done processing DELETE event')
