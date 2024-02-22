try:
    import unzip_requirements
except ImportError:
    pass

from functools import lru_cache
import time
import json
import requests
import boto3

TAG_KEY = 'category'
TAG_VALUE = 'ec2runner'

@lru_cache(maxsize=2)
def ec2client(region):
    return boto3.client("ec2", region_name=region)

def get_instances_by_tag(tag_key_value_map: dict[str, list[str]], region) -> list[dict]:
    ec2_client = ec2client(region)
    res = ec2_client.describe_instances(Filters=[
        {'Name': f'tag:{key}', 'Values': values}
        for key, values in tag_key_value_map.items()
    ])

    instances = []
    for reservation in res['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)
    return instances

def lambda_handler(event, context):
    print("[START] Starting script")

    region = event["awsregion"]
    instance_type = event.get("instance_type", "elastic")

    # find instance
    filter_map = {"category": ["ec2runner"]}
    instances = get_instances_by_tag(filter_map, region)
    print(f"[INFO] target instances: {instances}")
    if not instances:
        response2discord(event, dict(content="Failed to run server. No instance with filter."))
        raise ValueError(f"No target instance. filter: {filter_map}, region: {region}")
    
    # get one instance id
    inst = instances[0]
    instance_id = inst["InstanceId"]

    # run!
    result = start_ec2(instance_id, region)

    
    message = {}
    if result.get("status") == 1:
        message = {
            "content": f'ec2 already starting!\nIP:{result.get("ip","")}'
        }
    elif result.get("status") == 0:
        message = {"content": f'ec2 starting!\nIP:{result.get("ip","")}'}
    else:
        message = {"content": "error!"}
    
    r = response2discord(event, message)

    print(r.text)

    print("[FINISH] Finished runnning script")

    return r.status_code


def start_ec2(instance_id: str, region: str) -> dict:
    try:
        print("[INFO] Starting Instance: " + str(instance_id))
        ec2_client = ec2client(region)
        ec2_resource = boto3.resource("ec2").Instance(instance_id)

        status_response = ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )

        if (
            status_response["Reservations"][0]["Instances"][0]["State"]["Name"]
            == "running"
        ):
            print("[INFO] Instance is already running: " + str(instance_id))
            return {"status": 1, "ip": ec2_resource.public_ip_address}
        else:
            print(
                "[INFO] Instance was not running so called to start: "
                + str(instance_id)
            )
            response = ec2_client.start_instances(InstanceIds=[instance_id])
            print(response)
            ec2_resource.wait_until_running()
            print(
                "[INFO] Waiting for Instance to be ready: " + str(instance_id)
            )
            cont = True
            total = 0

            while cont:
                status_response = ec2_client.describe_instance_status(
                    InstanceIds=[instance_id]
                )
                if (
                    status_response["InstanceStatuses"][0]["InstanceStatus"][
                        "Status"
                    ]
                    == "ok"
                    and status_response["InstanceStatuses"][0]["SystemStatus"][
                        "Status"
                    ]
                    == "ok"
                ):
                    cont = False
                else:
                    time.sleep(10)
                    total += 10
            return {"status": 0, "ip": ec2_resource.public_ip_address}

    except Exception as error:
        print("[ERROR]" + str(error))
        return error

def response2discord(event: dict, message: str):
    application_id = event["appid"]
    interaction_token = event["token"]
    payload = json.dumps(message)
    r = requests.post(
        url=f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}",
        data=payload,
        headers={
            "Content-Type": "application/json",
        },
    )
    return r
