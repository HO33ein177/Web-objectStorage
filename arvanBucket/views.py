import json
import math
import os
import boto3
import logging
from botocore.exceptions import ClientError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from UIWebObjectStorage import settings
from .models import File
from arvanBucket import *

logger = logging.getLogger(__name__)

def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


file_type_choices = {
    'image': 'Image',
    'video': 'Video',
    'audio': 'Audio',
    'document': 'Document',
    'unknown': 'Unknown',
}
icon_paths = {
    'image': './static/icons/image.png',
    'video': 'C:/Users/Hosein/PycharmProjects/UIWebObjectStorage/arvanBucket/static/icons/video.png',
    'audio': 'C:/Users/Hosein/PycharmProjects/UIWebObjectStorage/arvanBucket/static/icons/audio.png',
    'document': 'C:/Users/Hosein/PycharmProjects/UIWebObjectStorage/arvanBucket/static/icons/document.png',
    'unknown': 'C:/Users/Hosein/PycharmProjects/UIWebObjectStorage/arvanBucket/static/icons/unknown.png',
}


def get_file_type(file_name):
    if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return 'image'
    elif file_name.endswith(('.mp4', '.avi', '.mov')):
        return 'video'
    elif file_name.endswith(('.mp3', '.wav', '.aac')):
        return 'audio'
    elif file_name.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt')):
        return 'document'
    else:
        return 'unknown'


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
            endpoint_url=settings.tehran_endpoint_url,
            aws_access_key_id=settings.access_key_id,
            aws_secret_access_key=settings.secret_access_key
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
        # bucket_name = request.POST.get('bucket_name')
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
                bucket = s3_resource.Bucket(settings.bucket_name)
                file_path = filePath
                object_name = file_name

                with open(file_path, "rb") as file:
                    print(type(file))
                    bucket.put_object(
                        ACL='private',
                        Body=file,
                        Key=object_name
                    )
                    get_object_list_from_bucket(request)
                    return JsonResponse({'success': True})
            except ClientError as e:
                logging.error(e)


@csrf_exempt
def object_download_in_bucket(request):
    if request.method == 'POST':
        logging.basicConfig(level=logging.INFO)
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            file_name = data.get('file_name')
        else:
            file_name = request.POST.get('file_name')

        print(file_name, type(file_name))
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
                # bucket
                bucket = s3_resource.Bucket('vault141')

                object_name = file_name
                base_dir = 'D:/Storage'
                download_path = os.path.join(base_dir, file_name)

                bucket.download_file(
                    object_name,
                    download_path
                )
                return JsonResponse({'success': "file downloaded"}, status=200)
            except ClientError as e:
                logging.error(e)
                return JsonResponse({'error': "file not found"}, status=404)


@csrf_exempt
# @login_required
def get_object_list_from_bucket(request):
    if request.method == 'POST':
        import boto3
        import logging
        from botocore.exceptions import ClientError

        # Configure logging
        logging.basicConfig(level=logging.INFO)

        try:
            # S3 resource
            s3_resource = boto3.resource(
                's3',
                endpoint_url=settings.tehran_endpoint_url,
                aws_access_key_id=settings.access_key_id,
                aws_secret_access_key=settings.secret_access_key
            )
        except Exception as exc:
            logging.error(f"Failed to initialize S3 resource: {exc}")
            return JsonResponse({'error': 'Failed to initialize S3 resource'}, status=500)

        try:
            bucket_name = settings.bucket_name
            bucket = s3_resource.Bucket(bucket_name)
            objects_list = []
            for obj in bucket.objects.all():
                objects_list.append({
                    'file_name': obj.key,
                    'size': format_size(obj.size),
                    'last_modified': obj.last_modified.isoformat()  # Ensure proper date formatting
                })

                file_type_key = get_file_type(obj.key)
                file_type = file_type_choices[file_type_key]
                icon_path = icon_paths[file_type_key]
                upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                relativePath = os.path.join(upload_dir, obj.key)
                filePath = os.path.abspath(relativePath)

                existing_file = File.objects.filter(name=obj.key)

                if not existing_file:
                    File.objects.create(
                        name=obj.key,
                        path=filePath,
                        size=format_size(obj.size),
                        icon=icon_path,
                        owner=get_object_or_404(User, pk=48),
                        last_modified=obj.last_modified.isoformat(),
                        file_type=file_type,
                    )

            return JsonResponse({'objects': objects_list})

        except ClientError as e:
            logging.error(f"ClientError: {e}")
            return JsonResponse({'error': 'Failed to list objects from bucket'}, status=500)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


@csrf_exempt
def object_delete_in_bucket(file_name):
    import boto3
    import logging
    from botocore.exceptions import ClientError

    logging.basicConfig(level=logging.INFO)
    # data = json.loads(request.body.decode('utf-8'))  # Ensure proper decoding of request body
    # bucketName = data.get('bucket_name')
    fileName = file_name

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


@csrf_exempt
def delete(request):
    import logging
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
                file_name = data.get('file_name')
            else:
                file_name = request.POST.get('file_name')

            print(file_name, type(file_name))
            if not file_name:
                return JsonResponse({'error': 'No file name provided'}, status=400)

            try:
                file = File.objects.get(name=file_name)
                object_id = file.id
                # Perform the deletion logic here
                object_delete_in_bucket(file_name)
                File.objects.filter(id=object_id).delete()
                return JsonResponse({"status": 'success', "message": "File successfully deleted"})
            except File.DoesNotExist:
                return JsonResponse({"status": 'error', "message": "File not found"}, status=400)
            except File.MultipleObjectsReturned:
                return JsonResponse({'status': 'error', 'message': 'Multiple files found with the same name'}, status=405)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
