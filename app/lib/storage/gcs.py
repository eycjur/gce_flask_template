import os
import io

from google.cloud import storage as gcs
from lib import utils


project_id = os.environ.get("PROJECT_ID")
bucket_name = os.environ.get("BUCKET_NAME")

client = gcs.Client(project_id)
bucket = client.get_bucket(bucket_name)


def read(path):
	if not bucket.get_blob(path):
		raise FileNotFoundError(f"{path} not found")
	blob = bucket.get_blob(path)
	return blob.download_as_string()

def read_all(dir_name):
	blobs = bucket.list_blobs(prefix=f"{dir_name}/", delimiter="/")
	blobs = list(blobs)
	files = [blob.download_as_string() for blob in blobs]
	file_names = [blob.name for blob in blobs]
	return file_names, files

def create(file, path, content_type="text/plain"):
	if bucket.get_blob(path):
		raise FileExistsError(f"{path} already exists")
	blob = bucket.blob(path)
	blob.upload_from_string(file, content_type=content_type)

def delete(path):
	blob = bucket.get_blob(path)
	if blob:
		blob.delete()
	else:
		raise FileNotFoundError(f"{path} not found")
