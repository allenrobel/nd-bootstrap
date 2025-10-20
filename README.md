# Summary

Bootstrap a Nexus Dashboard cluster.

## Features

- Supports IPv4 connectivity to Nexus Dashboard and ready for IPv6 if/when ND bootstrap supports it.
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
  - Example configuration files provided for ND versions 3.2(2)m and 4.1(1)g
- Validates that NTP servers are reachable and compatible from Nexus Dashboard's perspective prior to POST
- Retrieves node credentials from environment variables and dynamically updates the node configurations prior to POST
  - More secure and flexible than hardcoding credentials in the configuration file
- Retrieves node serial numbers from Nexus Dashboard and dynamically updates the node configurations prior to POST
  - No need to manually specify serial numbers in the configuration file
- Supports a `--dry-run` flag to perform all validation steps but skip the request to bootstrap the cluster
- Supports a `--poll-status` flag to poll for both bootstrap and services installation completion before exiting
  - polling behavior can be controlled with `--retries` and `--interval` flags
    - Default `--retries` is 100
    - Default `--interval` is 10 seconds
    - `--retries` and `--interval` are reset for each polling phase (bootstrap polling and install polling), hence:
      - Bootstrap polling timeout is 1000 seconds by default (100 x 10)
      - Install polling timeout is 1000 seconds by default (100 x 10)
- Posts the configuration to Nexus Dashboard after the terminal-based bringup is complete
  - That is, the CLI-based initial setup must still be performed manually to set the password, IP address, and gateway
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

### 1. Repository setup

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

### 2. Separately, perform initial manual CLI-based Nexus Dashboard setup

- Set the password
- Set the IPv4 address with mask e.g. 192.168.7.14/24
- Set the gateway e.g. 192.168.7.1

### 3. Set the environment variables used by this script as shown below

Note, these could be set in a shell script tailored to a specific Nexus Dashboard instance, and collections
of these scripts built up for your various Nexus Dashboard instances.

Nexus Dashboard bootstrap currently supports IPv4 only.

```bash
# optional, defaults to local
export ND_DOMAIN=local
# optional preferred IP protocol, defaults to IP4
export ND_IP_PROTOCOL=IP4
export ND_IP4=192.168.1.14
# optional, (mandatory if ND_IP_PROTOCOL is set to IP6)
export ND_IP6=2001:db8::1
export ND_PASSWORD=MyPassword
export ND_USERNAME=admin
```

### 4. Run the script with --dry-run to validate the configuration

Optionally use the `--dry-run` flag to validate the configuration, NTP server compatibility, and reachability, without
posting the configuration.

```bash
cd $HOME/repos/nd-bootstrap
./nd_bootstrap.py nd_bootstrap_322m_vnode.yaml --dry-run
```

### 5. Run the script without --dry-run to post the configuration to Nexus Dashboard and poll for bootstrap and services install completion

```bash
cd $HOME/repos/nd-bootstrap
./nd_bootstrap.py nd_bootstrap_322m_vnode.yaml --poll-status --retries 200 --interval 5
```

### Example script output

For example script output, see the files in [develop/example_output](https://github.com/allenrobel/nd-bootstrap/tree/main/develop/example_output).
