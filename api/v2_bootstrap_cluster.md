## Endpoint Path

/v2/bootstrap/cluster

## Endpoint Verb

POST

## Request Body

```json
{
  "clusterConfig": {
    "name": "nd-4-2-1-10",
    "ntpConfig": {
      "servers": [
        {
          "host": "192.168.7.6",
          "prefer": true
        }
      ]
    },
    "nameServers": [
      "192.168.7.1"
    ],
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
    "persona": "LAN",
    "appNetwork": "172.17.0.1/16",
    "serviceNetwork": "100.80.0.0/16"
  },
  "nodes": [
    {
      "hostName": "nd-4-2-1-10-node1",
      "clusterLeader": false,
      "role": "Master",
      "self": true,
      "serialNumber": "518FBB1F13C5",
      "dataNetwork": {
        "ipSubnet": "192.168.12.14/24",
        "gateway": "192.168.12.1"
      },
      "managementNetwork": {
        "ipSubnet": "192.168.7.7/24",
        "gateway": "192.168.7.1"
      },
      "bgpConfig": {},
      "nodeController": {
        "id": "vnode",
        "ipAddress": "192.168.7.7",
        "loginUser": "rescue-user"
      }
    }
  ]
}
```

## Response

### 200

### Response Text

None


