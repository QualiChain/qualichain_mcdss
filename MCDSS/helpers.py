import numpy as np
import pandas as pd
import math
import json

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
        result.append(json.dumps({"Alternative": sorted_alternatives[i], "Score": sorted_scores[i], "Ranking": i+1}))
    return result

def negate_columns(decision_matrix, optimization_type):
    """ negate columns of decision matrix in case optimization type is 1 (minimize) """
    for j in range(len(optimization_type)):
        if (optimization_type[j] == 1):
            for i in range(len(decision_matrix)):
                decision_matrix[i][j] = decision_matrix[i][j]*(-1.0)
    return decision_matrix
