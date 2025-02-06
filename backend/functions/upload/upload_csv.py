import json
import boto3
import base64
import os
import uuid
import io

# Initialisation du client S3
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler_upload_file(event, context):
    try:
        # Décoder le fichier reçu en base64 (UTF-8)
        file_content = base64.b64decode(event['body']).decode('utf-8')

        generated_uuid = uuid.uuid4()
        # Nom du fichier (assuré via les headers)
        file_name = event['headers'].get('file-name', 'uploaded_file.csv')

        key = f"{generated_uuid}/{file_name}"
        # Upload du fichier CSV directement dans le bucket S3
        # TODO à tester
        s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=file_content)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"File {file_name} uploaded to {BUCKET_NAME} successfully!"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
