# import json
# import os
# import boto3
# import pandas as pd
# import logging
# from typing import Dict, Any, List
# from datetime import datetime, timezone
# # from io import StringIO

# from utils.response_handler import create_response

# # Initialize AWS clients
# s3 = boto3.client('s3')
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(os.environ['ANALYSIS_TABLE'])

# # Configure logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# def analyze_csv(df: pd.DataFrame) -> Dict[str, Any]:
#     """
#     Analyze CSV data and detect anomalies
#     You can implement your analysis logic here
#     """
#     try:
#         return {
#             'statistics': {'price': {}, 'quantity': {}, 'rating': {}},
#             'anomalies': [],
#         }
#     except Exception as e:
#         logger.error(f"Error analyzing data: {str(e)}")
#         raise

# def save_analysis_result(file_id: str, analysis: Dict[str, Any]) -> None:
#     """Save analysis results to DynamoDB"""
#     try:
#         item = {
#             'fileId': file_id,
#             'timestamp': datetime.now(timezone.utc).isoformat(),
#             'results': analysis,
#             'status': 'COMPLETED',
#         }
#         table.put_item(Item=item)
#     except Exception as e:
#         logger.error(f"Error saving analysis results: {str(e)}")
#         raise

# def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
#     """Main Lambda handler for processing uploaded CSV files"""
#     logger.info(f"Received event: {json.dumps(event)}")

#     return create_response(200, {'message': 'Hello from CSV Analyzer!'})


#     # try:
#     #     # Get bucket and file information from the S3 event
#     #     bucket = event['Records'][0]['s3']['bucket']['name']
#     #     key = event['Records'][0]['s3']['object']['key']
#     #     file_id = os.path.splitext(os.path.basename(key))[0]

#     #     # Mark analysis as started in DynamoDB
#     #     table.put_item(
#     #         Item={
#     #             'fileId': file_id,
#     #             'timestamp': datetime.now(timezone.utc).isoformat(),
#     #             'status': 'PROCESSING',
#     #         }
#     #     )

#     #     # Read CSV file from S3
#     #     response = s3.get_object(Bucket=bucket, Key=key)
#     #     df = pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))

#     #     # Perform analysis
#     #     analysis_results = analyze_csv(df)

#     #     # Save results
#     #     save_analysis_result(file_id, analysis_results)

#     #     return {
#     #         'statusCode': 200,
#     #         'body': json.dumps({
#     #             'message': 'File processed successfully',
#     #             'fileId': file_id
#     #         })
#     #     }

#     # except Exception as e:
#     #     logger.error(f"Error processing file: {str(e)}")
#     #     # Save error status to DynamoDB if we have the file_id
#     #     if 'file_id' in locals():
#     #         table.put_item(
#     #             Item={
#     #                 'fileId': file_id,
#     #                 'timestamp': datetime.now(timezone.utc).isoformat(),
#     #                 'status': 'ERROR',
#     #                 'error': str(e),
#     #             }
#     #         )
#     #     return {
#     #         'statusCode': 500,
#     #         'body': json.dumps({
#     #             'error': 'Error processing file',
#     #             'details': str(e)
#     #         })
#     #     }

import json
from typing import Dict, Any

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main Lambda handler"""
    # logger.info(f"Received event: {json.dumps(event)}")

    print("Hello from the File!")
    # http_method = event['httpMethod']
    # path = event['path']

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Hello from the API!'})
    }
