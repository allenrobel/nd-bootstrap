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
./nd_bootstrap.py path/to/bootstrap.yaml [--dry-run]
export ND_PASSWORD=MyPassword
export ND_USERNAME=admin
```

"""
# pylint: disable=too-many-instance-attributes,line-too-long
import argparse
import inspect
import json
from os import environ
from sys import exit as sys_exit

import requests
import urllib3
from yaml import safe_load

# Disable warnings for self-signed certificates (if applicable)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO: Add class NdVersion to retrieve and expose Nexus Dashboard version information
# Version JSON
# https://192.168.7.13/version.json
# GET
# Response:
# {
#     "commit_id": "07a8f967",
#     "build_time": "now",
#     "build_host": "kube14",
#     "user": "root",
#     "product_id": "nd",
#     "product_name": "Nexus Dashboard",
#     "release": false,
#     "major": 3,
#     "minor": 2,
#     "maintenance": 2,
#     "patch": "m"
# }


class NdEnvironment:
    """
    # Summary

    Read the environment variables below for Nexus Dashboard and provide property access.

    - ND_DOMAIN: The domain for Nexus Dashboard authentication. Default is "local".
    - ND_IP_PROTOCOL: The preferred IP protocol to use, either "IP4" or "IP6". Default is "IP4".
    - ND_IP4: The IPv4 address of the Nexus Dashboard
    - ND_IP6: The IPv6 address of the Nexus Dashboard
    - ND_PASSWORD: The password for Nexus Dashboard authentication
    - ND_USERNAME: The username for Nexus Dashboard authentication

    ## Properties

    - nd_domain: The domain for Nexus Dashboard authentication. Default is "local".
    - nd_ip: The IP address of the Nexus Dashboard, based on the preferred IP protocol.
    - nd_ip_protocol: The preferred IP protocol, either "IP4" or "IP6". Default is "IP4".
    - nd_ip4: The IPv4 address of the Nexus Dashboard.
    - nd_ip6: The IPv6 address of the Nexus Dashboard.
    - nd_password: The password for Nexus Dashboard authentication.
    - nd_username: The username for Nexus Dashboard authentication.

    ## Usage

    ```python
    nd_env = NdEnvironment()
    print(nd_env.nd_ip)  # Prints the IP address based on ND_IP_PROTOCOL
    print(nd_env.nd_username)  # Prints the username
    # etc...
    ```
    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._nd_domain: str = environ.get("ND_DOMAIN", "local")
        self._nd_ip: str = ""
        self._nd_ip_protocol: str = environ.get("ND_IP_PROTOCOL", "IP4")  # IP4 or IP6
        self._nd_ip4: str = environ.get("ND_IP4", "")
        self._nd_ip6: str = environ.get("ND_IP6", "")
        self._nd_password: str = environ.get("ND_PASSWORD", "")
        self._nd_username: str = environ.get("ND_USERNAME", "")

    @property
    def nd_domain(self) -> str:
        """
        Return the Nexus Dashboard domain.

        Returns:
            str: The domain for Nexus Dashboard authentication. Defaults to "local".
        """
        return self._nd_domain

    @property
    def nd_ip(self) -> str:
        """
        Return the Nexus Dashboard IPv4 or IPv6 address, based on the preferred IP protocol.

        Returns:
            str: The IP address of the Nexus Dashboard.

        Exits with error message if:
            - ND_IP_PROTOCOL is not set to "IP4" or "IP6"
            - ND_IP_PROTOCOL is "IP4" but ND_IP4 is not set
            - ND_IP_PROTOCOL is "IP6" but ND_IP6 is not set
        """
        method_name: str = inspect.stack()[0][3]
        if self._nd_ip_protocol == "IP4":
            if not self._nd_ip4:
                msg = f"{self.class_name}.{method_name}: "
                msg += "ND_IP_PROTOCOL is set to IP4 but ND_IP4 environment variable is not set"
                print(msg)
                sys_exit(1)
            return self._nd_ip4
        if self._nd_ip_protocol == "IP6":
            if not self._nd_ip6:
                msg = f"{self.class_name}.{method_name}: "
                msg += "ND_IP_PROTOCOL is set to IP6 but ND_IP6 environment variable is not set"
                print(msg)
                sys_exit(1)
            return self._nd_ip6
        msg = f"{self.class_name}.{method_name}: "
        msg += f"Invalid ND_IP_PROTOCOL '{self._nd_ip_protocol}', must be 'IP4' or 'IP6'"
        print(msg)
        sys_exit(1)

    @property
    def nd_ip_protocol(self) -> str:
        """
        Retrieve ND_IP_PROTOCOL.

        Returns:
            str: The preferred IP protocol, either "IP4" or "IP6". Defaults to "IP4".
        """
        return self._nd_ip_protocol

    @property
    def nd_ip4(self) -> str:
        """
        Return the Nexus Dashboard IPv4 address.

        Returns:
            str: The IPv4 address of the Nexus Dashboard.
        """
        return self._nd_ip4

    @property
    def nd_ip6(self) -> str:
        """
        Return the Nexus Dashboard IPv6 address.

        Returns:
            str: The IPv6 address of the Nexus Dashboard.
        """
        return self._nd_ip6

    @property
    def nd_password(self) -> str:
        """
        Return the Nexus Dashboard password.

        Returns:
            str: The password for Nexus Dashboard authentication.

        Exits with error message if:
            - ND_PASSWORD is not set
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""
        if not self._nd_password:
            msg = f"{self.class_name}.{method_name}: "
            msg += "ND_PASSWORD environment variable not set"
            print(msg)
            sys_exit(1)
        return self._nd_password

    @property
    def nd_username(self) -> str:
        """
        Return the Nexus Dashboard username.

        Returns:
            str: The username for Nexus Dashboard authentication.

        Exits with error message if:
            - ND_USERNAME is not set
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""
        if not self._nd_username:
            msg = f"{self.class_name}.{method_name}: "
            msg += "ND_USERNAME environment variable not set"
            print(msg)
            sys_exit(1)
        return self._nd_username

class NdLogin:
    """
    Login to Nexus Dashboard and expose the Request Session via a property.

    ## Endpoint

    path: /login
    verb: POST

    ## Properties

    - session: (getter) The requests.Session object.

    ## Usage

    ```python
    nd_login = NdLogin()
    nd_login.commit()
    session = nd_login.session
    ```

    """
    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._session = requests.Session()
        self._session.verify = False
        self._session.headers.update({"Content-Type": "application/json"})
        self.nd_environment = NdEnvironment()
        self._url: str = f"https://{self.nd_environment.nd_ip}/login"

        self._payload: dict[str, str] = {
            "domain": self.nd_environment.nd_domain,
            "userName": self.nd_environment.nd_username,
            "userPasswd": self.nd_environment.nd_password,
        }

    def commit(self) -> None:
        """
        Login to Nexus Dashboard and, if successful, set the auth_token.
        If not successful, sys_exit(1) with an error message.
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""


        response = self._session.post(self._url, json=self._payload, timeout=10)
        if response.status_code != 200:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Authentication failed: {response.status_code} : {response.text}"
            print(msg)
            sys_exit(1)

    @property
    def session(self) -> requests.Session:
        """
        getter: return the requests.Session object.
        setter: set and validate the requests.Session object.
        """
        return self._session


class NdBootstrapConfig:
    """
    Load and validate a Nexus Dashboard bootstrap configuration file.

    Properties:
        - config: (getter) Returns the configuration dictionary loaded from config_file
        - config_file: (getter/setter) The path to the YAML configuration file
        - nd_cluster_name: (getter) The name of the cluster, retrieved from config_file clusterConfig.name
    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._config: dict = {}
        self._config_file: str = ""
        self._nd_cluster_name: str = ""

    def load_config(self) -> None:
        """
        Load and parse a YAML configuration file.

        Args:
            self._config_file: Path to the YAML configuration file

        Sets:
            self._config: Dictionary containing the parsed YAML configuration

        Exits with error message if:
            - the configuration file doesn't exist
            - the YAML file is malformed
            - 'clusterConfig' is not in the configuration
            - 'nodes' is not in the configuration or is empty
            - 'clusterConfig.name' is empty
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""
        if not self._config_file:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.config_file must be set before calling instance.load_yaml_config, exiting."
            print(msg)
            sys_exit(1)
        try:
            with open(self._config_file, "r", encoding="utf-8") as config_file:
                self._config = safe_load(config_file)
        except FileNotFoundError:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error: Configuration file '{self._config_file}' not found."
            print(msg)
            sys_exit(1)
        except IOError as e:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error reading configuration file '{self._config_file}': {str(e)}"
            print(msg)
            sys_exit(1)

    def validate_config(self) -> None:
        """
        Validate the loaded configuration.
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        if "clusterConfig" not in self._config:
            msg = f"{self.class_name}.{method_name}: "
            msg += "'clusterConfig' not found in config, exiting."
            print(msg)
            sys_exit(1)
        if not self._config.get("nodes", []):
            msg = f"{self.class_name}.{method_name}: "
            msg += "No nodes defined in 'config', exiting."
            print(msg)
            sys_exit(1)
        self._nd_cluster_name = self._config["clusterConfig"].get("name", "")
        if not self._nd_cluster_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "'clusterConfig.name' is empty, exiting."
            print(msg)
            sys_exit(1)

    def commit(self) -> None:
        """
        Load and validate the configuration file.
        """
        self.load_config()
        self.validate_config()

    @property
    def config_file(self) -> str:
        """
        getter: return the configuration file path.
        setter: set the configuration file path.
        """
        return self._config_file

    @config_file.setter
    def config_file(self, value: str) -> None:
        if not value or not isinstance(value, str):
            print("Invalid config_file: empty or not a string, exiting.")
            sys_exit(1)
        self._config_file = value

    @property
    def config(self) -> dict:
        """
        Return the configuration dictionary.

        Returns:
            dict: The configuration dictionary.
        """
        return self._config

    @config.setter
    def config(self, value: dict) -> None:
        if not isinstance(value, dict):
            print("Invalid config: not a dictionary, exiting.")
            sys_exit(1)
        self._config = value

    @property
    def nd_cluster_name(self) -> str:
        """
        Return the cluster name from the configuration.

        Returns:
            str: The cluster name.
        """
        return self._nd_cluster_name


class NdNtpServersValidate:
    """
    Validate Nexus Dashboard reachability and compatibility with the NTP servers in `config`.

    ## Endpoint

    - Path: /v2/bootstrap/verifyntp
    - Verb: POST

    ## Properties

    - config: (getter/setter) The configuration dictionary containing clusterConfig.ntpConfig.servers
    - session: (getter/setter) The requests.Session object instance with authentication cookies set

    ## Usage

    ```python
    instance = NdNtpServersValidate()
    instance.session = configured_requests_session_instance
    instance.config = your_nd_bootstrap_configuration_dict
    instance.commit()  # Validates the NTP servers, exits on failure
    ```
    """
    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._config: dict = {}
        self._session: requests.Session
        self.nd_environment = NdEnvironment()

    def commit(self) -> None:
        """
        Validate the NTP servers in the configuration.

        Exits if:
            - instance.session is not set
            - instance.config is not set
            - instance.config contains no NTP servers
            - validation fails for one or more NTP servers

        Returns:
            None
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        if not self._session:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.session must be set before calling instance.commit, exiting."
            print(msg)
            sys_exit(1)
        if not self._config:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.config must be set before calling instance.commit, exiting."
            print(msg)
            sys_exit(1)

        ntp_servers = (
            self._config.get("clusterConfig", {})
            .get("ntpConfig", {})
            .get("servers", [])
        )
        if not ntp_servers:
            msg = f"{self.class_name}.{method_name}: "
            msg += "At least one NTP server must be specified in the configuration. Exiting."
            print(msg)
            sys_exit(1)

        url = f"https://{self.nd_environment.nd_ip}/v2/bootstrap/verifyntp"
        payload = {
            "nameServers": [server["host"] for server in ntp_servers],
            "ntpConfig": {
                "servers": [
                    {"host": server["host"], "prefer": server["prefer"]}
                    for server in ntp_servers
                ],
                "keys": [],
            },
        }
        response = self._session.post(
            url,
            json=payload,
            timeout=60,
        )
        if response.status_code not in [200]:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"NTP servers validation failed with status code {response.status_code}, response.text: {response.text}"
            print(msg)
            sys_exit(1)

        result = set()
        for server in response.json():
            #  response.json() -> [{"name":"192.168.7.6","error":"","info":"valid"}]
            name = server.get("name", "") or "UNKNOWN"
            error = server.get("error", "") or "NONE"
            info = server.get("info", "")
            if error != "NONE" or info != "valid":
                result.add((name, error, info))
        if not result:
            msg = f"{self.class_name}.{method_name}: "
            msg += "NTP servers validation succeeded."
            print(msg)
            return
        msg = f"{self.class_name}.{method_name}: "
        msg += "NTP servers validation failed. "
        msg += f"Status Code: {response.status_code}. "
        msg += f"Response: {response.text}.\n"
        msg += f"Invalid NTP servers: {result}"
        print(msg)
        sys_exit(1)

    @property
    def session(self) -> requests.Session:
        """
        getter: return the authentication cookie dictionary.
        setter: set and validate the authentication cookie dictionary.
        """
        return self._session
    @session.setter
    def session(self, value: requests.Session) -> None:
        if not isinstance(value, requests.Session):
            print("Invalid session: not a requests.Session instance, exiting.")
            sys_exit(1)
        self._session = value

    @property
    def config(self) -> dict:
        """
        getter: return the configuration dictionary.
        setter: set and validate the configuration dictionary.
        """
        return self._config
    @config.setter
    def config(self, value: dict) -> None:
        if not isinstance(value, dict):
            print("Invalid config: not a dictionary, exiting.")
            sys_exit(1)
        self._config = value

class NdBootstrap:
    """
    Bootstrap a Nexus Dashboard cluster.
    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._auth_cookie: dict[str, str] = {}
        self._auth_token: str = ""
        self._cluster_name: str = ""
        self._config: dict = {}
        self._config_file: str = ""
        self._dry_run: bool = False
        self._headers: dict[str, str] = {"Content-Type": "application/json"}
        self.nd_bootstrap_config = NdBootstrapConfig()
        self.nd_environment = NdEnvironment()
        self.ntp_servers_validate = NdNtpServersValidate()
        self._nd_login = NdLogin()
        self._nd_login.commit()
        self.session = self._nd_login.session


    def update_node_serial_numbers(self) -> None:
        """
        Update self._config.nodes[<index>].serialNumber for each node in the configuration dictionary by retrieving cluster
        information from Nexus Dashboard and matching self._config.nodes[<index>].managementNetwork.ipSubnet with the
        corresponding response.nodes.<index>.managementNetwork.ipSubnet and updating self._config.nodes[<index>].serialNumber
        with response.nodes[<index>].serialNumber.

        ## Endpoint

        Path: /v2/bootstrap/cluster
        Verb: GET
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        url = f"https://{self.nd_environment.nd_ip}/v2/bootstrap/cluster"
        try:
            response = self.session.get(
                url,
                headers=self._headers,
                cookies=self._auth_cookie,
                verify=False,
                timeout=10,
            )
        except requests.RequestException as e:
            msg  = f"{self.class_name}.{method_name}: "
            msg += f"Error retrieving serial numbers: {str(e)}"
            print(msg)
            sys_exit(1)

        if response.status_code not in (200, 201):
            msg  = f"{self.class_name}.{method_name}: "
            msg += f"Failed to retrieve serial numbers. Status code: {response.status_code} : {response.text}"
            print(msg)
            sys_exit(1)

        data = response.json()
        nodes_info = data.get("nodes", [])
        if not nodes_info:
            msg  = f"{self.class_name}.{method_name}: "
            msg += "No nodes found in the response."
            print(msg)
            sys_exit(1)

        for node in self._config.get("nodes", []):
            mgmt_ip_subnet = node.get("managementNetwork", {}).get("ipSubnet", "")
            if not mgmt_ip_subnet:
                msg  = f"{self.class_name}.{method_name}: "
                msg += "Node managementNetwork.ipSubnet is missing or empty."
                print(msg)
                sys_exit(1)

            matched_node = next(
                (
                    n
                    for n in nodes_info
                    if n.get("managementNetwork", {}).get("ipSubnet", "")
                    == mgmt_ip_subnet
                ),
                None,
            )
            if not matched_node:
                msg  = f"{self.class_name}.{method_name}: "
                msg += f"No matching node found for managementNetwork.ipSubnet {mgmt_ip_subnet}."
                print(msg)
                sys_exit(1)

            serial_number = matched_node.get("serialNumber", "")
            if not serial_number:
                msg  = f"{self.class_name}.{method_name}: "
                msg += f"Matched node for managementNetwork.ipSubnet {mgmt_ip_subnet} has no serialNumber."
                print(msg)
                sys_exit(1)
            node["serialNumber"] = serial_number
            msg  = f"{self.class_name}.{method_name}: "
            msg += f"Updated node with managementNetwork.ipSubnet {mgmt_ip_subnet} to serialNumber {serial_number}."
            print(msg)

    def update_node_credentials(self) -> None:
        """
        Update the nodeController credentials (if any) in the configuration dictionary.

        Args:
            config: The configuration dictionary to update.
            nd_username: The username to set for each nodeController.
            nd_password: The password to set for each nodeController.
        """
        for node in self._config.get("nodes", []):
            if "nodeController" not in node:
                continue
            if "loginUser" in node["nodeController"]:
                if node["nodeController"]["loginUser"] == "ND_USERNAME":
                    node["nodeController"][
                        "loginUser"
                    ] = self.nd_environment.nd_username
            if "loginPassword" in node["nodeController"]:
                if node["nodeController"]["loginPassword"] == "ND_PASSWORD":
                    node["nodeController"][
                        "loginPassword"
                    ] = self.nd_environment.nd_password

    def post_bootstrap_configuration(self) -> None:
        """
        Post the bootstrap configuration to the specified URL.

        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        url = f"https://{self.nd_environment.nd_ip}/v2/bootstrap/cluster"

        if self.dry_run:
            msg = f"{self.class_name}.{method_name}: "
            msg += "DRY RUN: Skipping POST to cluster bootstrap endpoint.\n"
            msg += f"Would POST the following configuration to {url} if --dry_run were not set:\n"
            msg += f"{json.dumps(self._config, indent=4)}"
            print(msg)
            sys_exit(0)

        msg = f"{self.class_name}.{method_name}: "
        msg += f"Posting bootstrap configuration to Nexus Dashboard at {url}.\n"
        print(msg)

        try:
            response = self.session.post(
                url,
                json=self._config,
                timeout=300,
            )
        except requests.RequestException as e:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error sending POST request for cluster bootstrap: "
            msg += f"Error detail: {str(e)}"
            print(msg)
        if response.status_code in (200, 201):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Cluster bootstrap initiated successfully.\n"
            msg += f"Response: {response.json()}"
            print(msg)
        else:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Failed to bootstrap cluster. Status code: {response.status_code} : {response.text}"
            print(msg)

    def commit(self) -> None:
        """
        Commit the changes by loading the YAML config, updating node credentials, and
        posting the bootstrap configuration.
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        if not self.session:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.session must be set before calling instance.commit, exiting."
            print(msg)
            sys_exit(1)
        if not self.config_file:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.config_file must be set before calling instance.commit, exiting."
            print(msg)
            sys_exit(1)

        self.nd_bootstrap_config.config_file = self.config_file
        self.nd_bootstrap_config.commit()
        self._config = self.nd_bootstrap_config.config

        self.update_node_credentials()

        msg = f"{self.class_name}.{method_name}: "
        msg += f"Bootstrapping cluster '{self.nd_bootstrap_config.nd_cluster_name}' "
        msg += f"on Nexus Dashboard at {self.nd_environment.nd_ip}.\n"
        print(msg)
        self.update_node_serial_numbers()

        self.ntp_servers_validate.session = self.session
        self.ntp_servers_validate.config = self._config
        self.ntp_servers_validate.commit()

        # POST the Bootstrap JSON
        self.post_bootstrap_configuration()

    @property
    def config_file(self) -> str:
        """
        getter: return the configuration file path.
        setter: set the configuration file path.
        """
        return self._config_file

    @config_file.setter
    def config_file(self, value: str) -> None:
        if not value or not isinstance(value, str):
            print("Invalid config_file: empty or not a string, exiting.")
            sys_exit(1)
        self._config_file = value

    @property
    def config(self) -> dict:
        """
        getter: return the configuration dictionary.
        setter: set and validate the configuration dictionary.
        """
        return self._config

    @property
    def dry_run(self) -> bool:
        """
        getter: return the dry_run flag.
        setter: set the dry_run flag.
        """
        return self._dry_run

    @dry_run.setter
    def dry_run(self, value: bool) -> None:
        if not isinstance(value, bool):
            print("Invalid dry_run: not a boolean, exiting.")
            sys_exit(1)
        self._dry_run = value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bootstrap ND cluster from YAML configuration"
    )
    parser.add_argument("config_file", help="Path to the YAML configuration file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform all validation steps but skip the final POST to bootstrap the cluster",
    )
    args = parser.parse_args()

    instance = NdBootstrap()
    instance.config_file = args.config_file
    instance.dry_run = args.dry_run
    instance.commit()
