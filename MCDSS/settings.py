import os

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')
ALLOWED_EXTENSIONS = set(['csv'])
