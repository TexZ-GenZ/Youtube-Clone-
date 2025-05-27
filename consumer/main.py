import json
import boto3

from secret_keys import SecretKeys

secret_keys = SecretKeys()
sqs_client = boto3.client("sqs", region_name=secret_keys.REGION_NAME)


def poll_sqs():
    while True:
        response = sqs_client.receive_message(
            QueueUrl=secret_keys.AWS_SQS_RAW_VIDEO_PROCESSING,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )

        for messsage in response.get("Messages", []):
            message_body = json.loads(messsage.get("Body"))

            if (
                "Service" in message_body
                and "Event" in message_body
                and message_body.get("Event") == "s3:TestEvent"
            ):
                sqs_client.delete_message(
                    QueueUrl=secret_keys.AWS_SQS_RAW_VIDEO_PROCESSING,
                    ReceiptHandle=messsage["ReceiptHandle"],
                )
                continue
        
            if "Records" in message_body:
                for record in message_body["Records"]:
                    if "s3" in record and "bucket" in record["s3"]:
                        bucket_name = record["s3"]["bucket"]["name"]
                        object_key = record["s3"]["object"]["key"]
                        print(f"Processing S3 object: {bucket_name}/{object_key}")
                        # Here you would add your processing logic

                        #TODO: Spin up a docker container to process the video
                        
        print(response)


poll_sqs()
