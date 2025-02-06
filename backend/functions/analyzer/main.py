from report_generator import ReportGenerator
from s3_service import S3Service
import boto3
import base64
import os
import tempfile
from dotenv import load_dotenv

from .dynamo_service import DynamoDBService

def lambda_handler_parser(event, context):
    try:
        dynamo_service = DynamoDBService("csv-analyzer-AnalysisTable-17KBIMQ0RAT64")
        s3Service = S3Service("csv-analyzer-bucket")
        file_key = event['Records'][0]['s3']['object']['key'];
        file = s3Service.get_file(file_key)
        # Récupération du fichier CSV encodé en base64 depuis l'event
        file_content = base64.b64decode(file['Body'])  # Supposons que le contenu encodé est dans 'body'
        
        # Crée un fichier temporaire pour stocker le CSV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv:
            temp_csv.write(file_content)
            temp_csv_path = temp_csv.name
        
        # Initialiser le ReportGenerator avec le fichier temporaire
        report_generator = ReportGenerator(temp_csv_path)
        json_report = report_generator.generate_report(file_key)
        
        dynamo_service.save_analysis(file_id=file_key, analysis_data=json_report)
        
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