from report_generator import ReportGenerator
import boto3
import base64
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Récupération du fichier CSV encodé en base64 depuis l'event
        file_content = base64.b64decode(event['body'])  # Supposons que le contenu encodé est dans 'body'
        
        # Crée un fichier temporaire pour stocker le CSV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv:
            temp_csv.write(file_content)
            temp_csv_path = temp_csv.name
        
        # Initialiser le ReportGenerator avec le fichier temporaire
        report_generator = ReportGenerator(temp_csv_path)
        json_report = report_generator.generate_report()
        
        print(json_report)
        
        return {
            "statusCode": 200,
            "body": json_report
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": str(e)
        }