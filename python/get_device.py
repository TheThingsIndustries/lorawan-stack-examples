#!/usr/bin/env python3

import argparse
import json
import sys

import requests

# Base URL for The Things Stack API.
BASE_URL = "https://eu1.cloud.thethings.network/api/v3"

# API Key for The Things Stack.
API_KEY = "NNSXS.XXXXXXXXXXXXXXXXXXXXXXXXXX.YYYYYYYYYYYYYYYY"


def get_end_device(args):
    url = "{}/applications/{}/devices/{}".format(
        args.api_url, args.application_id, args.device_id
    )
    response = requests.get(
        url,
        headers={
            "authorization": "Bearer {}".format(args.api_key),
            "accept": "application/json",
            "user-agent": "integration/v1.0.0",
        },
        params={
            "field_mask": "name,description",  # querystring parameters
        },
    )

    if response.status_code != 200:
        print("Error {}:\n{}".format(response.status_code, response.text))
        return {}

    device = response.json()
    return device


if __name__ == "__main__":
    parser = argparse.ArgumentParser(sys.argv[0])

    parser.add_argument("application-id", help="Application ID")
    parser.add_argument("device-id", help="End Device ID")
    parser.add_argument("--api-url", help="The Things Stack API URL", default=BASE_URL)
    parser.add_argument("--api-key", help="The Things Stack API Key", default=API_KEY)
    args = parser.parse_args()

    dev = get_end_device(args)

    print("Device: {}".format(dev))

    # Fields with zero values (e.g. empty strings) will not be present in the
    # JSON response, so we use dev.get('name') instead of dev['name']
    print("Device Name: {}".format(dev.get("name")))
    print("Device Description:".format(dev.get("description")))
