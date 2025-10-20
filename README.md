# Summary

Bootstrap a Nexus Dashboard cluster.

## Features

- Supports both IPv4 and IPv6 connectivity to Nexus Dashboard
- Verified to work with Nexus Dashboard versions
  - 3.2(2)m
  - 4.1(1)g
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
- Supports a --poll-status flag to poll for bootstrap completion before exiting
  - polling behavior can be controlled with --retries and --interval flags
  - Polls for bootstrap completion
  - Polls for healthy services state after bootstrap is complete
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

Note, both of the example configuration files (322m for ND 3.2(2)m and 411g for ND4.1(1)g)
are tailored to Nexus Dashboard running under KVM (aka vNd/KVM).  We will include example
configuration files for physical Nexus Dashboard appliances (pNd) and vNd running under
VMmare ESXi once these have been tested.

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
./nd_bootstrap.py nd_bootstrap_322m_vnode.yaml --dry-run
```

### 4. Run the script without --dry-run to post the configuration to Nexus Dashboard and poll for bootstrap completion and services health

```bash
cd $HOME/repos/nd-bootstrap
./nd_bootstrap.py nd_bootstrap_322m_vnode.yaml --poll-status --retries 30 --interval 20
```

### Example output (with --dry-run option) prior to bootstrap being initiated

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

### Example output (322m), successful bootstrap

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode_322m.yaml --poll --retries 200 --interval 5
NdBootstrap.commit: Bootstrapping cluster 'ND14-3' on Nexus Dashboard at 192.168.7.13.
NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.13/24 to serialNumber 94D03F101E9E.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.send_bootstrap_configuration: Sending bootstrap configuration to Nexus Dashboard at https://192.168.7.13/v2/bootstrap/cluster.
NdBootstrap.send_bootstrap_configuration: Cluster bootstrap initiated successfully.
NdPollBootstrapStatus.commit: Polling bootstrap status until complete. Max retries: 200, interval: 5 seconds.
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 199, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 198, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 197, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 196, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 195, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 194, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 193, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 192, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 191, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 190, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 189, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 188, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 187, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 186, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 185, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 184, state: Completed, overall_progress: 100, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.commit: Bootstrap complete.
NdPollInstallStatus.commit: Polling install status until complete. Max retries: 200, interval: 5 seconds.
NdPollInstallStatus.poll_once: Install status: retries 199, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 198, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 197, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 196, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 195, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 194, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.login_refresh: Refreshing login. You may see this message multiple times during install polling.
NdPollInstallStatus.login_refresh: Sleeping 10 seconds before attempting re-authentication.
NdPollInstallStatus.login_refresh: Re-authentication successful.
NdPollInstallStatus.poll_once: Install status: retries 192, state: InProgress, overall_progress: 28, overall_status: Setup ND Cluster
NdPollInstallStatus.poll_once: Install status: retries 191, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 190, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 189, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 188, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 187, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 186, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 185, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 184, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 183, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 182, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 181, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 180, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 179, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 178, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 177, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 176, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 175, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 174, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 173, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 172, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 171, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 170, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 169, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 168, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 167, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 166, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 165, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 164, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 163, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 162, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 161, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 160, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 159, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 158, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 157, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 156, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 155, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 154, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 153, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 152, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 151, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 150, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 149, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 148, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 147, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 146, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 145, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 144, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 143, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 142, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 141, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 140, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 139, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 138, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 137, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 136, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 135, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 134, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 133, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 132, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 131, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 130, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 129, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 128, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 127, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 126, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 125, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 124, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 123, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 122, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 121, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 120, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 119, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 118, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 117, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 116, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 115, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 114, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 113, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 112, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 111, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 110, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 109, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 108, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 107, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 106, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 105, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 104, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 103, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 102, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 101, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 100, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 99, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 98, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 97, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 96, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 95, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 94, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 93, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 92, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 91, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 90, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 89, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 88, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 87, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 86, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 85, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 84, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 83, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 82, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 81, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 80, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 79, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 78, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 77, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 76, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 75, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 74, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 73, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 72, state: Completed, overall_progress: 100, overall_status: Wait for infra services to be ready
NdPollInstallStatus.commit: Install complete.
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```

