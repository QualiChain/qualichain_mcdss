import os
import sys
import logging
from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
from methods import maut, prometheeII, topsis, electreI
from settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, API_PORT
from helpers import allowed_file, save_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/mcdss", methods=['POST'])
def mcdss():
    # read method and files
    method = request.form['method']
    if 'Decision Matrix' not in request.files or ('Criteria Details' not in request.files):
        return "Both the Decision Matrix file and the Criteria Details file are required", 400
    decision_matrix_file = request.files['Decision Matrix']
    criteria_details_file = request.files['Criteria Details']
    # check for uploaded files
    if decision_matrix_file.filename == '' or criteria_details_file.filename == '':
        return "Select files for upload", 400
    # check file type of decision matrix file and save file
    decision_matrix_file_path = save_file(decision_matrix_file, app.config['UPLOAD_FOLDER'])
    if decision_matrix_file_path == '':
        return "Allowed file type is csv", 400
    # check file type of criteria details file and save file
    criteria_details_file_path = save_file(criteria_details_file, app.config['UPLOAD_FOLDER'])
    if criteria_details_file_path == '':
        return "Allowed file type is csv", 400
    # call respective method
    if method is not None:
        if method == "Maut":
            return maut.main(decision_matrix_file_path, criteria_details_file_path)
        elif method == "Topsis":
            return topsis.main(decision_matrix_file_path, criteria_details_file_path)
        elif method == "Promethee II":
            return prometheeII.main(decision_matrix_file_path, criteria_details_file_path)
        elif method == "Electre I":
            return electreI.main(decision_matrix_file_path, criteria_details_file_path)
        else:
            return "Method does not exist", 404
    else:
        return "Method not specified", 404

if __name__ == '__main__':
    log.info("Starting Qualichain MCDSS")
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=API_PORT, debug=True)
