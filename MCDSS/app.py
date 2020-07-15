import os
import sys
import logging
from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
from methods import maut, prometheeII, topsis, electreI
from settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, API_PORT
from helpers import allowed_file, save_file, result_in_json
from csv_loaders import upload_csv_files

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/mcdss/maut", methods=['POST'])
def mcdss_maut():
    """ maut method """
    try:
        # get uploaded files
        decision_matrix_file_path, criteria_details_file_path = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call maut method
        sorted_utility_scores, sorted_alternatives = maut.main(decision_matrix_file_path, criteria_details_file_path)
        # create result as json object, each json object consists of the alternative name, score and ranking
        result = result_in_json(sorted_alternatives, sorted_utility_scores)
        return result, 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/mcdss/topsis", methods=['POST'])
def mcdss_topsis():
    """ topsis method """
    try:
        # get uploaded files
        decision_matrix_file_path, criteria_details_file_path = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call topsis method
        sorted_closeness, sorted_alternatives = topsis.main(decision_matrix_file_path, criteria_details_file_path)
        # create result as json object, each json object consists of the alternative name, score and ranking
        result = result_in_json(sorted_alternatives, sorted_closeness)
        return result, 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/mcdss/prometheeII", methods=['POST'])
def mcdss_prometheeII():
    """ promethee II method """
    try:
        # get uploaded files
        decision_matrix_file_path, criteria_details_file_path = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call topsis method
        sorted_net_flows, sorted_net_alternatives = prometheeII.main(decision_matrix_file_path, criteria_details_file_path)
        # create result as json object, each json object consists of the alternative name, score and ranking
        result = result_in_json(sorted_net_alternatives, sorted_net_flows)
        return result, 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/mcdss", methods=['POST'])
def mcdss():
    try:
        # get method
        method = request.form['method']
        # get uploaded files
        decision_matrix_file_path, criteria_details_file_path = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call respective method
        if method is not None:
            if method == "Maut":
                sorted_utility_scores, sorted_alternatives = maut.main(decision_matrix_file_path, criteria_details_file_path)
                result = result_in_json(sorted_alternatives, sorted_utility_scores)
                return result, 200
            elif method == "Topsis":
                sorted_closeness, sorted_alternatives = topsis.main(decision_matrix_file_path, criteria_details_file_path)
                result = result_in_json(sorted_alternatives, sorted_closeness)
                return result, 200
            elif method == "Promethee II":
                sorted_net_flows, sorted_net_alternatives = prometheeII.main(decision_matrix_file_path, criteria_details_file_path)
                result = result_in_json(sorted_net_alternatives, sorted_net_flows)
                return result, 200
            elif method == "Electre I":
                return electreI.main(decision_matrix_file_path, criteria_details_file_path)
            else:
                return "Method does not exist", 404
        else:
            return "Method not specified", 404
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

if __name__ == '__main__':
    log.info("Starting Qualichain MCDSS")
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=API_PORT, debug=True)
