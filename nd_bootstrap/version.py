"""
Nexus Dashboard Version Detection

Retrieves the firmware version from a Nexus Dashboard instance.
"""

import inspect
from sys import exit as sys_exit

import requests

from nd_bootstrap.environment import NdEnvironment


class NdVersion:
    """
    Retrieve the firmware version from Nexus Dashboard.

    ## Endpoint

    - Path: /v2/bootstrap/syscfg
    - Verb: GET

    ## Properties

    - firmware_version: (getter) The firmware version string after commit()
    - session: (getter/setter) The requests.Session object instance with authentication cookies set

    ## Usage

    ```python
    instance = NdVersion()
    instance.session = configured_requests_session_instance
    instance.commit()
    print(instance.firmware_version)  # e.g. "4.2.1.10"
    ```
    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._firmware_version: str = ""
        self._session: requests.Session
        self.nd_environment = NdEnvironment()

    def commit(self) -> None:
        """
        Retrieve the firmware version from Nexus Dashboard.

        Exits if:
            - instance.session is not set
            - The GET request fails
            - FirmwareVersion is not found in the response

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

        url = f"https://{self.nd_environment.nd_ip}/v2/bootstrap/syscfg"
        try:
            response = self._session.get(
                url,
                timeout=60,
            )
        except requests.RequestException as e:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error retrieving firmware version: {str(e)}"
            print(msg)
            sys_exit(1)

        if response.status_code not in [200]:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Failed to retrieve firmware version. Status code: {response.status_code} : {response.text}"
            print(msg)
            sys_exit(1)

        data = response.json()
        self._firmware_version = data.get("FirmwareVersion", "")
        if not self._firmware_version:
            msg = f"{self.class_name}.{method_name}: "
            msg += "FirmwareVersion not found in response."
            print(msg)
            sys_exit(1)

        msg = f"{self.class_name}.{method_name}: "
        msg += f"Detected ND firmware version: {self._firmware_version}"
        print(msg)

    @property
    def firmware_version(self) -> str:
        """
        getter: return the firmware version string.
        """
        return self._firmware_version

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
