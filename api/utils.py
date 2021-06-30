from flask import jsonify
import csv
import numpy as np
import os
from werkzeug.utils import secure_filename
from settings import ALLOWED_EXTENSIONS


def result_in_json(sorted_alternatives, sorted_scores):
    """ create list of json objects for alternatives, scores and rankings """
    result = []
    for i in range(len(sorted_alternatives)):
        result.append({"Alternative": sorted_alternatives[i], "Score": sorted_scores[i], "Ranking": i + 1})
    return jsonify(result)


def delete_file(file_path):
    """ delete csv file after usage """
    os.remove(file_path)
    return


def allowed_file(filename):
    """ allowed formats to be uploaded for mcdss """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, path):
    """ check file type and return path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(path, filename))
        return os.path.join(path, filename)
    else:
        return ""


def upload_csv_files(files, upload_folder):
    """ get content of the uploaded files """
    if 'Decision Matrix' not in files or ('Criteria Details' not in files):
        raise Exception("Both the Decision Matrix file and the Criteria Details file are required")
    decision_matrix_file = files['Decision Matrix']
    criteria_details_file = files['Criteria Details']
    # check for uploaded files
    if decision_matrix_file.filename == '' or criteria_details_file.filename == '':
        raise Exception("Select files for upload")
    # check file type of decision matrix file and save file
    decision_matrix_file_path = save_file(decision_matrix_file, upload_folder)
    if decision_matrix_file_path == '':
        raise Exception("Allowed file type is csv")
    # check file type of criteria details file and save file
    criteria_details_file_path = save_file(criteria_details_file, upload_folder)
    if criteria_details_file_path == '':
        raise Exception("Allowed file type is csv")
    with open(decision_matrix_file_path, 'r', encoding='utf-8-sig') as csvfile:
        decision_matrix = list(csv.reader(csvfile, delimiter=';'))
    decision_matrix = np.array(decision_matrix)
    with open(criteria_details_file_path, 'r', encoding='utf-8-sig') as csvfile:
        criteria_details = list(csv.reader(csvfile, delimiter=';'))
    criteria_details = np.array(criteria_details)
    # delete uploaded csv files
    delete_file(decision_matrix_file_path)
    delete_file(criteria_details_file_path)
    return decision_matrix, criteria_details
