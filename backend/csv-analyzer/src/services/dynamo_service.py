from decimal import Decimal
from enum import Enum
import json
import boto3
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from botocore.exceptions import ClientError
from datetime import timezone


from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models.file_processor_model import AnalysisResults, AnalysisStatus


import gzip
import base64
from typing import Any


class DynamoDBItem(BaseModel):
    fileId: str
    status: AnalysisStatus
    compressed_data: str
    error: Optional[str] = None

    class Config:
        json_encoders = {Enum: lambda v: v.value}

    @classmethod
    def compress_data(cls, data: Any) -> str:
        """Compress data using gzip and encode as base64"""
        json_str = json.dumps(data)
        compressed = gzip.compress(json_str.encode("utf-8"))
        return base64.b64encode(compressed).decode("utf-8")

    @classmethod
    def decompress_data(cls, compressed_str: str) -> Any:
        """Decompress base64 encoded gzip data"""
        compressed = base64.b64decode(compressed_str)
        decompressed = gzip.decompress(compressed)
        return json.loads(decompressed.decode("utf-8"))

    @classmethod
    def from_analysis(cls, analysis_results: AnalysisResults, status: AnalysisStatus):
        analysis_dict = json.loads(json.dumps(analysis_results.dict()))
        return cls(
            fileId=analysis_results.file_id,
            status=status,
            compressed_data=cls.compress_data(analysis_dict),
        )


class DynamoDBResponse(BaseModel):
    items: List[DynamoDBItem]
    count: int


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        return float(obj) if isinstance(obj, Decimal) else super().default(obj)


class DynamoDBService:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)
        self.logger = logging.getLogger(__name__)

    def save_analysis(
        self,
        analysis_results: AnalysisResults,
        status: AnalysisStatus = AnalysisStatus.COMPLETED,
    ) -> bool:
        try:
            item = DynamoDBItem.from_analysis(analysis_results, status)
            item_dict = json.loads(json.dumps(item.dict()))
            dynamo_item = json.loads(
                json.dumps(item_dict, cls=DecimalEncoder), parse_float=Decimal
            )
            self.table.put_item(Item=dynamo_item)
            return True
        except Exception as e:
            self.logger.error(f"Error saving to DynamoDB: {str(e)}")
            return False

    def get_analysis(self, file_id: str) -> Optional[DynamoDBItem]:
        """Get analysis results by file ID"""
        try:
            response = self.table.query(
                KeyConditionExpression="fileId = :fileId",
                ExpressionAttributeValues={":fileId": file_id},
                ScanIndexForward=False,
                Limit=1,
            )

            if items := response.get("Items", []):
                # Convert Decimals back to floats
                item_str = json.dumps(items[0], cls=DecimalEncoder)
                converted_item = json.loads(item_str)

                # Create DynamoDBItem and decompress the data
                item = DynamoDBItem.parse_obj(converted_item)
                item.compressed_data = DynamoDBItem.decompress_data(
                    item.compressed_data
                )
                return item
            return None

        except ClientError as e:
            self.logger.error(f"Error getting analysis from DynamoDB: {e}")
            return None

    def list_analyses(self, limit: int = 50) -> DynamoDBResponse:
        """List recent analyses"""
        try:
            response = self.table.scan(Limit=limit)

            # Convert all items' Decimals to floats
            items_str = json.dumps(response.get("Items", []), cls=DecimalEncoder)
            converted_items = json.loads(items_str)

            # Create DynamoDBItems and decompress their data
            items = []
            for item_data in converted_items:
                item = DynamoDBItem.parse_obj(item_data)
                item.compressed_data = DynamoDBItem.decompress_data(
                    item.compressed_data
                )
                items.append(item)

            return DynamoDBResponse(items=items, count=len(items))
        except ClientError as e:
            self.logger.error(f"Error listing analyses from DynamoDB: {e}")
            return DynamoDBResponse(items=[], count=0)

    def update_status(
        self, file_id: str, status: AnalysisStatus, error: Optional[str] = None
    ) -> bool:
        """Update analysis status"""
        try:
            update_expr = "SET #status = :status, #timestamp = :timestamp"
            expr_attr_names = {"#status": "status", "#timestamp": "timestamp"}
            expr_attr_values = {
                ":status": status.value,
                ":timestamp": datetime.now(timezone.utc).isoformat(),
            }

            if error:
                update_expr += ", #error = :error"
                expr_attr_names["#error"] = "error"
                expr_attr_values[":error"] = error

            self.table.update_item(
                Key={"fileId": file_id},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
            )
            return True
        except ClientError as e:
            self.logger.error(f"Error updating status in DynamoDB: {e}")
            return False


# class DynamoDBItem(BaseModel):
#     fileId: str
#     timestamp: str
#     status: AnalysisStatus
#     data: dict
#     error: Optional[str] = None

#     @classmethod
#     def from_analysis(cls, analysis_results: AnalysisResults, status: AnalysisStatus):
#         """
#         Create DynamoDBItem from AnalysisResults
#         Note: AnalysisResults uses snake_case, but DynamoDB uses camelCase
#         """
#         return cls(
#             fileId=analysis_results.file_id,  # matching the snake_case from AnalysisResults
#             timestamp=datetime.now(timezone.utc).isoformat(),
#             status=status,
#             data={
#                 "fileId": analysis_results.file_id,
#                 "timestamp": analysis_results.timestamp.isoformat(),
#                 "status": analysis_results.status.value,
#                 "statistics": analysis_results.statistics.dict(),
#                 "anomalies": [anomaly.dict() for anomaly in analysis_results.anomalies],
#                 "metadata": analysis_results.metadata,
#                 "totalRows": analysis_results.total_rows,
#                 "anomalyCount": analysis_results.anomaly_count,
#             },
#         )
