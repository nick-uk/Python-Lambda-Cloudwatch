# Python demo with AWS SDK & Lambda

## What is the repository for?
#### This is a quick Lambda function PoC to work as REST API with API Gateway for demo and performance comparison reasons.

> Generates a JSON output with CPU load peak, Networking IN peak activity and averages/total calculation for the last 3 days for anomaly detection tasks. 

## Results:
#### I tried to call two parallel boto3 async functions to get a faster result but:
- Async calls: Billed Duration: 4900 ms, Memory Size: 128 MB, Max Memory Used: 78 MB, Init Duration: 282.25 ms
- Sync calls:  Billed Duration: 4900 ms, Memory Size: 128 MB, Max Memory Used: 78 MB, Init Duration: 272.44 ms

> Seems I got same total execution times. Is not easy to save time and money with Python and Lambda, is a coding or an SDK issue?

> See Go implementation comparison results at: https://github.com/nick-uk/Go-Lambda-Cloudwatch/blob/master/README.md
