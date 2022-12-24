from storages.backends.s3boto3 import S3Boto3Storage

class MediaS3Boto3Storage(S3Boto3Storage):
    file_overwrite = False

class StaticS3Boto3Storage(S3Boto3Storage):
    querystring_auth = False
