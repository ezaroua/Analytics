import json
import logging
from http import HTTPStatus
from io import StringIO
import pandas as pd
from typing import Dict, Any

from utils.csv_analyzer import CSVAnalyzer
from services.s3_service import S3Service
from services.dynamo_service import DynamoDBService
from utils.response_handler import create_response
from models.file_processor_model import AnalysisResults, AnalysisStatus


# ! Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ! Initialize services
s3_service = S3Service("csv-analyzer-bucket")
dynamodb_service = DynamoDBService("csv-analyzer-AnalysisTable-1PSRX2YSFU8AB")
analyzer = CSVAnalyzer()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    # sourcery skip: extract-method
    """AWS Lambda function to process CSV files uploaded to S3."""
    logger.info("Received event: %s", json.dumps(event))

    try:
        # Extract S3 event details
        record = event["Records"][0]["s3"]
        bucket, key = record["bucket"]["name"], record["object"]["key"]

        logger.info(f"Processing file {key} from bucket {bucket}")

        # Read file content from S3
        file_content, encoding = s3_service.get_file_content(key)
        if not file_content:
            logger.error(f"File {key} not found in bucket {bucket}")
            return create_response(
                HTTPStatus.NOT_FOUND, {"error": f"File {key} not found"}
            )

        # ! Parse CSV with encoding
        try:
            df = pd.read_csv(
                StringIO(file_content),
                encoding=encoding or "utf-8",
                on_bad_lines="warn",
            )
            # Print columns to verify correct reading
            logger.info(f"CSV columns: {df.columns.tolist()}")
            logger.info(f"CSV sample:\n{df.head()}")

        except Exception as e:
            logger.error(f"Error parsing CSV: {str(e)}")
            return create_response(
                HTTPStatus.BAD_REQUEST, {"error": f"Invalid CSV format: {str(e)}"}
            )

        # ! Analyze CSV data
        try:
            results = analyzer.analyze(df, key)
            # print("Results: ", results)
            # print("Results dict: ", results.dict())
        except Exception as e:
            logger.error(f"Error analyzing data: {str(e)}")
            return create_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": f"Analysis failed: {str(e)}"},
            )

        # ! Save to DynamoDB
        try:
            dynamodb_service.save_analysis(results, status=AnalysisStatus.COMPLETED)

        except Exception as e:
            logger.error(f"Error saving to DynamoDB: {str(e)}")
            return create_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": f"Failed to save results: {str(e)}"},
            )

        return create_response(
            HTTPStatus.OK,
            {
                "message": "Analysis completed successfully",
                "fileId": key,
                "results": results.dict(),
            },
        )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return create_response(
            HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Unexpected error: {str(e)}"}
        )
