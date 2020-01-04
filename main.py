import boto3
import os
import json
import asyncio
import time
from datetime import datetime, timedelta

# Example
"""
aws cloudwatch get-metric-statistics --namespace "AWS/EC2" \
    --metric-name CPUUtilization \
    --start-time $(date -v-1d -u +"%Y-%m-%dT%H:%M:%SZ") \
    --end-time $(date -u +"%Y-%m-%dT%H:%M:%SZ") --period 300 --namespace AWS/EC2 --statistics Average \
    --dimensions Name=AutoScalingGroupName,Value=nano-ag
"""


def getCPU(client):
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': 'nano-ag'
            },
        ],
        StartTime=datetime.utcnow() - timedelta(days=3),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=[
            'Average',
        ],
        Unit='Percent'
    )

    max = {'perc': 0.0, 'time': datetime.now()}
    gavg = 0.0

    for i in range(len(response["Datapoints"])):
        if response["Datapoints"][i]["Average"] > max["perc"]:
            max["perc"] = response["Datapoints"][i]["Average"]
            max["time"] = response["Datapoints"][i]["Timestamp"]
        gavg += response["Datapoints"][i]["Average"]

    print("Managers group CPU MAX:", str(max["perc"])+'%', max["time"].strftime('%d/%m/%Y %H:%M:%S'),
          ", + 3 days AVG:", str(gavg/len(response["Datapoints"]))+'%')

    return {
        "CPUPEAK": str(max["perc"])+'%',
        "TIME": max["time"].strftime('%d/%m/%Y %H:%M:%S'),
        "AVG": str(gavg/len(response["Datapoints"]))+'%'
    }


def getNET(client):
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='NetworkIn',
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': 'nano-ag'
            },
        ],
        StartTime=datetime.utcnow() - timedelta(days=3),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=[
            'Maximum',
        ],
        # KB / MB / GB etc not available
        Unit='Bytes'
    )

    nettotal = 0.0
    netpeak = {'max': 0.0, 'time': datetime.now()}

    for i in range(len(response["Datapoints"])):
        if response["Datapoints"][i]["Maximum"] > netpeak["max"]:
            netpeak["max"] = response["Datapoints"][i]["Maximum"]
            netpeak["time"] = response["Datapoints"][i]["Timestamp"]
        nettotal += response["Datapoints"][i]["Maximum"]

    print("Managers group NET Peak:", str(round(netpeak["max"]/1024, 0))+' KB', netpeak["time"].strftime(
        '%d/%m/%Y %H:%M:%S'), ", 3 days total:", str(round(nettotal/1024/1024, 0))+" MB")

    return {
        "NETPEAK": str(round(netpeak["max"]/1024, 0))+' KB',
        "TIME": netpeak["time"].strftime('%d/%m/%Y %H:%M:%S'),
        "TOTAL": str(round(nettotal/1024/1024, 0))+" MB"
    }


def lambda_handler(event, context):

    print(json.dumps(event, indent=4, sort_keys=True))

    client = boto3.client('cloudwatch')

    # Well, not easy to save time and money with Python or is a SDK issue?
    # With or without async execution duration is similar (?!)
    """
    # ASYNC
    # Billed Duration: 4900 ms, Memory Size: 128 MB, Max Memory Used: 78 MB, Init Duration: 282.25 ms
    loop = asyncio.new_event_loop()
    task1 = loop.create_task(getCPU(client))
    task2 = loop.create_task(getNET(client))
    loop.run_until_complete(asyncio.wait([task1, task2]))
    loop.close()
    response = {'CPU': task1.result(), 'NET': task2.result()}
    """

    # SYNC
    # Billed Duration: 4900 ms, Memory Size: 128 MB, Max Memory Used: 78 MB, Init Duration: 272.44 ms
    cpures = getCPU(client)
    netres = getNET(client)
    response = {'CPU': cpures, 'NET': netres}

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }


if os.environ.get('AWS_EXECUTION_ENV') is None:
    print(lambda_handler(None, None))
