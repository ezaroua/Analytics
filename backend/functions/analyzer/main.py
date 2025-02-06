import time

from report_generator import ReportGenerator


def lambda_handler(event, context):
    """AWS Lambda handler for CSV analysis."""
    try:
        report_generator = ReportGenerator("/home/cedric/Téléchargements/data_aberrant.csv")
        json_report = report_generator.generate_report()
        print(json_report)
    except Exception as e:
        print(e)
