import json
import uscis_form as uscis

def lambda_handler(event, context):

    """
    Routes to appropriate form filler based on event type
    """

    # Add detailed logging to see the event structure
    print(f"Event: {json.dumps(event)}")

    resource_path = event.get('resourceContext', {}).get('resourcePath', '')
    path = event.get('path', '')
    raw_path = event.get('rawPath', '')

    print(f"Resource Path: {resource_path}, Path: {path}, Raw Path: {raw_path}")

    if path == '/uscis-form':
        return uscis.fill_form(event, context)
    
    else:
        print(f"Unknown path. Resource Path: {resource_path}, Path: {path}, Raw Path: {raw_path}")
        return {
            'statusCode': 404,
            'headers': get_cors_headers(),
            'body': json.dumps({'message': 'Not Found'})
        }

def get_cors_headers():
    """
    Returns CORS headers
    """
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }