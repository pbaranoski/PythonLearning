
evnt = {
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
