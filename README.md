# Python demo with AWS SDK

## What is the repository for?
#### This is a quick Lambda function PoC to work as REST API with API Gateway for demo and performance comparison reasons.

> Generates a JSON output with CPU load peak, Networking IN peak activity and averages/total calculation for the last 3 days for anomaly detection tasks. 

## Results:
#### I tried to call two parallel boto3 async functions to get a faster result but:
- With or without async execution duration is the same around 4900 ms (?!)
- Billed Duration: 5000 ms for both sync/async cases. 77 MB Init Duration: 258.77 ms

> Is not easy to save time and money with Python and Lambda, is a coding or an SDK issue?
