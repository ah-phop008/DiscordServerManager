import argparse
import json

import requests

commands = {
    "name": "server",
    "description": "control ec2 server",
    "options": [
        {
            "name": "action",
            "description": "start/stop/status",
            "type": 3,
            "required": True,
            "choices": [
                {"name": "start", "value": "start-elastic"},
                {"name": "startrich", "value": "start-elastic"},
                {"name": "stop", "value": "stop"},
                {"name": "status", "value": "status"},
            ],
        },
    ],
}

def main(token, appid):
    url = f"https://discord.com/api/v10/applications/{appid}/commands"
    headers = {
        "Authorization": f'Bot {token}',
        "Content-Type": "application/json",
    }
    res = requests.post(url, headers=headers, data=json.dumps(commands))
    print(res.content)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-t", '--token', type=str, help='Bot token')
    p.add_argument("-a", '--appid', type=str, help='Application ID')

    args = p.parse_args()
    if not args.token:
        raise ValueError("--token option must be set")
    if not args.appid:
        raise ValueError("--appid option must be set")
    main(args.token, args.appid)