### Example output (411g), successful bootstrap

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode_411g.yaml --poll --retries 200 --interval 5
NdBootstrap.commit: Bootstrapping cluster 'ND411g-2' on Nexus Dashboard at 192.168.7.14.
NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.14/24 to serialNumber 7290C46C15AB.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.send_bootstrap_configuration: Sending bootstrap configuration to Nexus Dashboard at https://192.168.7.14/v2/bootstrap/cluster.
NdBootstrap.send_bootstrap_configuration: Cluster bootstrap initiated successfully.
NdPollBootstrapStatus.commit: Polling bootstrap status until complete. Max retries: 200, interval: 5 seconds.
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 199, state: InProgress, overall_progress: 1, overall_status: Initialize node
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 198, state: InProgress, overall_progress: 1, overall_status: Initialize node
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 197, state: InProgress, overall_progress: 1, overall_status: Initialize node
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 196, state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 195, state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 194, state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 193, state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 192, state: InProgress, overall_progress: 32, overall_status: Setup boot time configuration
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 191, state: InProgress, overall_progress: 37, overall_status: Upload system configuration to all nodes
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 190, state: InProgress, overall_progress: 37, overall_status: Upload system configuration to all nodes
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 189, state: InProgress, overall_progress: 42, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 188, state: InProgress, overall_progress: 42, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 187, state: InProgress, overall_progress: 51, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 186, state: InProgress, overall_progress: 51, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 185, state: InProgress, overall_progress: 54, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 184, state: InProgress, overall_progress: 42, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 183, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 182, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 181, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 180, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 179, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 178, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 177, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 176, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 175, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 174, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 173, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 172, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 171, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 170, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 169, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 168, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 167, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 166, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 165, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 164, state: Completed, overall_progress: 100, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.commit: Bootstrap complete.
NdPollInstallStatus.commit: Polling install status until complete. Max retries: 200, interval: 5 seconds.
NdPollInstallStatus.poll_once: Install status: retries 199, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 198, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 197, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 196, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 195, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.login_refresh: Refreshing login. You may see this message multiple times during install polling.
NdPollInstallStatus.login_refresh: Sleeping 10 seconds before attempting re-authentication.
NdPollInstallStatus.login_refresh: Re-authenticated during install polling.
NdPollInstallStatus.poll_once: Install status: retries 193, state: InProgress, overall_progress: 57, overall_status: Deploy Kubernetes stack
NdPollInstallStatus.login_refresh: Refreshing login. You may see this message multiple times during install polling.
NdPollInstallStatus.login_refresh: Sleeping 10 seconds before attempting re-authentication.
NdPollInstallStatus.login_refresh: Retry login refresh due to exception: HTTPSConnectionPool(host='192.168.7.14', port=443): Max retries exceeded with url: /login (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x10a78afd0>: Failed to establish a new connection: [Errno 61] Connection refused'))
NdPollInstallStatus.login_refresh: Retry login refresh due to exception: HTTPSConnectionPool(host='192.168.7.14', port=443): Max retries exceeded with url: /login (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x10a78b250>: Failed to establish a new connection: [Errno 61] Connection refused'))
NdPollInstallStatus.login_refresh: Re-authenticated during install polling.
NdPollInstallStatus.poll_once: Install status: retries 191, state: InProgress, overall_progress: 76, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 190, state: InProgress, overall_progress: 76, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 189, state: InProgress, overall_progress: 76, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 188, state: InProgress, overall_progress: 76, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 187, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 186, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 185, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 184, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 183, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 182, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 181, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 180, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 179, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 178, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 177, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 176, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 175, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 174, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 173, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 172, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 171, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 170, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 169, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 168, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 167, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 166, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 165, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 164, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 163, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 162, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 161, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 160, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 159, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 158, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 157, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 156, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 155, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 154, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 153, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 152, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 151, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 150, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 149, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 148, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 147, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 146, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 145, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 144, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 143, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 142, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 141, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 140, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 139, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 138, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 137, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 136, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 135, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 134, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 133, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 132, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 131, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 130, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 129, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 128, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 127, state: Completed, overall_progress: 100, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.commit: Install complete.
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```

### Example output, with polling enabled, after bootstrap is complete and all services are up/healthy

The following is to show that you can run the script against a fully booted Nexus Dashboard instance with no ill effects.

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode_322m.yaml --poll --retries 200 --interval 5
NdBootstrap.commit: Bootstrapping cluster 'ND14-3' on Nexus Dashboard at 192.168.7.13.
NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.13/24 to serialNumber 94D03F101E9E.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.send_bootstrap_configuration: Sending bootstrap configuration to Nexus Dashboard at https://192.168.7.13/v2/bootstrap/cluster.
NdBootstrap.send_bootstrap_configuration: Bootstrap configuration already sent. Returning.
NdPollBootstrapStatus.commit: Polling bootstrap status until complete. Max retries: 200, interval: 5 seconds.
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 199, state: Completed, overall_progress: 100, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.commit: Bootstrap complete.
NdPollInstallStatus.commit: Polling install status until complete. Max retries: 200, interval: 5 seconds.
NdPollInstallStatus.poll_once: Install status: retries 199, state: Completed, overall_progress: 100, overall_status: Wait for infra services to be ready
NdPollInstallStatus.commit: Install complete.
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```

### Example output (411g), failure due to duplicate IP address assigned to cluster node data network interface

The resolution would be to fix your configuration.  Specifically, the value for `nodes[x].dataNetwork.ipSubnet`

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode_411g.yaml --poll --retries 50 --interval 20
NdBootstrap.commit: Bootstrapping cluster 'ND411g-2' on Nexus Dashboard at 192.168.7.14.
NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.14/24 to serialNumber 6F3CE014936C.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.send_bootstrap_configuration: Sending bootstrap configuration to Nexus Dashboard at https://192.168.7.14/v2/bootstrap/cluster.
NdBootstrap.send_bootstrap_configuration: Cluster bootstrap initiated successfully.
NdPollBootstrapStatus.commit: Polling bootstrap status until complete. Max retries: 50, interval: 20 seconds.
NdPollBootstrapStatus.poll_once: Bootstrap status: state: InProgress, overall_progress: 1, overall_status: Initialize node, retries remaining: 49
NdPollBootstrapStatus.poll_once: Bootstrap status: state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services, retries remaining: 48
NdPollBootstrapStatus.poll_once: Bootstrap status: state: Failed, overall_progress: 100, overall_status: Cluster bring up failed at install stage: 'Duplicate IPs check for nodes data network and external services', please check and retry, retries remaining: 47
NdPollBootstrapStatus.poll_once: Bootstrap encountered an error, exiting. overallProgress: 100, overallStatus: Cluster bring up failed at install stage: 'Duplicate IPs check for nodes data network and external services', please check and retry, state: Failed
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```
