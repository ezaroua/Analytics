from report_generator.py import ReportGenerator


def lambda_handler(event, context):
    """AWS Lambda handler for CSV analysis."""
    report_generator = ReportGenerator("/home/cedric/Téléchargements/data_aberrant.csv")
    json_report = report_generator.generate_report()
    print(json_report)

