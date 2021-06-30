import os

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/opt/qualichain_mcdss/MCDSS/uploads')
ALLOWED_EXTENSIONS = set(['csv'])
API_PORT = os.environ.get('API_PORT', 7070)
