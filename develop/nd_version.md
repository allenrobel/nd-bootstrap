# Class name

NdVersion

## File name

nd_bootstrap/version.py

## Class behavior

- import NdEnvironment for credentials (from nd_bootstrap.environment import NdEnvironment)
- expose public setter/getter property `session` which accepts and returns a requests.Session instance
- expose public method NdVersion.commit() to send the request.
- expose public getter property `info` which contains the response body.

## Endpoint

### Path

https://192.168.7.13/version.json

### Verb

GET

### Response body

```json
    {
        "commit_id": "07a8f967",
        "build_time": "now",
        "build_host": "kube14",
        "user": "root",
        "product_id": "nd",
        "product_name": "Nexus Dashboard",
        "release": false,
        "major": 3,
        "minor": 2,
        "maintenance": 2,
        "patch": "m"
    }
```
