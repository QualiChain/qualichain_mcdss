import csv
import numpy as np
import pandas as pd
import math
import logging
import sys
from read_csv import read_criteria_details, read_decision_matrix
from helpers import normalize_weights, sort_alternatives, result_in_json, negate_columns, check_uploaded_files, delete_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

def main(decision_matrix_file_path, criteria_specification_file_path):
    """ promethee II method implementation """
    # read file
    try:
        number_of_criteria, number_of_alternatives, alternatives, decision_matrix = read_decision_matrix(decision_matrix_file_path)
        weights, preference_thresholds, indifference_thresholds, optimization_type, criteria_types = read_criteria_details('Promethee II', criteria_specification_file_path)
        check_uploaded_files(number_of_criteria, optimization_type, [], preference_thresholds, indifference_thresholds, criteria_types)
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
    # create preference matrix
    preference_matrix = calculate_preference_matrix(decision_matrix, criteria_types, preference_thresholds, indifference_thresholds, normalized_weights)
    # calculate dominance
    positive_flow, negative_flow, net_flow = calculate_flows(preference_matrix)
    #sort alternatives
    sorted_net_flows, sorted_net_alternatives = sort_alternatives(net_flow, alternatives, True)
    # create result as json object, each json object consists of the alternative name, score and ranking
    result = result_in_json(sorted_net_alternatives, sorted_net_flows)
    return result, 200

def calculate_preference_matrix(decision_matrix, criteria_types, preference_thresholds, indifference_thresholds, normalized_weights):
    """ calculates the preference matrix for promithee """
    preference_matrix = np.zeros((len(decision_matrix), len(decision_matrix)), float)
    for i in range(len(decision_matrix)):
        for j in range(len(decision_matrix)):
            if i != j:
                for k in range(len(decision_matrix[0])):
                    preference = 0
                    if criteria_types[k] == "usual":
                        preference = usual_criterion(decision_matrix[i][k] - decision_matrix[j][k])
                    elif criteria_types[k] == "quasi":
                        preference = quasi_criterion(indifference_thresholds[k], decision_matrix[i][k] - decision_matrix[j][k])
                    elif criteria_types[k] == "linear":
                        preference = linear_criterion(preference_thresholds[k], decision_matrix[i][k] - decision_matrix[j][k])
                    elif criteria_types[k] == "linear with indifference threshold":
                        preference = linear_indifference__criterion(indifference_thresholds[k], preference_thresholds[k], decision_matrix[i][k] - decision_matrix[j][k])
                    elif criteria_types[k] == "level":
                        preference = level_criterion(indifference_thresholds[k], preference_thresholds[k], decision_matrix[i][k] - decision_matrix[j][k])
                    preference_matrix[i][j] += preference * normalized_weights[k]
    return preference_matrix

def calculate_flows(preference_matrix):
    """ calculate positive, negative and net flows """
    positive_flow = np.zeros(len(preference_matrix), float)
    negative_flow = np.zeros(len(preference_matrix), float)
    net_flow = np.zeros(len(preference_matrix), float)
    for i in range(len(preference_matrix)):
        for j in range(i+1, len(preference_matrix)):
            positive_flow[i] += preference_matrix[i][j]
            negative_flow[i] += preference_matrix[j][i]
            positive_flow[j] += preference_matrix[j][i]
            negative_flow[j] += preference_matrix[i][j]
        positive_flow[i] = round(positive_flow[i]*1.0 / (len(preference_matrix) -1), 4)
        negative_flow[i] = round(negative_flow[i]*1.0 / (len(preference_matrix) -1), 4)
        net_flow[i] = positive_flow[i] - negative_flow[i]
    return positive_flow, negative_flow, net_flow

def usual_criterion(distance):
    """ implements usual criterion """
    if distance > 0:
        return 1
    else:
        return 0

def quasi_criterion(indifference_threshold, distance):
    """ implements quasi criterion """
    if distance > indifference_threshold:
        return 1
    else:
        return 0

def linear_criterion(preference_threshold, distance):
    """ implements linear criterion without indifference threshold """
    if distance < 0:
        return 0
    elif distance < preference_threshold:
        return distance*1.0 / preference_threshold
    else:
        return 1

def linear_indifference__criterion(indifference_threshold, preference_threshold, distance):
    """ implements linear criterion with indifference threshold """
    if distance < indifference_threshold:
        return 0
    elif distance < preference_threshold:
        return ((distance-indifference_threshold) / (preference_threshold-indifference_threshold))
    else:
        return 1

def level_criterion(indifference_threshold, preference_threshold, distance):
    """ implements level criterion """
    if distance < indifference_threshold:
        return 0
    elif distance < preference_threshold:
        return 0.5
    else:
        return 1
