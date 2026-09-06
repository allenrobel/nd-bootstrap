# Verify Cluster Subnets

## Endpoint Path

## Endpoint Method

POST

## Request Body

```json
{
  "enableBgp": false,
  "nodes": [
    {
      "id": "1",
      "hostName": "nd-4-2-1-10-node1",
      "serialNumber": "518FBB1F13C5",
      "role": "Master",
      "dataNetwork": {
        "ipSubnet": "192.168.12.14/24",
        "gateway": "192.168.12.1",
        "ipv6Subnet": "",
        "gatewayv6": ""
      },
      "managementNetwork": {
        "ipSubnet": "192.168.7.7/24",
        "gateway": "192.168.7.1",
        "ipv6Subnet": "",
        "gatewayv6": ""
      },
      "nodeController": {
        "id": "vnode",
        "ipAddress": "192.168.7.7",
        "loginUser": "rescue-user"
      },
      "bgpConfig": {},
      "clusterLeader": false,
      "self": true,
      "mgmtIp": "192.168.7.7/24",
      "dataIp": "192.168.12.14/24",
      "notDeletable": false
    }
  ],
  "persona": "LAN"
}
```

## Response

### Success

200
