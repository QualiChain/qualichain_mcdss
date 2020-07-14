import csv
import numpy as np
import pandas as pd
import logging
import math
import sys
from read_csv import read_criteria_details, read_decision_matrix
from helpers import normalize_weights, sort_alternatives, result_in_json, negate_columns, check_uploaded_files, delete_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

def main(decision_matrix_file_path, criteria_specification_file_path):
    """ maut method implementation """
    # read file
    try:
        number_of_criteria, number_of_alternatives, alternatives, decision_matrix = read_decision_matrix(decision_matrix_file_path)
        weights, optimization_type = read_criteria_details('Maut', criteria_specification_file_path)
        check_uploaded_files(number_of_criteria, optimization_type)
    except Exception as ex:
        log.error(ex)
        return "Wrong configuration of the uploaded files", 400
    # delete uploaded csv files
    delete_file(decision_matrix_file_path)
    delete_file(criteria_specification_file_path)
    # negate columns of decision matrix in case optimization type is 1 (minimize)
    decision_matrix = negate_columns(decision_matrix, optimization_type)
    # normalize weights
    normalized_weights = normalize_weights(weights)
    # normalize decision_matrix
    normalized_decision_matrix = normalize_decision_matrix(decision_matrix, normalized_weights)
    # compute utility scores
    utility_scores = [0 for i in range(number_of_alternatives)]
    for i in range(number_of_alternatives):
        for j in range(number_of_criteria):
            utility_scores[i] += normalized_decision_matrix[i][j]
        utility_scores[i] = round(utility_scores[i], 4)
    # sort alternatives by score
    sorted_utility_scores, sorted_alternatives = sort_alternatives(utility_scores, alternatives, True)
    # create result as json object, each json object consists of the alternative name, score and ranking
    result = result_in_json(sorted_alternatives, sorted_utility_scores)
    return result, 200

def normalize_decision_matrix(decision_matrix, weights):
    """ normalizes the decision matrix using min - max """
    max_decision_matrix = np.max(decision_matrix, axis=0)
    min_decision_matrix = np.min(decision_matrix, axis=0)
    normalized_decision_matrix = [[0 for j in range(len(decision_matrix[0]))] for i in range(len(decision_matrix))]
    for i in range(len(decision_matrix)):
        for j in range(len(decision_matrix[0])):
            normalized_decision_matrix[i][j] = ((decision_matrix[i][j] - min_decision_matrix[j])*weights[j]*1.0
                                                / (max_decision_matrix[j] - min_decision_matrix[j]))
    return normalized_decision_matrix
