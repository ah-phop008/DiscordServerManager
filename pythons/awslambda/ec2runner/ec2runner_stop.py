try:
    import unzip_requirements
except ImportError:
    pass

from functools import lru_cache
import json
import requests
import boto3

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
    print("[START] Starting Script")

    region = event["awsregion"]
    # find instance
    filter_map = {"category": ["ec2runner"]}
    instances = get_instances_by_tag(filter_map, region)
    print(f"[INFO] target instances: {instances}")
    if not instances:
        response2discord(event, dict(content="Failed to stop server. No instance with filter."))
        raise ValueError(f"No target instance. filter: {filter_map}, region: {region}")
    
    # get one instance id
    inst = instances[0]
    instance_id = inst["InstanceId"]

    stop_ec2_instances(instance_id, region)

    message = {"content": "ec2 stopping!"}
    r = response2discord(event, message)
    print("[FINISH] Finished stopping script")

    return


def stop_ec2_instances(instance_id: str, region) -> None:
    """
    Stop all instances and wait until they are stopped.
    NOTE: the wait method can only wait for one instance at a time
    This script is not expected to stop multiple instances at once
    therefore will not loop all instances to wait.
    """
    try:
        print("[INFO] Stopping Instance: " + str(instance_id))
        ec2_client = ec2client(region)
        ec2_resource = boto3.resource("ec2").Instance(instance_id)
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        print(response)
        ec2_resource.wait_until_stopped()
        print(
            "[INFO] Successfully Called to Stop Instance: " + str(instance_id)
        )

    except Exception as error:
        print("[ERROR] " + str(error))
        # call_sns(str(error))
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
