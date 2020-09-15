from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import pickle
import json
import os

BASE_DIR = Path(__file__).resolve().parent


def _loadClassifiers():
    print(BASE_DIR)
    rf_org = None
    rf_utl = None
    with open(f'{BASE_DIR}/rf_org.pkl', 'rb') as fid:
        rf_org = pickle.load(fid)
    with open(f'{BASE_DIR}/rf_utl.pkl', 'rb') as fid:
        rf_utl = pickle.load(fid)

    return rf_org, rf_utl


def run(metrics):
    item = [list(metrics.values())]

    rf_org, rf_utl = _loadClassifiers()

    result_org = rf_org.predict(item)
    result_utl = rf_utl.predict(item)

    return (not result_org[0] or not result_utl[0])
