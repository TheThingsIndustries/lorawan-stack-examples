#!/usr/bin/env python3

import argparse
import json
import sys

import requests

# Base URL for The Things Stack API.
BASE_URL = "https://eu1.cloud.thethings.network/api/v3"

# API Key for The Things Stack.
API_KEY = "NNSXS.XXXXXXXXXXXXXXXXXXXXXXXXXX.YYYYYYYYYYYYYYYY"


def subscribe_to_device_events(args):
    url = "{}/events".format(args.api_url)
    response = requests.post(
        url,
        headers={
            "authorization": "Bearer {}".format(args.api_key),
            "content-type": "application/json",
            "accept": "text/event-stream",  # enable long streaming responses
            "user-agent": "my-integration/1.0.0",
        },
        json={
            "identifiers": [
                {
                    "device_ids": {
                        "application_ids": {"application_id": args.application_id},
                        "device_id": args.device_id,
                    },
                }
            ],
        },
        stream=True,  # set stream to True, so that the response is read in chunks
    )

    if response.status_code != 200:
        print("Error {}:\n{}".format(response.status_code, response.text))
        return {}

    for line in response.iter_lines():
        # Consecutive responses are separated by a double new-line ('\n\n'), so
        # we ignore empty lines
        if not line:
            continue

        event_data = json.loads(line)
        print("New event: {}".format(event_data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(sys.argv[0])

    parser.add_argument("application-id", help="Application ID")
    parser.add_argument("device-id", help="End Device ID")
    parser.add_argument("--api-url", help="The Things Stack API URL", default=BASE_URL)
    parser.add_argument("--api-key", help="The Things Stack API Key", default=API_KEY)
    args = parser.parse_args()

    subscribe_to_device_events(args)
