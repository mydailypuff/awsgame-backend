

def lambda_handler(event, context):
    print(event)
    print(context)
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }