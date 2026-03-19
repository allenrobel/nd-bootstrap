"""
Nexus Dashboard Remote Services Validation

Validates DNS and NTP server reachability for ND 4.2+ using the combined endpoint.
"""

import inspect
from sys import exit as sys_exit

import requests

from nd_bootstrap.environment import NdEnvironment


class NdVerifyRemoteServices:
    """
    Validate Nexus Dashboard reachability and compatibility with DNS and NTP servers in `config`.

    Used for ND 4.2+ which replaces the separate NTP validation endpoint with a combined one.

    ## Endpoint

    - Path: /bootstrap/verifyremoteservices
    - Verb: POST

    ## Properties

    - config: (getter/setter) The configuration dictionary containing clusterConfig
    - session: (getter/setter) The requests.Session object instance with authentication cookies set

    ## Usage

    ```python
    instance = NdVerifyRemoteServices()
    instance.session = configured_requests_session_instance
    instance.config = your_nd_bootstrap_configuration_dict
    instance.commit()  # Validates DNS and NTP servers, exits on failure
    ```
    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._config: dict = {}
        self._session: requests.Session
        self.nd_environment = NdEnvironment()

    def commit(self) -> None:
        """
        Validate the DNS and NTP servers in the configuration.

        Exits if:
            - instance.session is not set
            - instance.config is not set
            - instance.config contains no DNS servers
            - instance.config contains no NTP servers
            - validation fails

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

        name_servers = self._config.get("clusterConfig", {}).get("nameServers", [])
        if not name_servers:
            msg = f"{self.class_name}.{method_name}: "
            msg += "At least one DNS server must be specified in clusterConfig.nameServers. Exiting."
            print(msg)
            sys_exit(1)

        ntp_servers = self._config.get("clusterConfig", {}).get("ntpConfig", {}).get("servers", [])
        if not ntp_servers:
            msg = f"{self.class_name}.{method_name}: "
            msg += "At least one NTP server must be specified in clusterConfig.ntpConfig.servers. Exiting."
            print(msg)
            sys_exit(1)

        url = f"https://{self.nd_environment.nd_ip}/bootstrap/verifyremoteservices"
        payload = {
            "nameServers": name_servers,
            "ntpConfig": {
                "servers": [{"host": server["host"], "prefer": server["prefer"]} for server in ntp_servers],
            },
        }
        try:
            response = self._session.post(
                url,
                json=payload,
                timeout=60,
            )
        except requests.RequestException as e:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error validating remote services: {str(e)}"
            print(msg)
            sys_exit(1)

        if response.status_code not in [200]:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Remote services validation failed with status code {response.status_code}, response.text: {response.text}"
            print(msg)
            sys_exit(1)

        msg = f"{self.class_name}.{method_name}: "
        msg += "Remote services (DNS + NTP) validation succeeded."
        print(msg)

    @property
    def session(self) -> requests.Session:
        """
        getter: return the requests.Session instance.
        setter: set and validate the requests.Session instance.
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
