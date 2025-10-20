# Example output (with --dry-run option) prior to bootstrap being initiated

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_IP4=192.168.7.13
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_IP_PROTOCOL=IP4
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_USERNAME=admin
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_PASSWORD=******
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_DOMAIN=local
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_322m_vnode.yaml --dry-run
NdBootstrap.commit: Bootstrapping cluster 'ND14-3' on Nexus Dashboard at 192.168.7.13.

NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.13/24 to serialNumber 494C0DD63549.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.post_bootstrap_configuration: DRY RUN: Skipping POST to cluster bootstrap endpoint.
Would POST the following configuration to https://192.168.7.13/v2/bootstrap/cluster if --dry_run were not set:
{
    "clusterConfig": {
        "ntpConfig": {
            "servers": [
                {
                    "host": "192.168.7.6",
                    "prefer": true
                }
            ]
        },
        "name": "ND14-3",
        "searchDomains": [
            "arobel.com"
        ],
        "ignoreHosts": [],
        "nameServers": [
            "192.168.7.1"
        ],
        "proxyServers": [],
        "appNetwork": "172.17.0.1/16",
        "serviceNetwork": "100.80.0.0/16",
        "externalServices": [
            {
                "target": "Management",
                "pool": [
                    "192.168.7.40",
                    "192.168.7.41",
                    "192.168.7.42"
                ]
            },
            {
                "target": "Data",
                "pool": [
                    "192.168.14.40",
                    "192.168.14.41",
                    "192.168.14.42"
                ]
            }
        ],
        "deploymentMode": "ndfc"
    },
    "nodes": [
        {
            "hostName": "ND13-3-1",
            "clusterLeader": false,
            "role": "Master",
            "self": true,
            "dataNetwork": {
                "ipSubnet": "192.168.14.3/24",
                "gateway": "192.168.14.1",
                "ipv6Subnet": "",
                "gatewayv6": ""
            },
            "managementNetwork": {
                "ipSubnet": "192.168.7.13/24",
                "gateway": "192.168.7.1",
                "ipv6Subnet": "",
                "gatewayv6": ""
            },
            "bgpConfig": {},
            "nodeController": {
                "id": "vnode",
                "loginUser": "rescue-user"
            },
            "serialNumber": "494C0DD63549"
        }
    ]
}
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```
