import numpy as np


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
        alternatives[i] = data[i + decision_matrix_index[0][0]][0]
        for j in range(number_of_criteria):
            decision_matrix[i][j] = float(data[i + decision_matrix_index[0][0]][j + decision_matrix_index[0][1]])
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
            optimization_type[j] = int(data[optimization_types_index[0][0]][j + optimization_types_index[0][1] + 1])

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
                preference_thresholds[j] = float(
                    data[preference_thresholds_index[0][0]][j + preference_thresholds_index[0][1] + 1])
                indifference_thresholds[j] = float(
                    data[indifference_threshold_index[0][0]][j + indifference_threshold_index[0][1] + 1])
                criteria_types[j] = data[criteria_types_index[0][0]][j + criteria_types_index[0][1] + 1]
            return weights, preference_thresholds, indifference_thresholds, optimization_type, criteria_types
        else:
            return weights, optimization_type
    except Exception as ex:
        raise Exception("Wrong configuration of the uploaded files")


def create_decision_matrix_json(json_decision_matrix):
    """ read decision matrix from json """
    number_of_alternatives = int(json_decision_matrix['Number_of_alternatives'])
    number_of_criteria = int(json_decision_matrix['Number_of_criteria'])
    alternatives_values = json_decision_matrix['Alternatives']
    decision_matrix = [[0 for j in range(number_of_criteria)] for i in range(number_of_alternatives)]
    alternatives = ["" for i in range(number_of_alternatives)]
    for i in range(number_of_alternatives):
        alternatives[i] = alternatives_values[i]['Name']
        for j in range(number_of_criteria):
            decision_matrix[i][j] = float(alternatives_values[i]['Values'][j])
    return number_of_criteria, number_of_alternatives, alternatives, decision_matrix


def create_criteria_details_json(method, criteria_details_json):
    try:
        """ read criteria details from json """
        number_of_criteria = int(criteria_details_json['Number_of_criteria'])
        weights = [0 for j in range(number_of_criteria)]
        optimization_type = [0 for j in range(number_of_criteria)]
        for j in range(number_of_criteria):
            weights[j] = float(criteria_details_json['Weights'][j])
            optimization_type[j] = int(criteria_details_json['Optimization_Type'][j])

        if method == "Electre I":
            agreement_threshold = float(criteria_details_json['Agreement_Threshold'])
            veto_thresholds = [0 for j in range(number_of_criteria)]
            for j in range(number_of_criteria):
                veto_thresholds[j] = float(criteria_details_json['Veto_Thresholds'][j])
            return agreement_threshold, weights, veto_thresholds, optimization_type
        elif method == "Promethee II":
            preference_thresholds = [0 for j in range(number_of_criteria)]
            indifference_thresholds = [0 for j in range(number_of_criteria)]
            criteria_types = ["" for j in range(number_of_criteria)]
            for j in range(number_of_criteria):
                preference_thresholds[j] = float(criteria_details_json['Preference_Thresholds'][j])
                indifference_thresholds[j] = float(criteria_details_json['Indifference_Thresholds'][j])
                criteria_types[j] = criteria_details_json['Criteria_Types'][j]
            return weights, preference_thresholds, indifference_thresholds, optimization_type, criteria_types
        else:
            return weights, optimization_type
    except Exception as ex:
        raise Exception("Wrong configuration of the input")
