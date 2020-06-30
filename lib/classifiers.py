from sklearn.ensemble import RandomForestClassifier
import pickle
import json
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def loadClassifiers():
    path = f"{BASE_PATH}/../utils/classifiers"
    rf_org = None
    rf_utl = None
    with open(f'{path}/rf_org.pkl', 'rb') as fid:
        rf_org = pickle.load(fid)
    with open(f'{path}/rf_utl.pkl', 'rb') as fid:
        rf_utl = pickle.load(fid)

    return rf_org, rf_utl


def run(metric_json):
    item = [list(metric_json.values())]
    rf_org, rf_utl = loadClassifiers()

    result_org = rf_org.predict(item)
    result_utl = rf_utl.predict(item)    

    return (not result_org[0] or not result_utl[0])


# if __name__ == '__main__':
#     item = {
#         'ci': 1,
#         'license': 1,
#         'history': 180.66666666666666,
#         'management': 107.0,
#         'documentation': 0.2658569500674764,
#         'community': 3,
#         'tests': 0.0038095238095238095
#     }
#     item2 = {
#         "ci": 0,
#         "license": 0,
#         "history": 17.333333333333332,
#         "management": 0,
#         "documentation": 0.3676183026984748,
#         "community": 1,
#         "tests": 0.0
#     }
#     item3 = {
#         "ci": 0,
#         "license": 0,
#         "history": 10,
#         "management": 0,
#         "documentation": 0.5,
#         "community": 10,
#         "tests": 5.0
#     }
#     a = run([list(item3.values())])
#     print(a)
