import os
import sys

import numpy as np
import pandas as pd
import math
from flask import Flask, jsonify, send_from_directory
from settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from werkzeug.utils import secure_filename

def normalize_weights(weights):
    """ normalizes criteria's weigths """
    normalized_weights = [0 for j in range(len(weights))]
    weights_sum = sum(weights)
    for j in range(len(weights)):
        normalized_weights[j] = (weights[j]*1.0 / weights_sum)
    return normalized_weights

def sort_alternatives(scores, alternatives, reverse):
    """ sorts alternatives by score """
    sorted_scores, sorted_alternatives = (list(t) for t in zip(*sorted(zip(scores, alternatives), reverse=reverse)))
    return sorted_scores, sorted_alternatives

def result_in_json(sorted_alternatives, sorted_scores):
    """ create listo of json objects for alternatives, scores and rankings """
    result = []
    for i in range(len(sorted_alternatives)):
        result.append({"Alternative": sorted_alternatives[i], "Score": sorted_scores[i], "Ranking": i+1})
    return jsonify(result)

def negate_columns(decision_matrix, optimization_type):
    """ negate columns of decision matrix in case optimization type is 1 (minimize) """
    for j in range(len(optimization_type)):
        if optimization_type[j] == 1:
            for i in range(len(decision_matrix)):
                decision_matrix[i][j] = decision_matrix[i][j]*(-1.0)
    return decision_matrix

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

def check_uploaded_data(number_of_criteria, optimization_type, veto_thresholds=[], preference_thresholds=[], indifference_thresholds=[], criteria_types=[]):
    for j in range(len(optimization_type)):
        if optimization_type[j] != 0 and optimization_type[j] != 1:
            raise Exception("Optimization types can only take values of 0 or 1")
    if veto_thresholds != []:
        for j in range(len(veto_thresholds)):
            if veto_thresholds[j] <0:
                raise Exception("Veto thresholds can only take nonnegative values")
    if preference_thresholds != []:
        for j in range(len(preference_thresholds)):
            if preference_thresholds[j] <0:
                raise Exception("Preference thresholds can only take nonnegative values")
    if indifference_thresholds != []:
        for j in range(len(indifference_thresholds)):
            if indifference_thresholds[j] <0:
                raise Exception("Indiferrence thresholds can only take nonnegative values")
    if criteria_types != []:
        for j in range(len(criteria_types)):
            if criteria_types[j] not in ["usual", "quasi", "linear", "linear with indifference threshold", "level"]:
                raise Exception("The criteria types, used in Promethee II, can only take the following values: usual, quasi, linear, linear with indifference threshold, and level.  ")
    if number_of_criteria != len(optimization_type):
        raise Exception("Number of criteria should be the same in both files")
    return

def delete_file(file_path):
    """ delete csv file after usage """
    os.remove(file_path)
    return
