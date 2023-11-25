import requests
from src import config
from datetime import datetime

import json


def set_report_creation_time(report_id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.put(
        f'{config.ACCOUNT_API_URL}/report/{report_id}',
        data=json.dumps({
            "creation_status": "in_progress",
            "creation_start": datetime.utcnow().isoformat(),
        }),
        headers=headers
    )
    resp = json.loads(response.text)
    return resp


def store_report_data(report_id, report_data):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.put(
        f'{config.ACCOUNT_API_URL}/report/{report_id}',
        data=json.dumps({
            "report_data": report_data,
            "report_data_stored": True,
        }),
        headers=headers
    )
    resp = json.loads(response.text)
    return resp


def get_report_data(report_id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.get(
        f'{config.ACCOUNT_API_URL}/report/{report_id}/report_data',
        headers=headers
    )
    resp = json.loads(response.text)
    return resp


def report_created(report_id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.put(
        f'{config.ACCOUNT_API_URL}/report/{report_id}',
        data=json.dumps({
            "creation_status": "complete"
        }),
        headers=headers
    )
    resp = json.loads(response.text)
    return resp
