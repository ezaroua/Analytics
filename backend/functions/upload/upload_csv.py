import json
import boto3
import base64
import os
from dotenv import load_dotenv

load_dotenv()
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']  # Définir le bucket dans les variables d'environnement

def lambda_handler(event, context):
    try:
        # Récupérer le fichier depuis la requête
        file_content = base64.b64decode(event['body'])
        file_name = event['headers']['file-name']  # Assurez-vous que le frontend envoie le nom du fichier dans les headers

        # Upload du fichier dans le bucket S3
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_content)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File uploaded successfully!"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
