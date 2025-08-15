import os
import boto3
from datetime import datetime
from Helpers import custom_logger
from dotenv import load_dotenv


log = custom_logger.get_logger()
load_dotenv()


def upload_report_to_s3(bucket_name: str = "practice-automation") -> str:
    """
    Uploads the test report to S3 and returns the S3 object URL.
    Args:
        bucket_name: Name of the S3 bucket
    Returns:
        str: The S3 URL of the uploaded file
    """
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name='ap-south-1'
    )

    local_report_path = os.path.join(os.path.abspath(__file__ + "/../../../"), 'new_report.html')
    
    # Generate timestamp and S3 object name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    object_name = f"UIAutomationPelagoWebsite/reports/new_report_{timestamp}.html"
    
    try:
        # Upload the file
        s3.upload_file(local_report_path, bucket_name, object_name)
        # Generate and return the S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        log.info(f"Report uploaded successfully to: {s3_url}")
        return s3_url
    except Exception as e:
        error_msg = f"Error uploading file to S3: {str(e)}"
        log.error(error_msg)
        raise Exception(error_msg)
