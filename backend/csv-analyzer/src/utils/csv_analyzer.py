import pandas as pd
from pydantic import BaseModel, Field, validator
from typing import Any, List
from enum import Enum
from models.file_processor_model import *


class CSVAnalyzer:
    def __init__(self):
        self.validation_ranges = {
            "Prix": (10, 500),
            "Quantite": (1, 50),
            "Note_Client": (1.0, 5.0),
        }

    def normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to handle both accented and non-accented versions"""
        df_copy = df.copy()

        column_mappings = {
            "ID": ["ID"],
            "Nom": ["Nom"],
            "Prix": ["Prix"],
            "Quantite": ["Quantite", "Quantité"],  # Handle both versions
            "Note_Client": ["Note_Client", "Note client"],  # Handle both versions
        }

        column_standardization = {}
        for standard_name, possible_names in column_mappings.items():
            for possible_name in possible_names:
                if possible_name in df_copy.columns:
                    column_standardization[possible_name] = standard_name

        # logger.info(f"Original columns: {df.columns.tolist()}")
        # logger.info(f"Column mapping: {column_standardization}")

        df_copy = df_copy.rename(columns=column_standardization)

        if missing_cols := set(column_mappings.keys()) - set(df_copy.columns):
            raise ValueError(f"Missing required columns: {missing_cols}")

        return df_copy

    def calculate_statistics(self, series: pd.Series) -> Statistics:
        return Statistics(
            mean=float(series.mean()),
            median=float(series.median()),
            std=float(series.std()),
        )

    def determine_severity(
        self, type: AnomalyType, value: float, expected_range: tuple[float, float]
    ) -> AnomalySeverity:
        if value < 0 or value > expected_range[1] * 2:
            return AnomalySeverity.HIGH
        elif value > expected_range[1]:
            return AnomalySeverity.MEDIUM
        return AnomalySeverity.LOW

    def get_anomaly_message(
        self, type: AnomalyType, value: float, expected_range: tuple[float, float]
    ) -> str:
        """Generate descriptive message for anomaly"""
        type_messages = {
            AnomalyType.PRICE: {
                "low": "Prix négatif",
                "high": f"Prix supérieur à {expected_range[1]}€",
            },
            AnomalyType.QUANTITY: {
                "low": "Quantité négative ou nulle",
                "high": f"Quantité excessivement haute (> {expected_range[1]} unités)",
            },
            AnomalyType.RATING: {
                "low": "Note client négative",
                "high": "Note client supérieure à 5",
            },
        }

        if value < expected_range[0]:
            return type_messages[type]["low"]
        else:
            return type_messages[type]["high"]

    def create_anomaly(
        self,
        product_id: int,
        type: AnomalyType,
        value: float,
        expected_range: tuple[float, float],
    ) -> Anomaly:
        severity = self.determine_severity(type, value, expected_range)
        return Anomaly(
            product_id=product_id,
            type=type,
            value=value,
            expected_range=expected_range,
            severity=severity,
            message=self.get_anomaly_message(type, value, expected_range),
        )

    def detect_anomalies(self, df: pd.DataFrame) -> List[Anomaly]:
        # Normalize column names first
        df = self.normalize_column_names(df)

        # Price anomalies
        price_mask = (df["Prix"] < 10) | (df["Prix"] > 500)
        anomalies = [
            self.create_anomaly(
                product_id=row["ID"],
                type=AnomalyType.PRICE,
                value=row["Prix"],
                expected_range=(10, 500),
            )
            for _, row in df[price_mask].iterrows()
        ]

        # Quantity anomalies
        quantity_mask = (df["Quantite"] <= 0) | (df["Quantite"] > 50)
        anomalies.extend(
            self.create_anomaly(
                product_id=row["ID"],
                type=AnomalyType.QUANTITY,
                value=row["Quantite"],
                expected_range=(1, 50),
            )
            for _, row in df[quantity_mask].iterrows()
        )

        # Rating anomalies
        rating_mask = (df["Note_Client"] < 1.0) | (df["Note_Client"] > 5.0)
        anomalies.extend(
            self.create_anomaly(
                product_id=row["ID"],
                type=AnomalyType.RATING,
                value=row["Note_Client"],
                expected_range=(1.0, 5.0),
            )
            for _, row in df[rating_mask].iterrows()
        )
        return anomalies

    def analyze(self, df: pd.DataFrame, file_key: Any) -> AnalysisResults:
        # Normalize column names first
        df = self.normalize_column_names(df)

        # First detect anomalies
        anomalies = self.detect_anomalies(df)

        # Create masks for valid data (excluding anomalies)
        price_anomaly_ids = [
            a.product_id for a in anomalies if a.type == AnomalyType.PRICE
        ]
        quantity_anomaly_ids = [
            a.product_id for a in anomalies if a.type == AnomalyType.QUANTITY
        ]
        rating_anomaly_ids = [
            a.product_id for a in anomalies if a.type == AnomalyType.RATING
        ]

        # Filter dataframe for each statistic calculation
        valid_prices_df = df[~df["ID"].isin(price_anomaly_ids)]
        valid_quantities_df = df[~df["ID"].isin(quantity_anomaly_ids)]
        valid_ratings_df = df[~df["ID"].isin(rating_anomaly_ids)]

        # Calculate statistics only on valid data
        stats = AnalysisStats(
            price_stats=self.calculate_statistics(valid_prices_df["Prix"]),
            quantity_stats=self.calculate_statistics(valid_quantities_df["Quantite"]),
            rating_stats=self.calculate_statistics(valid_ratings_df["Note_Client"]),
        )

        print("stats: ", stats)

        return AnalysisResults(
            file_id=file_key,
            status=AnalysisStatus.COMPLETED,
            statistics=stats,
            anomalies=anomalies,
            metadata={
                "filename": df.name if hasattr(df, "name") else "unknown",
                "processing_time": 0.0,
                "valid_records": {
                    "price": len(valid_prices_df),
                    "quantity": len(valid_quantities_df),
                    "rating": len(valid_ratings_df),
                },
            },
            total_rows=len(df),
            anomaly_count=len(anomalies),
        )
