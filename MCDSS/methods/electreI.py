import csv
import numpy as np
import pandas as pd
import math
import logging
import sys
from flask import Flask, jsonify
from csv_loaders import read_criteria_details, read_decision_matrix
from helpers import normalize_weights, sort_alternatives, result_in_json, negate_columns, check_uploaded_files, delete_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

def calculate_agreement_matrix(decision_matrix, weights):
    """ calculaties the agreement matrix for electre """
    agreement_matrix = np.zeros((len(decision_matrix), len(decision_matrix)), float)
    np.fill_diagonal(agreement_matrix, 1.0)
    for i in range(len(decision_matrix)):
        for j in range(i+1, len(decision_matrix)):
            for k in range(len(decision_matrix[0])):
                if decision_matrix[i][k] > decision_matrix[j][k]:
                    agreement_matrix[i][j] += weights[k]
                elif decision_matrix[i][k] == decision_matrix[j][k]:
                    agreement_matrix[i][j] += weights[k]
                    agreement_matrix[j][i] += weights[k]
                else:
                    agreement_matrix[j][i] += weights[k]
    return agreement_matrix

def calculate_disagreement_matrix(decision_matrix, veto_thresholds):
    """ calculates the disagreement table for electre """
    disagreement_matrix = np.zeros((len(decision_matrix), len(decision_matrix)), int)
    for i in range(len(decision_matrix)):
        for j in range(len(decision_matrix)):
                for k in range(len(decision_matrix[0])):
                    if veto_thresholds[k] > 0 and (decision_matrix[j][k] - decision_matrix[i][k]) >= veto_thresholds[k]:
                        disagreement_matrix[i][j] = 1
    return disagreement_matrix

def calculate_dominance_table(agreement_matrix, disagreement_matrix, agreement_threshold):
    """ calculates the dominance table for electre """
    dominance_matrix = np.zeros((len(agreement_matrix), len(agreement_matrix)), int)
    for i in range(len(agreement_matrix)):
        for j in range(len(agreement_matrix)):
            if i != j and agreement_matrix[i][j] >= agreement_threshold and disagreement_matrix[i][j] == 0:
                dominance_matrix[i][j] = 1
    return dominance_matrix

def main(decision_matrix_file_path, criteria_specification_file_path):
    """ electre method implementation """
    # read file
    number_of_criteria, number_of_alternatives, alternatives, decision_matrix = read_decision_matrix(decision_matrix_file_path)
    agreement_threshold, weights, veto_thresholds, optimization_type = read_criteria_details('Electre I', criteria_specification_file_path)
    check_uploaded_files(number_of_criteria, optimization_type, veto_thresholds)
    # delete uploaded csv files
    delete_file(decision_matrix_file_path)
    delete_file(criteria_specification_file_path)
    # negate columns of decision matrix in case optimization type is 1 (minimize)
    decision_matrix = negate_columns(decision_matrix, optimization_type)
    # normalize weights
    normalized_weights = normalize_weights(weights)
    # create Agreement Table
    agreement_matrix = calculate_agreement_matrix(decision_matrix, normalized_weights)
    # create Disagreement Table
    disagreement_matrix = calculate_disagreement_matrix(decision_matrix, veto_thresholds)
    # create Dominance Table
    dominance_matrix = calculate_dominance_table(agreement_matrix, disagreement_matrix, agreement_threshold)
    return dominance_matrix, alternatives
