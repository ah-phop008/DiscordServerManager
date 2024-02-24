try:
    import unzip_requirements
except ImportError:
    pass

import os
import json
import boto3

# from aws-lambda import (APIGatewayProxyEventV2, APIGatewayProxyResultV2 )
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

DEFAULT_PUBLIC_KEY = ""
DEFAULT_APPLICATION_ID = ""
DEFAULT_AWS_REGION = "ap-northeast-1" # TOKYO
DEFAULT_START_FUNC_NAME = "ec2runner_start"
DEFAULT_STOP_FUNC_NAME = "ec2runner_stop"

public_key = os.environ.get("PUBLIC_KEY") or DEFAULT_PUBLIC_KEY
appid = os.environ.get("APPLICATION_ID") or DEFAULT_APPLICATION_ID
awsregion = os.environ.get("AWS_REGION") or DEFAULT_AWS_REGION
start_func_name = os.environ.get("START_FUNC_NAME") or DEFAULT_START_FUNC_NAME
stop_func_name = os.environ.get("STOP_FUNC_NAME") or DEFAULT_STOP_FUNC_NAME

verify_key = VerifyKey(bytes.fromhex(public_key))


def lambda_handler(event: dict, context: dict):
    try:
        print(f"[INFO] Recieve event: {event}")
        # if event.get("type") == 1:
        #     return {"type": 1} 

        # headers: dict = {k.lower(): v for k, v in event['headers'].items()}
        headers: dict = {k.lower(): v for k, v in event['params']['header'].items()}
        # rawBody: str = event.get("body", "")
        rawBody: str = event.get("rawBody", "")
        signature: str = headers["x-signature-ed25519"]
        timestamp: str = headers["x-signature-timestamp"]

        # validate the interaction
        if not verify(signature, timestamp, rawBody):
            print("return 401")
            return {
                "cookies": [],
                "isBase64Encoded": False,
                "statusCode": 401,
                "headers": {},
                "body": "",
            }

        req: dict = json.loads(rawBody) if isinstance(rawBody, str) else rawBody
        if int(req["type"]) == 1:  # InteractionType.Ping
            # registerCommands()
            print("ping pong")
            return {"type": 1}  # InteractionResponseType.Pong
        elif int(req["type"]) == 2:  # InteractionType.ApplicationCommand
            # command options list -> dict
            # opts = (
            #     {v["name"]: v["value"] for v in req["data"]["options"]}
            #     if "options" in req["data"]
            #     else {}
            # )
            print(req)
            action = req["data"]["options"][0]["value"]
            username = req["member"]["user"]["username"]

            if action.startswith("start"):
                token = req.get("token", "")
                instance_type = "spot" if action.endswith("spot") else "elastic"
                parameter = {
                    "token": token,
                    "appid": appid,
                    "instance_type": instance_type,
                    "awsregion": awsregion,
                }
                payload = json.dumps(parameter)
                boto3.client("lambda").invoke(
                    FunctionName=start_func_name,
                    InvocationType="Event",
                    Payload=payload,
                )
                text = "hi " + username + ", server starting up …"
            elif action == "stop":
                token = req.get("token", "")
                parameter = {
                    "token": token,
                    "appid": appid,
                    "awsregion": awsregion,
                }
                payload = json.dumps(parameter)
                boto3.client("lambda").invoke(
                    FunctionName=stop_func_name,
                    InvocationType="Event",
                    Payload=payload,
                )
                text = "hi " + username + ", server stopping …"
            elif action == "status":
                return {"type": 4,"data": {"content": "currently not in service"}}
                token = req.get("token", "")
                parameter = {
                    "token": token,
                    "DISCORD_APP_ID": appid,
                }
                payload = json.dumps(parameter)
                boto3.client("lambda").invoke(
                    FunctionName="discord-slash-command-dev-minecraft-ec2-status",
                    InvocationType="Event",
                    Payload=payload,
                )
                text = "scanning…"
            else:
                text = "Hello!"
        else:
            text = "unknown command"
        return {
            "type": 4,  # InteractionResponseType.ChannelMessageWithSource
            "data": {"content": text},
        }

    except Exception as e:
        print("[ERROR]" + str(e))
        return e


def verify(signature: str, timestamp: str, body: str) -> bool:
    try:
        verify_key.verify(
            f"{timestamp}{body}".encode(), bytes.fromhex(signature)
        )
    except BadSignatureError:
        print(f"invalid request signature")
        return False
    except Exception as e:
        print(f"failed to verify request: {e}")
        return False

    return True

def command_handler(body):
    command = body["data"]["name"]

    if command == "hello":
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "type": 4,
                    "data": {
                        "content": "Hello, World.",
                    },
                }
            ),
        }
    else:
        return {"statusCode": 400, "body": json.dumps("unhandled command")}
