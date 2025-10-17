"""
Nexus Dashboard Bootstrap Orchestrator

Main class that orchestrates the complete bootstrap workflow.
"""

import inspect
import json
from sys import exit as sys_exit

import requests

from nd_bootstrap.config import NdBootstrapConfig
from nd_bootstrap.environment import NdEnvironment
from nd_bootstrap.login import NdLogin
from nd_bootstrap.ntp import NdNtpServersValidate
from nd_bootstrap.status import NdPollBootstrapStatus


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
        self._interval: int = 10
        self._retries: int = 10
        self._poll: bool = True  # Whether to poll the bootstrap status after posting the configuration
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
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error retrieving serial numbers: {str(e)}"
            print(msg)
            sys_exit(1)

        if response.status_code not in (200, 201):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Failed to retrieve serial numbers. Status code: {response.status_code} : {response.text}"
            print(msg)
            sys_exit(1)

        data = response.json()
        nodes_info = data.get("nodes", [])
        if not nodes_info:
            msg = f"{self.class_name}.{method_name}: "
            msg += "No nodes found in the response."
            print(msg)
            sys_exit(1)

        for node in self._config.get("nodes", []):
            mgmt_ip_subnet = node.get("managementNetwork", {}).get("ipSubnet", "")
            if not mgmt_ip_subnet:
                msg = f"{self.class_name}.{method_name}: "
                msg += "Node managementNetwork.ipSubnet is missing or empty."
                print(msg)
                sys_exit(1)

            matched_node = next(
                (n for n in nodes_info if n.get("managementNetwork", {}).get("ipSubnet", "") == mgmt_ip_subnet),
                None,
            )
            if not matched_node:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"No matching node found for managementNetwork.ipSubnet {mgmt_ip_subnet}."
                print(msg)
                sys_exit(1)

            serial_number = matched_node.get("serialNumber", "")
            if not serial_number:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Matched node for managementNetwork.ipSubnet {mgmt_ip_subnet} has no serialNumber."
                print(msg)
                sys_exit(1)
            node["serialNumber"] = serial_number
            msg = f"{self.class_name}.{method_name}: "
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
                    node["nodeController"]["loginUser"] = self.nd_environment.nd_username
            if "loginPassword" in node["nodeController"]:
                if node["nodeController"]["loginPassword"] == "ND_PASSWORD":
                    node["nodeController"]["loginPassword"] = self.nd_environment.nd_password

    def send_bootstrap_configuration(self) -> None:
        """
        # Summary

        Send the bootstrap configuration to the specified URL.

        ## Endpoint

        - Path: /v2/bootstrap/cluster
        - Verb: POST

        ## Exits if:

        - self.dry_run is True (after printing the configuration that would be sent)

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
        msg += f"Sending bootstrap configuration to Nexus Dashboard at {url}.\n"
        print(msg)

        try:
            response = self.session.post(
                url,
                json=self._config,
                timeout=300,
            )
        except requests.RequestException as e:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error sending POST request for cluster bootstrap: "
            msg += f"Error detail: {str(e)}"
            print(msg)
        if response.status_code in (200, 201):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Cluster bootstrap initiated successfully.\n"
            msg += f"Response: {response.text}"
            print(msg)
        else:
            if response.status_code == 405:
                msg = f"{self.class_name}.{method_name}: "
                msg += "Bootstrap configuration already sent. Returning..."
                print(msg)
                return
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

        # Return if cluster is already bootstrapped
        nd_install_status = NdPollBootstrapStatus()
        nd_install_status.session = self.session
        percent_complete = nd_install_status.poll_once()
        if percent_complete == 100:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Cluster '{self.nd_bootstrap_config.nd_cluster_name}' is already bootstrapped."
            print(msg)
            return

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
        self.send_bootstrap_configuration()

        if self.poll:
            nd_install_status.retries = self.retries
            nd_install_status.interval = self.interval
            nd_install_status.commit()

    @property
    def config_file(self) -> str:
        """
        The bootstrap configuration file path.

        - getter: return the configuration file path.
        - setter: set the configuration file path.
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
        The bootstrap configuration dictionary.

        - getter: return the configuration dictionary.
        - setter: set and validate the configuration dictionary.
        """
        return self._config

    @property
    def dry_run(self) -> bool:
        """
        If true, perform all validation steps but skip the final POST to bootstrap the cluster.

        - getter: return the dry_run flag.
        - setter: set the dry_run flag.
        """
        return self._dry_run

    @dry_run.setter
    def dry_run(self, value: bool) -> None:
        if not isinstance(value, bool):
            print("Invalid dry_run: not a boolean, exiting.")
            sys_exit(1)
        self._dry_run = value

    @property
    def interval(self) -> int:
        """
        The polling interval in seconds.

        - getter: return the polling interval in seconds.
        - setter: set and validate the polling interval in seconds.
        """
        return self._interval

    @interval.setter
    def interval(self, value: int) -> None:
        if not isinstance(value, int):
            print("Invalid interval: not an int, exiting.")
            sys_exit(1)
        self._interval = value

    @property
    def poll(self) -> bool:
        """
        If true, poll the installation status after posting the bootstrap configuration.

        - getter: return the poll flag.
        - setter: set the poll flag.
        """
        return self._poll

    @poll.setter
    def poll(self, value: bool) -> None:
        if not isinstance(value, bool):
            print("Invalid poll: not a boolean, exiting.")
            sys_exit(1)
        self._poll = value

    @property
    def retries(self) -> int:
        """
        The number of retries for polling the installation status.

        - getter: return the number of retries.
        - setter: set and validate the number of retries.
        """
        return self._retries

    @retries.setter
    def retries(self, value: int) -> None:
        if not isinstance(value, int):
            print("Invalid retries: not an int, exiting.")
            sys_exit(1)
        self._retries = value
