import cfn_cleaner
import s3_cleaner


def lambda_handler(event, context):
    cfn_cleaner.handler()
    s3_cleaner.handler()
