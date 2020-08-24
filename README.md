# Qualichain-MCDSS

The Multi-Criteria Decision Support System facilitates the decision-making process by taking into account all the meaningful criteria.  
As of now the implemented methods are the following: MAUT, Topsis, Electre I and Promethee II.

You can access the MCDSS from port `7070`.

## Docker Installation

To install MCDSS using docker run the following command:

1. Install MCDSS using QualiChain Network Dependencies: `docker-compose up -d --build`
2. Standalone Installation: `docker-compose -f docker-compose.dev.yml up -d --build`

## Local Installation

1. Install Requirements: `pip install -r requirements.txt`
2. Go to /MCDSS folder using the command: `cd MCDSS`
3. Create a folder named **uploads** inside MCDSS folder using the command: `mkdir uploads`
3. Execute the command: `python3 -m flask run`

## MCDSS API

### Access points:

1. Maut (input: json): `http://127.0.0.1:7070/mcdss/maut`
2. Topsis (input: json): `http://127.0.0.1:7070/mcdss/topsis`
3. Electre I (input: json): `http://127.0.0.1:7070/mcdss/electreI`
4. Promethee II (input: json): `http://127.0.0.1:7070/mcdss/prometheeII`
5. Maut (input: csv files): `http://127.0.0.1:7070/mcdss/maut/file`
6. Topsis (input: csv files): `http://127.0.0.1:7070/mcdss/topsis/file`
7. Electre I (input: csv files): `http://127.0.0.1:7070/mcdss/electreI/file`
8. Promethee II (input: csv files): `http://127.0.0.1:7070/mcdss/prometheeII/file`
9. General access point for all methods (input: csv files): `http://127.0.0.1:7070/mcdss/file`

### Input

The MCDSS API receives POST requests that contain **one** of the following:

1. a json object that contains information about the Decision Matrix and the Criteria Details (a point (.) should be used as decimal separator)
2.	- a UTF-8 encoded csv file that contains the Decision Matrix (a point (.) should be used as decimal separator, while semicolon (;) is the csv separator)
    - a UTF-8 encoded csv file that contains the Criteria Details (a point (.) should be used as decimal separator, while semicolon (;) is the csv separator)
    - the preferred method which can only take the following values: Maut, Topsis, Promethee II, and Electre I **(only in case the access point `http://127.0.0.1:7070/mcdss` is used)**

#### JSON Object

The JSON object includes information about the decision matrix and the criteria details.

Optimization types can only take values of 0 or 1, with 0 denoting that the criterion is profit maximization and 1 denoting that it is cost minimization.  
The criteria types, used in Promethee II, can only take the following values: usual, quasi, linear, linear with indifference threshold, and level.  
All thresholds can only take nonnegative value.

Each method requires a specific set of **criteria details** to be configured.
*	In case the preferred method is either “Maut” or “Topsis”, users should insert information about the number of criteria, the weights, and the optimization types.
*	In case the preferred method is “Electre I”, users should insert information about the number of criteria, the weights, the optimization types, the agreement threshold, and the veto thresholds.
*	In case the preferred method is “Promethee II”, users should insert information about the number of criteria, the weights, the optimization types, the preference thresholds, the indifference thresholds, and the criteria types.

