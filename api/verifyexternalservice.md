# Verify External Service

## Endpoint Path

/bootstrap/verifyexternalservice

## Endpoint Method

POST

## Request Body

```json
{
  "externalServices": [
    {
      "target": "Data",
      "pool": [
        "192.168.12.50",
        "192.168.12.51",
        "192.168.12.52"
      ]
    }
  ],
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
  "enableBgp": false
}
```

## Response

### Code

200

### Body

```json
{"externalServices":[{"target":"Data","pool":["192.168.12.50","192.168.12.51","192.168.12.52"]}],"nodes":[{"hostName":"nd-4-2-1-10-node1","serialNumber":"518FBB1F13C5","clusterLeader":false,"role":"Master","managementNetwork":{"ipSubnet":"192.168.7.7/24","ipv6Subnet":"","gateway":"192.168.7.1"},"dataNetwork":{"ipSubnet":"192.168.12.14/24","ipv6Subnet":"","gateway":"192.168.12.1"},"nodeController":{"id":"vnode","ipAddress":"192.168.7.7","loginUser":"rescue-user"},"status":"BootstrapStarted","bgpConfig":{},"self":true}]}
```

