import boto3
import zipfile
import io

bucket = 'am-drones'
zipfile = 'images/blue-boxes-images.zip'

print('reading zip file')
s3_resource = boto3.resource('s3')
zip_obj = s3_resource.Object(bucket_name=bucket, key=zipfile)
buffer = io.BytesIO(zip_obj.get()["Body"].read())

z = zipfile.ZipFile(buffer)
for filename in z.namelist():
    file_info = z.getinfo(filename)
    print(f'uploading {filename}')
    s3_resource.meta.client.upload_fileobj(
        z.open(filename),
        Bucket=bucket,
        Key=f'{filename}'
    )
