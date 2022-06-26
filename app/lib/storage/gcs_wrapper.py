import os
import io

from PIL import Image
from google.cloud import storage as gcs
from lib import utils

from lib.storage import gcs


def save_img(img_pil, path):
    img_bytes = io.BytesIO()
    img_pil.save(img_bytes, format="png")
    img_bytes = img_bytes.getvalue()

    gcs.create(img_bytes, path, content_type="image/png")

def read_imgs(dir_name):
    file_names, files = gcs.read_all(dir_name)
    imgs = [Image.open(io.BytesIO(file)) for file in files]
    return file_names, imgs
