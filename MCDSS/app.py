import os
import sys
import logging
import numpy as np
from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
from methods import maut, prometheeII, topsis, electreI
from settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, API_PORT
from helpers import allowed_file, save_file, result_in_json
from input_loaders import upload_csv_files, read_json

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
        # get input
        data = request.get_json()
        decision_matrix_json = data[0]['Decision Matrix'][0]
        criteria_details_json = data[1]['Criteria Details'][0]
        # call maut method
        sorted_utility_scores, sorted_alternatives = maut.main(decision_matrix_json, criteria_details_json, False)
        # create result as json object, each json object consists of the alternative name, score and ranking
        result = result_in_json(sorted_alternatives, sorted_utility_scores)
        return result, 200
        return "OK"
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/mcdss/topsis", methods=['POST'])
def mcdss_topsis():
    """ topsis method """
    try:
        # get input
        data = request.get_json()
        decision_matrix_json = data[0]['Decision Matrix'][0]
        criteria_details_json = data[1]['Criteria Details'][0]
        # call topsis method
        sorted_closeness, sorted_alternatives = topsis.main(decision_matrix_json, criteria_details_json, False)
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
        # get input
        data = request.get_json()
        decision_matrix_json = data[0]['Decision Matrix'][0]
        criteria_details_json = data[1]['Criteria Details'][0]
        # call prometheeII method
        sorted_net_flows, sorted_net_alternatives = prometheeII.main(decision_matrix_json, criteria_details_json, False)
        # create result as json object, each json object consists of the alternative name, score and ranking
        result = result_in_json(sorted_net_alternatives, sorted_net_flows)
        return result, 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/mcdss/electreI", methods=['POST'])
def mcdss_electreI():
    """ electre I method """
    try:
        # get input
        data = request.get_json()
        decision_matrix_json = data[0]['Decision Matrix'][0]
        criteria_details_json = data[1]['Criteria Details'][0]
        # call electreI method
        dominance_matrix, alternatives = electreI.main(decision_matrix_json, criteria_details_json, False)
        # create result as json object, result consists of the dominance table and the alternatives
        result = []
        result.append({"Dominance Table": dominance_matrix.tolist(), "Alternatives": alternatives})
        return jsonify(result), 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/file/mcdss/maut", methods=['POST'])
def file_mcdss_maut():
    """ maut method """
    try:
        # get content of uploaded files
        decision_matrix, criteria_details = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call maut method
        sorted_utility_scores, sorted_alternatives = maut.main(decision_matrix, criteria_details)
        # create result as json object, each json object consists of the alternative name, score and ranking
        result = result_in_json(sorted_alternatives, sorted_utility_scores)
        return result, 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/file/mcdss/topsis", methods=['POST'])
def file_mcdss_topsis():
    """ topsis method """
    try:
        # get content of uploaded files
        decision_matrix, criteria_details = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call topsis method
        sorted_closeness, sorted_alternatives = topsis.main(decision_matrix, criteria_details)
        # create result as json object, each json object consists of the alternative name, score and ranking
        result = result_in_json(sorted_alternatives, sorted_closeness)
        return result, 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/file/mcdss/prometheeII", methods=['POST'])
def file_mcdss_prometheeII():
    """ promethee II method """
    try:
        # get content of uploaded files
        decision_matrix, criteria_details = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call prometheeII method
        sorted_net_flows, sorted_net_alternatives = prometheeII.main(decision_matrix, criteria_details)
        # create result as json object, each json object consists of the alternative name, score and ranking
        result = result_in_json(sorted_net_alternatives, sorted_net_flows)
        return result, 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/file/mcdss/electreI", methods=['POST'])
def file_mcdss_electreI():
    """ electre I method """
    try:
        # get content of uploaded files
        decision_matrix, criteria_details = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call electreI method
        dominance_matrix, alternatives = electreI.main(decision_matrix, criteria_details)
        # create result as json object, result consists of the dominance table and the alternatives
        result = []
        result.append({"Dominance Table": dominance_matrix.tolist(), "Alternatives": alternatives})
        return jsonify(result), 200
    except Exception as ex:
        log.error(ex)
        return str(ex).encode('utf-8'), 400

@app.route("/file/mcdss", methods=['POST'])
def mcdss():
    try:
        # get method
        method = request.form['method']
        # get content of uploaded files
        decision_matrix, criteria_details = upload_csv_files(request.files, app.config['UPLOAD_FOLDER'])
        # call respective method
        if method is not None:
            if method == "Maut":
                sorted_utility_scores, sorted_alternatives = maut.main(decision_matrix, criteria_details)
                # create result as json object, each json object consists of the alternative name, score and ranking
                result = result_in_json(sorted_alternatives, sorted_utility_scores)
                return result, 200
            elif method == "Topsis":
                sorted_closeness, sorted_alternatives = topsis.main(decision_matrix, criteria_details)
                # create result as json object, each json object consists of the alternative name, score and ranking
                result = result_in_json(sorted_alternatives, sorted_closeness)
                return result, 200
            elif method == "Promethee II":
                sorted_net_flows, sorted_net_alternatives = prometheeII.main(decision_matrix, criteria_details)
                # create result as json object, each json object consists of the alternative name, score and ranking
                result = result_in_json(sorted_net_alternatives, sorted_net_flows)
                return result, 200
            elif method == "Electre I":
                dominance_matrix, alternatives = electreI.main(decision_matrix, criteria_details)
                # create result as json object, result consists of the dominance table and the alternatives
                result = []
                result.append({"Dominance Table": dominance_matrix.tolist(), "Alternatives": alternatives})
                return jsonify(result), 200
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
