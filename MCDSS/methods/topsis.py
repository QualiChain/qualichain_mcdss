import csv
import numpy as np
import pandas as pd
import logging
import math
import sys
from csv_loaders import read_criteria_details, read_decision_matrix
from helpers import normalize_weights, sort_alternatives, result_in_json, negate_columns, check_uploaded_files, delete_file

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

def normalize_decision_matrix_squares(decision_matrix, weights):
    """ normalizes the decision matrix using the root sum square"""
    normalized_decision_matrix = [[0 for j in range(len(decision_matrix[0]))] for i in range(len(decision_matrix))]
    square_sum = 0.0
    for j in range(len(decision_matrix[0])):
        square_sum = 0.0
        for i in range(len(decision_matrix)):
            square_sum += (decision_matrix[i][j])**2
        for i in range(len(decision_matrix)):
            normalized_decision_matrix[i][j] = decision_matrix[i][j]*weights[j]*1.0 / (math.sqrt(square_sum))
    return normalized_decision_matrix

def calculate_ideal_solutions(normalized_decision_matrix):
    """ calculates ideal and negative-ideal solutions """
    ideal_solution = [0 for j in range(len(normalized_decision_matrix[0]))]
    negative_ideal_solution = [0 for j in range(len(normalized_decision_matrix[0]))]
    max_decision_matrix = np.max(normalized_decision_matrix, axis=0)
    min_decision_matrix = np.min(normalized_decision_matrix, axis=0)
    for j in range(len(normalized_decision_matrix[0])):
        ideal_solution[j] = max_decision_matrix[j]
        negative_ideal_solution[j] = min_decision_matrix[j]
    return ideal_solution, negative_ideal_solution

def calculate_separation_distances(normalized_decision_matrix, ideal_solution, negative_ideal_solution):
    """ calculates separation distance from ideal and negative-ideal solutions """
    distance_ideal = [0 for i in range(len(normalized_decision_matrix))]
    distance_negative_ideal = [0 for i in range(len(normalized_decision_matrix))]
    for i in range(len(normalized_decision_matrix)):
        for j in range(len(normalized_decision_matrix[0])):
            distance_ideal[i] += (normalized_decision_matrix[i][j] - ideal_solution[j])**2
            distance_negative_ideal[i] += (normalized_decision_matrix[i][j] - negative_ideal_solution[j])**2
        distance_ideal[i] = math.sqrt(distance_ideal[i])
        distance_negative_ideal[i] = math.sqrt(distance_negative_ideal[i])
    return distance_ideal, distance_negative_ideal

def calculate_closeness(distance_ideal, distance_negative_ideal):
    """ calculates closeness to ideal solution """
    closeness = [0 for i in range(len(distance_ideal))]
    for i in range(len(distance_ideal)):
        closeness[i] = round(distance_negative_ideal[i]*1.0 / (distance_ideal[i] + distance_negative_ideal[i]), 4)
    return closeness

def main(decision_matrix_file_path, criteria_specification_file_path):
    """ topsis method implementation """
    # read file
    number_of_criteria, number_of_alternatives, alternatives, decision_matrix = read_decision_matrix(decision_matrix_file_path)
    weights, optimization_type = read_criteria_details('Topsis', criteria_specification_file_path)
    check_uploaded_files(number_of_criteria, optimization_type)
    # delete uploaded csv files
    delete_file(decision_matrix_file_path)
    delete_file(criteria_specification_file_path)
    # negate columns of decision matrix in case optimization type is 1 (minimize)
    decision_matrix = negate_columns(decision_matrix, optimization_type)
    # normalize weights
    normalized_weights = normalize_weights(weights)
    # normalize decision_matrix
    normalized_decision_matrix = normalize_decision_matrix_squares(decision_matrix, normalized_weights)
    # calculate ideal and negative - ideal solutions
    ideal_solution, negative_ideal_solution = calculate_ideal_solutions(normalized_decision_matrix)
    # calculate separation distances
    distance_ideal, distance_negative_ideal = calculate_separation_distances(normalized_decision_matrix, ideal_solution, negative_ideal_solution)
    # calculate relative closeness to the ideal solution
    closeness = calculate_closeness(distance_ideal, distance_negative_ideal)
    # sort alternatives by score
    sorted_closeness, sorted_alternatives = sort_alternatives(closeness, alternatives, True)
    return sorted_closeness, sorted_alternatives
