import boto3
from typing import List
from models import Document
import botocore

# Let's use Amazon S3
# s3 = boto3.resource('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)

# s3.Bucket('semantic-348').put_object(Key='test.jpg', Body='blah blah blah')
# print('done')


def check_if_key_exists_s3(key: str) -> bool:
    """
    https://stackoverflow.com/questions/33842944/check-if-a-key-exists-in-a-bucket-in-s3-using-boto3
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("semantic-348")

    try:
        s3.Object("semantic-348", key).load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            # Something else has gone wrong.
            raise e
    else:
        # The object does exist.
        return True


def upload_to_s3(docs: List[Document]) -> None:
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("semantic-348")
    responses = []
    # note that it will overwrite if the key already exists, but hey let's check
    for doc in docs:
        if check_if_key_exists_s3(doc.hash_contents):
            print(f"Skipping {doc.hash_contents} because it already exists")
        else:
            print(f"Uploading {doc.hash_contents} to S3...")
            response = bucket.put_object(Key=doc.hash_contents, Body=doc.contents)
            responses.append(response)
    print(responses)
    return responses


def get_from_s3(key: str) -> str:
    """
    https://stackoverflow.com/questions/31976273/open-s3-object-as-a-string-with-boto3
    """
    obj = boto3.resource("s3").Bucket("semantic-348").Object(key)
    response = obj.get()
    return response["Body"].read()  # .decode('utf-8')
