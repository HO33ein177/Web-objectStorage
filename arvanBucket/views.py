import json
import os
import sys
import threading
from typing import Optional
from boto3.s3.transfer import TransferConfig
import boto3
import logging
from botocore.exceptions import ClientError
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from UIWebObjectStorage import settings


# from .models import File










# Get the list of buckets in your user account


@csrf_exempt
def check_bucket_list(request):
    logging.basicConfig(level=logging.INFO)

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='https://vault141.s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
            aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
        )
    except Exception as exc:
        logging.error(exc)
        return JsonResponse({'error': 'Failed to initialize S3 client', 'details': str(exc)}, status=500)

    bucket_list = []
    target_bucket_name = 'vault141'
    target_bucket_found = False

    try:
        for bucket in s3_resource.buckets.all():
            logging.info(f'bucket_name: {bucket.name}')
            bucket_list.append(bucket.name)
            if bucket.name == target_bucket_name:
                target_bucket_found = True
    except ClientError as exc:
        logging.error(exc)
        return JsonResponse({'error': 'Failed to list buckets', 'details': str(exc)}, status=500)
    except Exception as exc:
        logging.error(exc)
        return JsonResponse({'error': 'An unexpected error occurred', 'details': str(exc)}, status=500)

    if target_bucket_found:
        return JsonResponse({'buckets': bucket_list, 'message': f'Bucket {target_bucket_name} exists'}, status=200)
    else:
        return JsonResponse({'buckets': bucket_list, 'message': f'Bucket {target_bucket_name} does not exist'},
                            status=404)

    return JsonResponse({'error': 'Unhandled case'}, status=500)


@csrf_exempt
def delete_bucket(request):
    logging.basicConfig(level=logging.INFO)

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=settings.tehran_endpoint_url,
            aws_access_key_id=settings.access_key_id,
            aws_secret_access_key=settings.secret_access_key
        )
    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket_name = 'vault141'
            bucket = s3_resource.Bucket(bucket_name)
            bucket.delete()
        except ClientError as exc:
            logging.error(exc)




@csrf_exempt
def change_bucket_access_policy(request):
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='https://vault141.s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
            aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket_name = 'vault141'
            bucket_policy = s3_resource.BucketPolicy(bucket_name)

            policy = {
                'Version': '2012-10-17',
                'Statement': [{
                    'Sid': 'PolicyName',
                    'Effect': 'Allow',
                    'Principal': '*',
                    'Action': ['s3:GetObject'],
                    'Resource': f'arn:aws:s3:::{bucket_name}/user_*'
                }]
            }

            # Convert the policy from JSON dict to string
            policy = json.dumps(policy)
            bucket_policy.put(Policy=policy)
            logging.info(bucket_policy.policy)

        except ClientError as e:
            logging.error(e)


@csrf_exempt
def object_upload_in_bucket(request):
    if request.method == 'POST':
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        # data = json.loads(request.body.decode('utf-8'))  # Ensure proper decoding of request body
        bucket_name = request.POST.get('bucket_name')
        # file = request.POST.get('file')
        file_name = request.POST.get('file_name')
        filePath = request.POST.get('file_location')
        # fileSize = request.POST.get('file_size')
        # print(type(file))
        print(filePath)

        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        relativePath = os.path.join(upload_dir, file_name)
        filePath = os.path.abspath(relativePath)

        # print(f"Received file: {file_name}, bucket_name: {bucket_name}, file_location: {filePath}")
        try:
            s3_resource = boto3.resource(
                's3',
                endpoint_url=settings.tehran_endpoint_url,
                aws_access_key_id=settings.access_key_id,
                aws_secret_access_key=settings.secret_access_key
            )

        except Exception as exc:
            logging.error(exc)
        else:
            try:
                bucket = s3_resource.Bucket(bucket_name)
                file_path = filePath
                object_name = file_name

                with open(file_path, "rb") as file:
                    print(type(file))
                    bucket.put_object(
                        ACL='private',
                        Body=file,
                        Key=object_name
                    )
                    return JsonResponse({'success': True})
            except ClientError as e:
                logging.error(e)



