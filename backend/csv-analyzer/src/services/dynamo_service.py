import boto3
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from botocore.exceptions import ClientError
from datetime import timezone


class DynamoDBService:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)
        self.logger = logging.getLogger(__name__)

    def save_analysis(
        self, file_id: str, analysis_data: Dict[str, Any], status: str = "COMPLETED"
    ) -> bool:
        """Save analysis results to DynamoDB"""
        try:
            item = {
                "fileId": file_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": analysis_data,
                "status": status,
            }
            self.table.put_item(Item=item)
            return True
        except ClientError as e:
            self.logger.error(f"Error saving analysis to DynamoDB: {e}")
            return False

    def get_analysis(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get analysis results by file ID"""
        try:
            response = self.table.query(
                KeyConditionExpression="fileId = :fileId",
                ExpressionAttributeValues={":fileId": file_id},
                ScanIndexForward=False,  # Get most recent first
                Limit=1,
            )
            items = response.get("Items", [])
            return items[0] if items else None
        except ClientError as e:
            self.logger.error(f"Error getting analysis from DynamoDB: {e}")
            return None

    def list_analyses(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent analyses"""
        try:
            response = self.table.scan(Limit=limit)
            return response.get("Items", [])
        except ClientError as e:
            self.logger.error(f"Error listing analyses from DynamoDB: {e}")
            return []

    def update_status(self, file_id: str, status: str, error: str = None) -> bool:
        """Update analysis status"""
        try:
            update_expr = "SET #status = :status, #timestamp = :timestamp"
            expr_attr_names = {"#status": "status", "#timestamp": "timestamp"}
            expr_attr_values = {
                ":status": status,
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
