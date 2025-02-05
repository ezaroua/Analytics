import json
import os
import boto3
import logging
from typing import Dict, Any
from datetime import datetime
from botocore.exceptions import ClientError

from datetime import timezone
from utils.response_handler import create_response
from utils.http_method import HttpMethod

# ! Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ANALYSIS_TABLE'])
bucket_name = os.environ['UPLOAD_BUCKET']

# ! Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def get_upload_url() -> Dict[str, Any]:
    """Generate a pre-signed URL for S3 upload"""
    try:
        file_id = f"upload_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"{file_id}.csv",
                'ContentType': 'text/csv'
            },
            ExpiresIn=3600
        )
        return create_response(200, {
            'uploadUrl': url,
            'fileId': file_id
        })
    except Exception as e:
        logger.error(f"Error generating upload URL: {str(e)}")
        return create_response(500, {'error': 'Error generating upload URL'})

def get_analyses() -> Dict[str, Any]:
    """List all analyses"""
    try:
        response = table.scan()
        return create_response(200, {
            'analyses': response.get('Items', [])
        })
    except Exception as e:
        logger.error(f"Error fetching analyses: {str(e)}")
        return create_response(500, {'error': 'Error fetching analyses'})

def get_analysis(file_id: str) -> Dict[str, Any]:
    """Get a specific analysis result"""
    try:
        response = table.query(
            KeyConditionExpression='fileId = :fileId',
            ExpressionAttributeValues={':fileId': file_id}
        )
        if response.get('Items'):
            return create_response(200, {
                'analysis': response['Items'][0]
            })
        return create_response(404, {'error': 'Analysis not found'})
    except Exception as e:
        logger.error(f"Error fetching analysis: {str(e)}")
        return create_response(500, {'error': 'Error fetching analysis'})

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main Lambda handler"""
    logger.info(f"Received event: {json.dumps(event)}")

    # http_method = event['httpMethod']
    # path = event['path']

    return create_response(200, {'message': 'Hello from the API!'})
    # Route requests to appropriate handlers
    # try:
    #     if http_method == HttpMethod.POST and path == '/upload':
    #         return get_upload_url()
    #     elif http_method == HttpMethod.GET and path == '/analyses':
    #         return get_analyses()
    #     elif http_method == HttpMethod.GET and path.startswith('/analyses/'):
    #         file_id = path.split('/')[-1]
    #         return get_analysis(file_id)
    #     else:
    #         return create_response(404, {'error': 'Not found'})
    # except Exception as e:
    #     logger.error(f"Error processing request: {str(e)}")
    #     return create_response(500, {'error': 'Internal server error'})