@csrf_exempt
def object_download_in_bucket(request):
    if request.method == 'POST':
        logging.basicConfig(level=logging.INFO)
        data = json.loads(request.body.decode('utf-8'))  # Ensure proper decoding of request body

        file_name = data.get('file_name')

        # print(f"Received file: {file_name}, bucket_name: {bucket_name}")

        try:
            s3_resource = boto3.resource(
                's3',
                endpoint_url=settings.tehran_endpoint_url,
                aws_access_key_id = settings.access_key_id,
                aws_secret_access_key=settings.secret_access_key
            )
        except Exception as exc:
            logging.error(exc)
        else:
            try:
                # bucket
                bucket = s3_resource.Bucket('vault141')

                object_name = file_name
                base_dir = 'D:/Storage'
                download_path = os.path.join(base_dir, file_name)

                bucket.download_file(
                    object_name,
                    download_path
                )
            except ClientError as e:
                logging.error(e)


def get_object_list_from_bucket(request):
    import boto3
    import logging
    from botocore.exceptions import ClientError

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        # S3 resource
        s3_resource = boto3.resource(
            's3',
            endpoint_url='endpoint_url',
            aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
            aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket_name = 'bucket_name'
            bucket = s3_resource.Bucket(bucket_name)

            for obj in bucket.objects.all():
                logging.info(f"object_name: {obj.key}, last_modified: {obj.last_modified}")

        except ClientError as e:
            logging.error(e)


@csrf_exempt
def object_delete_in_bucket(request):
    import boto3
    import logging
    from botocore.exceptions import ClientError

    logging.basicConfig(level=logging.INFO)
    data = json.loads(request.body.decode('utf-8'))  # Ensure proper decoding of request body
    # bucketName = data.get('bucket_name')
    fileName = data.get('file_name')

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=settings.tehran_endpoint_url,
            aws_access_key_id=settings.access_key_id,
            aws_secret_access_key=settings.secret_access_key
        )
    except Exception as exc:
        logging.error(exc)
        return JsonResponse({'error': 'Failed to initialize S3 resource'}, status=500)

    try:
        # bucket
        bucket_name = settings.bucket_name
        object_name = fileName

        bucket = s3_resource.Bucket(bucket_name)
        objectName = bucket.Object(object_name)

        response = objectName.delete()
        return JsonResponse({'message': 'Object deleted successfully', 'response': response})
    except ClientError as e:
        logging.error(e)
        return JsonResponse({'error': 'Failed to delete object from bucket'}, status=500)
    except Exception as e:
        logging.error(e)
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


def delete_multiple_objects_in_bucket(request):
    import boto3
    import logging
    from botocore.exceptions import ClientError

    logging.basicConfig(level=logging.INFO)

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url='<ENDPOINT>',
            aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
            aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
        )
    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket = s3_resource.Bucket('<BUCKET_NAME>')
            response = bucket.delete_objects(
                Delete={
                    'Objects': [
                        {
                            'Key': 'string',
                            'VersionId': 'string'
                        },
                    ],
                    'Quiet': True | False
                },
                MFA='string',
                RequestPayer='requester',
                BypassGovernanceRetention=True | False,
                ExpectedBucketOwner='string'
            )
            logging.info(response)
        except ClientError as exc:
            logging.error(exc)


def get_access_level_to_bucket(request):
    import boto3
    import logging
    from botocore.exceptions import ClientError

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        # S3 resource
        s3_resource = boto3.resource(
            's3',
            endpoint_url='endpoint_url',
            aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
            aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket_name = 'sample_bucket_name'
            object_name = 'sample_object_name'

            bucket = s3_resource.Bucket(bucket_name)
            object_acl = bucket.Object(object_name).Acl()
            logging.info(object_acl.grants)
        except ClientError as e:
            logging.error(e)


def set_access_level_to_bucket(request):
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        # S3 resource
        s3_resource = boto3.resource(
            's3',
            endpoint_url='endpoint_url',
            aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
            aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket_name = 'sample_bucket_name'
            object_name = 'sample_object_name'

            bucket = s3_resource.Bucket(bucket_name)
            object_acl = bucket.Object(object_name).Acl()
            logging.info(f"Old Object's ACL: {object_acl.grants}")

            # update object's ACL
            object_acl.put(ACL='public-read')  # ACL='private'|'public-read'
            object_acl.reload()
            logging.info(f"New Object's ACL: {object_acl.grants}")

        except ClientError as e:
            logging.error(e)
