import json
import os
import logging
from http import HTTPStatus
from typing import Dict, Any
from datetime import datetime
from utils.response_handler import create_response
from utils.http_method import HttpMethod
from services.s3_service import S3Service
from services.dynamo_service import DynamoDBService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_service = S3Service(os.environ["STORAGE_BUCKET"])
dynamo_service = DynamoDBService(os.environ["ANALYSIS_TABLE"])


def get_upload_url() -> Dict[str, Any]:
    file_id = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if url := s3_service.generate_presigned_url(f"{file_id}.csv"):
        return create_response(HTTPStatus.OK, {"uploadUrl": url, "fileId": file_id})
    else:
        return create_response(
            HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Error generating upload URL"}
        )


def get_analyses() -> Dict[str, Any]:
    analyses = dynamo_service.list_analyses()
    return create_response(HTTPStatus.OK, {"analyses": analyses})


def get_analysis(file_id: str) -> Dict[str, Any]:
    if analysis := dynamo_service.get_analysis(file_id):
        return create_response(HTTPStatus.OK, {"analysis": analysis})
    else:
        return create_response(HTTPStatus.NOT_FOUND, {"error": "Analysis not found"})


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    logger.info("Received event: %s", json.dumps(event))

    http_method = event.get("httpMethod")
    path = event.get("path")

    try:
        if http_method == HttpMethod.POST and path == "/upload":
            return get_upload_url()
        elif http_method == HttpMethod.GET and path == "/analyses":
            return get_analyses()
        elif http_method == HttpMethod.GET and path.startswith("/analyses/"):
            return get_analysis(path.split("/")[-1])

        return create_response(HTTPStatus.NOT_FOUND, {"error": "Not found"})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return create_response(
            HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Internal server error"}
        )
