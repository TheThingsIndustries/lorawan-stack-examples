#!/usr/bin/env python3

import argparse
import json
import sys

import requests

# Base URL for The Things Stack API.
BASE_URL = "https://eu1.cloud.thethings.network/api/v3"

# API Key for The Things Stack.
API_KEY = "NNSXS.XXXXXXXXXXXXXXXXXXXXXXXXXX.YYYYYYYYYYYYYYYY"


def get_stored_uplink_messages(args):
    url = "{}/as/applications/{}{}/packages/storage/uplink_message".format(
        args.api_url,
        args.application,
        args.device and "/devices/{}".format(args.device) or "",
    )
    response = requests.get(
        url,
        headers={
            "authorization": "Bearer {}".format(args.api_key),
            "accept": "text/event-stream",  # enable long streaming responses
            "user-agent": "my-integration/1.0.0",
        },
        params={
            "limit": 3,
            "order": "-received_at",  # most recent first
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

        msg = json.loads(line)
        print("\n\nMessage: {}".format(msg))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(sys.argv[0])

    parser.add_argument("application", help="Application ID")
    parser.add_argument("--device", help="End Device ID")
    parser.add_argument("--api-url", help="The Things Stack API URL", default=BASE_URL)
    parser.add_argument("--api-key", help="The Things Stack API Key", default=API_KEY)
    args = parser.parse_args()

    get_stored_uplink_messages(args)
