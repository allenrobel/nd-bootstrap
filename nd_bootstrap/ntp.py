"""
Nexus Dashboard NTP Server Validation

Validates NTP server reachability and compatibility.
"""
import inspect
from sys import exit as sys_exit

import requests

from nd_bootstrap.environment import NdEnvironment


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

        ntp_servers = self._config.get("clusterConfig", {}).get("ntpConfig", {}).get("servers", [])
        if not ntp_servers:
            msg = f"{self.class_name}.{method_name}: "
            msg += "At least one NTP server must be specified in the configuration. Exiting."
            print(msg)
            sys_exit(1)

        url = f"https://{self.nd_environment.nd_ip}/v2/bootstrap/verifyntp"
        payload = {
            "nameServers": [server["host"] for server in ntp_servers],
            "ntpConfig": {
                "servers": [{"host": server["host"], "prefer": server["prefer"]} for server in ntp_servers],
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
