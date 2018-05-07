import json
import requests
import sys

def main(args, url="http://localhost:14041/jsonrpc", headers = {'content-type': 'application/json'}):
    # Example payload
    payload = {
        "method": args[0],
        "params": args[1:] if len(args) > 1 else [],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers=headers
    ).json()
    print(response)


if __name__ == "__main__":
    main(sys.argv[1:])
