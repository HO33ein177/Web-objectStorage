import json
import os
import sys
import threading
from typing import Optional
from boto3.s3.transfer import TransferConfig
import boto3
import logging
from botocore.exceptions import ClientError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def authenticate_bucket(request):
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

    try:
        bucket_name = 'vault141'
        bucket = s3_resource.Bucket(bucket_name)
        # Perform an operation to authenticate access to the bucket
        # Example: List objects in the bucket to check if authentication is successful
        bucket_objects = list(bucket.objects.limit(1))  # Attempt to list one object to check access
    except ClientError as exc:
        logging.error(exc)
        return JsonResponse({'error': 'Authentication failed', 'details': str(exc)}, status=403)
    except Exception as exc:
        logging.error(exc)
        return JsonResponse({'error': 'An unexpected error occurred', 'details': str(exc)}, status=500)
    else:
        return JsonResponse({'message': 'Authenticated successfully'}, status=200)

    return JsonResponse({'error': 'Unhandled case'}, status=500)


@csrf_exempt
def create_bucket(request):
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

    try:
        bucket_name = 'why'
        bucket = s3_resource.Bucket(bucket_name)
        bucket.create(ACL='public-read')  # ACL='private'|'public-read'
    except ClientError as exc:
        logging.error(exc)
        return JsonResponse({'error': 'Failed to create bucket', 'details': str(exc)}, status=500)
    except Exception as exc:
        logging.error(exc)
        return JsonResponse({'error': 'An unexpected error occurred', 'details': str(exc)}, status=500)
    else:
        return JsonResponse({'message': 'Bucket created successfully'}, status=200)

    return JsonResponse({'error': 'Unhandled case'}, status=500)


@csrf_exempt
def init_bucket(request):
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
            bucket_name = 'sample-bucket_name'
            bucket = s3_resource.Bucket(bucket_name)
            bucket.create(ACL='public-read')  # ACL='private'|'public-read'
        except ClientError as exc:
            logging.error(exc)


@csrf_exempt
def check_bucket_entity(request):
    logging.basicConfig(level=logging.INFO)

    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=' https://vault141.s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
            aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
        )
    except Exception as exc:
        logging.error(exc)
        return JsonResponse({'error': 'Failed to initialize S3 client', 'details': str(exc)}, status=500)

    try:
        response = s3_client.head_bucket(Bucket="vault1411")
    except ClientError as err:
        status = err.response["ResponseMetadata"]["HTTPStatusCode"]
        errcode = err.response["Error"]["Code"]

        if status == 404:
            logging.warning("Missing object, %s", errcode)
            return JsonResponse({'error': 'Bucket not found', 'code': errcode}, status=404)
        elif status == 403:
            logging.error("Access denied, %s", errcode)
            return JsonResponse({'error': 'Access denied', 'code': errcode}, status=403)
        else:
            logging.exception("Error in request, %s", errcode)
            return JsonResponse({'error': 'Error in request', 'code': errcode}, status=status)
    except Exception as exc:
        logging.error(exc)
        return JsonResponse({'error': 'An unexpected error occurred', 'details': str(exc)}, status=500)
    else:
        return JsonResponse({'message': 'Bucket exists'}, status=200)

    return JsonResponse({'error': 'Unhandled case'}, status=500)


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
            endpoint_url='https://vault141.s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
            aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
        )
    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket_name = 'vaultTest'
            bucket = s3_resource.Bucket(bucket_name)
            bucket.delete()
        except ClientError as exc:
            logging.error(exc)


