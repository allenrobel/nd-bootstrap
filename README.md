# Summary

Bootstrap a Nexus Dashboard cluster.

## Features

- Supports both IPv4 and IPv6 connectivity to Nexus Dashboard
- Uses environment variables for Nexus Dashboard connection and authentication
  - More secure than hardcoding credentials in the configuration file
  - Easier to integrate with CI/CD pipelines and secret management systems
  - Easier to use with shell scripts and automation tools
- Loads and validates a YAML configuration file
  - Separation of config from code
  - Create unique config file for each Nexus Dashboard setup
- Validates NTP servers are reachable and compatible from Nexus Dashboard's perspective prior to POST
- Retrieves node credentials from environment variables and dynamically updates the node configurations prior to POST
  - More secure and flexible than hardcoding credentials in the configuration file
- Retrieves node serial numbers from Nexus Dashboard and dynamically updates the node configurations prior to POST
  - No need to manually specify serial numbers in the configuration file
- Supports a --dry-run flag to perform all validation steps but skip the final POST to bootstrap the cluster
- Supports a --poll-install-status flag to poll for bootstrap completion before exiting
  - polling behavior can be controlled with --retries and --interval flags
- Posts the configuration to Nexus Dashboard after the terminal-based bringup is complete
- Modular design with classes for environment, login, configuration, NTP validation, and bootstrapping
- Uses requests library for HTTP interactions
- Uses PyYAML for YAML parsing
- Includes detailed error handling and informative messages

## Environment Variables

The following environment variables define the connectivity parameters when connecting to Nexus Dashboard.

- ND_IP4: The IPv4 address of the Nexus Dashboard
- ND_IP6: The IPv6 address of the Nexus Dashboard
- ND_IP_PROTOCOL: The IP protocol to use, either "IP4" or "IP6". Default is "IP4".
- ND_USERNAME: The username to authenticate with Nexus Dashboard
- ND_PASSWORD: The password to authenticate with Nexus Dashboard
- ND_DOMAIN: The domain to authenticate with Nexus Dashboard. Default is "local".

## Quick start

### 0. Repository setup

It's highly recommended to use a virtual environment, per below.

```bash
cd $HOME/repos/nd-bootstrap
python3 -m venv .venv --prompt nd-bootstrap
pip install uv
uv sync
# For development
uv sync --extra dev
```

### 1. Edit the example YAML bootstrap configuration file to suit your environment.

Note, the example file (`nd_bootstrap_vnode.yaml`) is tailored to Nexus Dashboard running under KVM
(aka vNd/KVM).  We will include example configuration files for physical Nexus Dashboard appliances
(pNd) and vNd running under VMWare once these have been tested.

### 2. Set the environment variables as shown below

Note, these could be set in a shell script tailored to a specific Nexus Dashboard instance, and collections
of these scripts built up for your various Nexus Dashboard instances.

```bash
# optional, defaults to local
export ND_DOMAIN=local
# optional preferred IP protocol, defaults to IP4
export ND_IP_PROTOCOL=IP4
export ND_IP4=192.168.1.1
# optional, (mandatory if ND_IP_PROTOCOL is set to IP6)
export ND_IP6=2001:db8::1
./nd_bootstrap.py path/to/bootstrap.yaml [--dry-run]
export ND_PASSWORD=MyPassword
export ND_USERNAME=admin
```

### 3. Run the script with --dry-run to validate the configuration

Optionally use the --dry-run flag to validate the configuration NTP server compatibility and reachability, without
posting the configuration.

```bash
cd $HOME/repos/nd-bootstrap
./nd_bootstrap.py nd_bootstrap_vnode.yaml --dry-run
```

### 4. Run the script without --dry-run to post the configuration to Nexus Dashboard and poll for bootstrap completion

```bash
cd $HOME/repos/nd-bootstrap
./nd_bootstrap.py nd_bootstrap_vnode.yaml --poll-install-status --retries 30 --interval 20
```

### Example output (with --dry-run option)

```bash
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_IP4=192.168.7.13
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_IP_PROTOCOL=IP4
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_USERNAME=admin
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_PASSWORD=******
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % export ND_DOMAIN=local
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode.yaml --dry-run
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