Examples of JSON objects can be found in folder [/Input_Templates/json_examples](https://gitlab.epu.ntua.gr/qualichain/qualichain-mcdss/-/tree/master/Input_Templates/json_examples).

#### Decision Matrix CSV

The “Decision Matrix” file includes information about the number of alternatives, the number of criteria and the decision matrix.
The text that appears in bold should not be changed.

|**Number of alternatives**||||||
|----|----|----|----|----|----|
|**Number of criteria**||||||
|**Alternatives / Criteria**|Criterion 1|Criterion 2|Criterion 3|Criterion 4|...|
|Alternative 1||||||
|Alternative 2||||||
|Alternative 3||||||
|Alternative 4||||||
|Alternative 5||||||
|...||||||

Examples of Decision Matrix csv files can be found in folder [/Input_Templates/csv_examples](https://gitlab.epu.ntua.gr/qualichain/qualichain-mcdss/-/tree/master/Input_Templates/csv_examples).

#### Criteria Details CSV

The “Criteria Details” file includes information about the number of criteria, their weights, optimization types and types, and different types of thresholds (veto, preference, etc.).
The text that appears in bold should not be changed.

|**Number of criteria**||||||
|----|----|----|----|----|----|
|**Agreement Threshold**||||||
||Criterion 1|Criterion 2|Criterion 3|Criterion 4|...|
|**Weights**||||||
|**Optimization Type**||||||
|**Veto Thresholds**||||||
|**Preference Thresholds**||||||
|**Indifference Thresholds**||||||
|**Criteria Types**||||||

Optimization types can only take values of 0 or 1, with 0 denoting that the criterion is profit maximization and 1 denoting that it is cost minimization.  
The criteria types, used in Promethee II, can only take the following values: usual, quasi, linear, linear with indifference threshold, and level.  
All thresholds can only take nonnegative value.

Each method requires a specific set of cells to be filled.
*	In case the preferred method is either “Maut” or “Topsis”, users should insert information about the number of criteria, the weights, and the optimization types.
*	In case the preferred method is “Electre I”, users should insert information about the number of criteria, the weights, the optimization types, the agreement threshold, and the veto thresholds.
*	In case the preferred method is “Promethee II”, users should insert information about the number of criteria, the weights, the optimization types, the preference thresholds, the indifference thresholds, and the criteria types.

Examples of Criteria Details csv files can be found in folder [/Input_Templates/csv_examples](https://gitlab.epu.ntua.gr/qualichain/qualichain-mcdss/-/tree/master/Input_Templates/csv_examples).

### Request Examples

This is an example API call that demonstrates the three different ways to invoke the Maut method.

```curl
curl --location --request POST 'http://127.0.0.1:7070/mcdss/maut' \
--header 'Content-Type: application/json' \
--data-raw '
{
  "Decision_Matrix":
    {
      "Number_of_alternatives": 3,
        "Number_of_criteria": 5,
        "Criteria": ["Criterion 1", "Criterion 2", "Criterion 3", "Criterion 4", "Criterion 5"],
        "Alternatives": [
            {
                "Name": "Alternative 1",
                 "Values": [85, 75, 75, 65, 75]
            },
            {
                "Name": "Alternative 2",
                 "Values": [80, 65, 75, 62.5, 75]
            },
            {
                "Name": "Alternative 3",
                 "Values": [50, 17.5, 70, 6.12, 60]
            }
        ]
    },
  "Criteria_Details":
    {
      "Number_of_criteria": 5,
        "Weights": [70, 75, 42.5, 77.5, 75],
        "Optimization_Type": [0, 0, 0, 0, 0]
    }
}
'
```

```curl
curl --location --request POST 'http://127.0.0.1:7070/mcdss/maut/file' \
--form 'Decision Matrix=@/qualichain-mcdss/Input_Templates/Decision_Matrix_Maut.csv' \
--form 'Criteria Details=@/qualichain-mcdss/Input_Templates/Criteria_Specification_Maut.csv'
```

```curl
curl --location --request POST 'http://127.0.0.1:5000/mcdss/file' \
--form 'Decision Matrix=@/qualichain-mcdss/Input_Templates/Decision_Matrix_Maut.csv' \
--form 'Criteria Details=@/qualichain-mcdss/Input_Templates/Criteria_Specification_Maut.csv' \
--form 'method=Maut'
```

### Response Examples

The MCDSS returns as a response a list of JSON objects.

In case the used method is Maut, Topsis or Promethee II, the list contains one JSON object for each alternative which consists of the name of the respective
alternative, its score and its rank. For example, the MCDSS can return:

```json
[
    {
        "Alternative": "Alternative 3",
        "Ranking": 1,
        "Score": 0.93
    },
    {
        "Alternative": "Alternative 1",
        "Ranking": 2,
        "Score": 0.19669999999999999
    },
    {
        "Alternative": "Alternative 2",
        "Ranking": 3,
        "Score": -0.37660000000000005
    },
    {
        "Alternative": "Alternative 4",
        "Ranking": 4,
        "Score": -0.75
    }
]
```

In case the used method is ELECTRE I, the list contains only one JSON object which consists of a list of the names of all alternatives and the dominance matrix.
For example, the MCDSS can return:

```json
[
    {
        "Alternatives": [
            "Alternative 1",
            "Alternative 2",
            "Alternative 3",
            "Alternative 4",
            "Alternative 5",
            "Alternative 6"
        ],
        "Dominance Table": [
            [
                0, 1, 0, 0, 0, 0
            ],
            [
                0, 0, 0, 0, 0, 0
            ],
            [
                0, 1, 0, 0, 0, 0
            ],
            [
                0, 1, 1, 0, 0, 0
            ],
            [
                0, 0, 0, 0, 0, 0
            ],
            [
                0, 0, 0, 0, 0, 0
            ]
        ]
    }
]
```
