import io
import sys
import csv
import numpy as np
from helpers import allowed_file, save_file, delete_file

def read_decision_matrix(data):
    """ read decision matrix """
    number_of_alternatives_index = np.argwhere(data == 'Number of alternatives')
    number_of_criteria_index = np.argwhere(data == 'Number of criteria')
    decision_matrix_index = np.argwhere(data == 'Alternatives / Criteria')
    decision_matrix_index[0][0] += 1
    decision_matrix_index[0][1] += 1
    number_of_alternatives = int(data[number_of_alternatives_index[0][0]][number_of_alternatives_index[0][1] + 1])
    number_of_criteria = int(data[number_of_criteria_index[0][0]][number_of_criteria_index[0][1] + 1])
    decision_matrix = [[0 for j in range(number_of_criteria)] for i in range(number_of_alternatives)]
    alternatives = ["" for i in range(number_of_alternatives)]
    for i in range(number_of_alternatives):
        alternatives[i] = data[i+decision_matrix_index[0][0]][0]
        for j in range(number_of_criteria):
                decision_matrix[i][j] = float(data[i + decision_matrix_index[0][0]][j + decision_matrix_index[0][1] ])
    return number_of_criteria, number_of_alternatives, alternatives, decision_matrix


def read_criteria_details(method, data):
    try:
        """ read criteria details """
        number_of_criteria_index = np.argwhere(data == 'Number of criteria')
        weights_index = np.argwhere(data == 'Weights')
        optimization_types_index = np.argwhere(data == 'Optimization Type')
        number_of_criteria = int(data[number_of_criteria_index[0][0]][number_of_criteria_index[0][1] + 1])
        weights = [0 for j in range(number_of_criteria)]
        optimization_type = [0 for j in range(number_of_criteria)]
        for j in range(number_of_criteria):
            weights[j] = float(data[weights_index[0][0]][j + weights_index[0][1] + 1])
            optimization_type[j] = int(data[optimization_types_index[0][0]][j + optimization_types_index[0][1] +1 ])

        if method == "Electre I":
            agreement_threshold_index = np.argwhere(data == 'Agreement Threshold')
            veto_thresholds_index = np.argwhere(data == 'Veto Thresholds')
            agreement_threshold = float(data[agreement_threshold_index[0][0]][agreement_threshold_index[0][1] + 1])
            veto_thresholds = [0 for j in range(number_of_criteria)]
            for j in range(number_of_criteria):
                veto_thresholds[j] = float(data[veto_thresholds_index[0][0]][j + veto_thresholds_index[0][1] + 1])
            return agreement_threshold, weights, veto_thresholds, optimization_type
        elif method == "Promethee II":
            preference_thresholds_index = np.argwhere(data == 'Preference Thresholds')
            indifference_threshold_index = np.argwhere(data == 'Indifference Thresholds')
            criteria_types_index = np.argwhere(data == 'Criteria Types')
            preference_thresholds = [0 for j in range(number_of_criteria)]
            indifference_thresholds = [0 for j in range(number_of_criteria)]
            criteria_types = ["" for j in range(number_of_criteria)]
            for j in range(number_of_criteria):
                preference_thresholds[j]= float(data[preference_thresholds_index[0][0]][j + preference_thresholds_index[0][1] + 1])
                indifference_thresholds[j]= float(data[indifference_threshold_index[0][0]][j + indifference_threshold_index[0][1] + 1])
                criteria_types[j] = data[criteria_types_index[0][0]][j + criteria_types_index[0][1] + 1]
            return weights, preference_thresholds, indifference_thresholds, optimization_type, criteria_types
        else:
            return weights, optimization_type
    except Exception as ex:
        raise Exception("Wrong configuration of the uploaded files")

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
