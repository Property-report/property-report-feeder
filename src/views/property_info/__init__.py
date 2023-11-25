import requests
from src import config
from flask import jsonify, Response
import json
from datetime import datetime
import base64


def get_info(postcode, house_number, street, bedrooms, type, lon, lat, uprn):
    url = "{}/info".format(config.property_information_api_url)

    headers = {
        'Content-Type': "application/json",
    }

    resp = requests.request(
        "GET", url, data=json.dumps({
            "postcode": postcode,
            "house_number": house_number,
            "street": street,
            "bedrooms": bedrooms,
            "type": type,
            "lon": lon,
            "lat": lat,
            "uprn": uprn
        }), headers=headers)
    data = json.loads(resp.text)

    return data
