import boto3
from botocore.exceptions import ClientError
import re
import os

s3 = boto3.resource("s3")
client = boto3.client("s3")
cfn_client = boto3.client("cloudformation")

APP_NAME = os.getenv("APP_NAME")
BUCKETS = os.getenv("BUCKETS")


def handler():
    print("Start s3 Cleaner")
    delete_useless_pr_buckets()
    print("End s3 Cleaner")


def delete_useless_pr_buckets():
    response = client.list_buckets()
    buckets = response.get("Buckets")
    for bucket in buckets:
        bucket_name = bucket.get("Name")
        match_cfn_template = re.match(
            rf"^amplify-{APP_NAME}-(?=pr[a-z].*)(?!production).*$", bucket_name)
        if match_cfn_template:
            env = bucket_name.split("-")[3]
            deployment_id = bucket_name.split("-")[4]
            cfn_stack_name = f"amplify-{APP_NAME}-{env}-{deployment_id}"
            try:
                cfn_client.get_template(
                    StackName=cfn_stack_name,
                )
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "ValidationError":
                    error_message = e.response["Error"]["Message"]
                    match_cfn_does_not_exist = re.match(
                        f"Stack with id {cfn_stack_name} does not exist", error_message)
                    if match_cfn_does_not_exist:
                        print(
                            f"Cfn stack : {cfn_stack_name} does not exist and delete s3 : {bucket_name}")
                        # delete cfn template bucket
                        delete_bucket(bucket_name)
                        # delete additional buckets
                        for bucket in BUCKETS.split(","):
                            if bucket:
                                delete_bucket(f"{bucket}-{env}")


def delete_bucket(bucket_name):
    print(f"Delete bucket : {bucket_name}")
    try:
        delete_bucket = s3.Bucket(bucket_name)
        delete_bucket.objects.delete()
        delete_bucket.delete()
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            print(f"No such bucket : {bucket_name}")
        else:
            print(f"Unexpected error: {e}")
