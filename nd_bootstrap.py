#!/usr/bin/env python
"""
# Summary

Bootstrap a Nexus Dashboard cluster.

## Features

- Supports both IPv4 and IPv6 connectivity to Nexus Dashboard
- Uses environment variables for Nexus Dashboard connection and authentication
  - More secure than hardcoding credentials in the configuration file
  - Easier to integrate with CI/CD pipelines and secret management systems
  - Easier to use with shell scripts and automation tools
- Loads and validates a YAML configuration file
- Validates NTP servers are reachable and compatible from Nexus Dashboard's perspective prior to POST
- Retrieves node credentials from environment variables and dynamically updates the node configurations prior to POST
  - More secure and flexible than hardcoding credentials in the configuration file
- Retrieves node serial numbers from Nexus Dashboard and dynamically updates the node configurations prior to POST
  - No need to manually specify serial numbers in the configuration file
- Supports a --dry-run flag to perform all validation steps but skip the final POST to bootstrap the cluster
- Posts the configuration to Nexus Dashboard after the terminal-based bringup is complete
- Modular design with classes for environment, login, configuration, NTP validation, and bootstrapping
- Uses requests library for HTTP interactions
- Uses PyYAML for YAML parsing
- Includes detailed error handling and informative messages

## Environment Variables

- ND_IP4: The IPv4 address of the Nexus Dashboard
- ND_IP6: The IPv6 address of the Nexus Dashboard
- ND_IP_PROTOCOL: The IP protocol to use, either "IP4" or "IP6". Default is "IP4".
- ND_USERNAME: The username to authenticate with Nexus Dashboard
- ND_PASSWORD: The password to authenticate with Nexus Dashboard
- ND_DOMAIN: The domain to authenticate with Nexus Dashboard. Default is "local".

## Usage Example

Set the environment variables as shown below, then run the script with the path to your
YAML configuration file.

Optionally use the --dry-run flag to validate the configuration, and NTP servers, without
posting the configuration.

```bash
# optional, defaults to local
export ND_DOMAIN=local
# optional preferred IP protocol, defaults to IP4
export ND_IP_PROTOCOL=IP4
export ND_IP4=192.168.1.1
# optional, (mandatory if ND_IP_PROTOCOL is set to IP6)
export ND_IP6=2001:db8::1
export ND_USERNAME=admin
export ND_PASSWORD=MyPassword
./nd_bootstrap.py path/to/bootstrap.yaml [--dry-run]
```

"""
import argparse

from nd_bootstrap.bootstrap import NdBootstrap

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap ND cluster from YAML configuration")
    parser.add_argument("config_file", help="Path to the YAML configuration file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform all validation steps but skip the final POST to bootstrap the cluster",
    )
    parser.add_argument(
        "--poll-status",
        action="store_true",
        help="Poll the bootstrap and services bringup status until both are complete. Ignored if --dry-run is set",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=10,
        help="Number of retries for polling the status (bootstrap and services). Ignored if --poll-status is not set or --dry-run is set",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Interval (in seconds) between polling attempts. Ignored if --poll-status is not set or --dry-run is set",
    )
    args = parser.parse_args()

    instance = NdBootstrap()
    instance.config_file = args.config_file
    instance.dry_run = args.dry_run
    instance.poll = args.poll_status
    instance.retries = args.retries
    instance.interval = args.interval
    instance.commit()