def get_bucket_policy(request):
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
            bucket_name = 'sample_bucket'
            bucket_policy = s3_resource.BucketPolicy(bucket_name)
            bucket_policy.load()
            logging.info(bucket_policy.policy)
        except ClientError as e:
            logging.error(e)


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
        file_name = request.POST.get('file_name')
        filePath = request.POST.get('file_location')

        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        relativePath = os.path.join(upload_dir, file_name)
        filePath = os.path.abspath(relativePath)

        print(f"Received file: {file_name}, bucket_name: {bucket_name}, file_location: {filePath}")
        try:
            s3_resource = boto3.resource(
                's3',
                endpoint_url='https://141vault141.s3.ir-tbz-sh1.arvanstorage.ir',
                aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
                aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
            )

        except Exception as exc:
            logging.error(exc)
        else:
            try:
                bucket = s3_resource.Bucket(bucket_name)
                file_path = filePath
                object_name = file_name

                with open(file_path, "rb") as file:
                    bucket.put_object(
                        ACL='private',
                        Body=file,
                        Key=object_name
                    )
                    return JsonResponse({'success': True})
            except ClientError as e:
                logging.error(e)


def object_multipart_upload_in_bucket(request):
    # Constant variables
    KB = 1024
    MB = KB * KB
    GB = MB * KB

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # S3 client instance
    s3_client = boto3.client(
        's3',
        endpoint_url='endpoint_url',
        aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
        aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
    )

    class ProgressPercentage:
        def __init__(self, file_path: str):
            self._file_path = file_path
            self._size = float(os.path.getsize(file_path))
            self._seen_so_far = 0
            self._lock = threading.Lock()

        def __call__(self, bytes_amount):
            """
            To simplify, assume this is hooked up to a single file_path

            :param bytes_amount: uploaded bytes
            """
            with self._lock:
                self._seen_so_far += bytes_amount
                percentage = (self._seen_so_far / self._size) * 100
                sys.stdout.write(
                    "\r%s  %s / %s  (%.2f%%)" % (self._file_path, self._seen_so_far, self._size, percentage)
                )
                sys.stdout.flush()

    # def upload_file(file_path: str, bucket: str, object_name: Optional[str] = None):
    #     """
    #     Upload a file to an S3 bucket
    #
    #     :param file_path: File to upload
    #     :param bucket: Bucket to upload to
    #     :param object_name: S3 object name. If not specified then file_path is used
    #     :return: True if file was uploaded, else False
    #     """
    #     # If S3 object_name was not specified, use file_path
    #     if object_name is None:
    #         object_name = file_path
    #
    #     # Upload the file
    #     try:
    #         # Set the desired multipart threshold value (400 MB)
    #         config = TransferConfig(multipart_threshold=400 * MB, max_concurrency=5)
    #         s3_client.upload_file(
    #             file_path,
    #             bucket,
    #             object_name,
    #             ExtraArgs={'ACL': 'public-read'},
    #             Callback=ProgressPercentage(file_path),
    #             Config=config
    #         )
    #     except ClientError as e:
    #         logging.error(e)
    #         return False
    #
    #     return True
    #
    # # file
    # object_name = 'file.png'
    # file_rel_path: str = os.path.join('files', object_name)
    # file_abs_path: str = os.path.join(base_directory, file_rel_path)
    #
    # upload_file(file_abs_path, 'sample_bucket', object_name)


@csrf_exempt
def object_download_in_bucket(request):
    if request.method == 'POST':
        logging.basicConfig(level=logging.INFO)
        data = json.loads(request.body.decode('utf-8'))  # Ensure proper decoding of request body

        bucket_name = data.get('bucket_name')
        file_name = data.get('file_name')

        # print(f"Received file: {file_name}, bucket_name: {bucket_name}")

        try:
            s3_resource = boto3.resource(
                's3',
                endpoint_url='https://141vault141.s3.ir-tbz-sh1.arvanstorage.ir',
                aws_access_key_id='c75bdfdb-a936-412e-a356-ae1f7ad82aee',
                aws_secret_access_key='1c7d029f48b2f93a720272da0557732be8bcf108'
            )
        except Exception as exc:
            logging.error(exc)
        else:
            try:
                # bucket
                bucket = s3_resource.Bucket('PersonalVault')

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
    bucketName = data.get('bucket_name')
    fileName = data.get('file_name')

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
            # bucket
            bucket_name = bucketName
            object_name = fileName

            bucket = s3_resource.Bucket(bucket_name)
            object = bucket.Object(object_name)

            response = object.delete(
                VersionId='string',
            )
        except ClientError as e:
            logging.error(e)


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
