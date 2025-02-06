import json
import os
import logging
from http import HTTPStatus
from typing import Dict, Any
from datetime import datetime
import uuid
from utils.response_handler import create_response
from utils.http_method import HttpMethod
from services.s3_service import S3Service
from services.dynamo_service import DynamoDBService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_service = S3Service("csv-analyzer-bucket")  # TODO: USE ENV VAR
dynamo_service = DynamoDBService("csv-analyzer-AnalysisTable-17KBIMQ0RAT64")


def get_upload_url(event: Dict[str, Any]) -> Dict[str, Any]:
    try:
        body = json.loads(event.get("body", "{}"))
        file_name = body.get("fileName")

        if not file_name:
            return create_response(
                HTTPStatus.BAD_REQUEST, {"error": "Missing fileName"}
            )

        # ! Generate unique ID
        generated_uuid = uuid.uuid4()

        # ! Create safe filename with unique prefix
        safe_file_name = os.path.basename(file_name)
        unique_key = f"{generated_uuid}/{safe_file_name}"

        if url := s3_service.generate_presigned_url(unique_key):
            return create_response(
                HTTPStatus.OK,
                {"uploadUrl": url, "fileId": unique_key, "fileName": safe_file_name},
            )

        return create_response(
            HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "URL generation failed"}
        )

    except json.JSONDecodeError:
        return create_response(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON"})


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

    print(f"HTTP Method: {http_method}")
    print(f"Path: {path}")
    print("http_method == HttpMethod.POST", http_method == HttpMethod.POST)
    print("path == /upload", path == "/upload")

    try:
        if http_method == HttpMethod.POST.value and path == "/upload":
            print("UPLOADING FILE")
            return get_upload_url(event)  # Pass event to extract fileName
        elif http_method == HttpMethod.GET.value and path == "/analyses":
            print("ANALYSES")
            return get_analyses()
        elif http_method == HttpMethod.GET.value and path.startswith("/analyses/"):
            print("ANALYSIS/ID")
            return get_analysis(path.split("/")[-1])

        return create_response(HTTPStatus.NOT_FOUND, {"error": "Not found"})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return create_response(
            HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Internal server error"}
        )
