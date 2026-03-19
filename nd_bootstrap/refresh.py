"""
Nexus Dashboard Refresh

Refreshes authentication to Nexus Dashboard and maintains the session.
"""

import inspect
from sys import exit as sys_exit

import requests
import urllib3

from nd_bootstrap.environment import NdEnvironment

# Disable warnings for self-signed certificates (if applicable)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NdRefresh:
    """
    Refresh authentication to Nexus Dashboard and expose the Request Session via a property.

    ## Endpoint

    path: /refresh
    verb: POST

    ## Properties

    - session: (getter) The requests.Session object.

    ## Usage

    ```python
    nd_refresh = NdRefresh()
    nd_refresh.session = existing_session
    nd_refresh.commit()
    ```

    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._session = requests.Session()
        self._session.verify = False
        self._session.headers.update({"Content-Type": "application/json"})
        self.nd_environment = NdEnvironment()
        self._url: str = f"https://{self.nd_environment.nd_ip}/refresh"

    def commit(self) -> None:
        """
        Refresh authentication to Nexus Dashboard and, if successful, set the auth_token.
        If not successful, sys_exit(1) with an error message.
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        response = self._session.post(self._url, timeout=10)
        if response.status_code != 200:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Refresh failed: {response.status_code} : {response.text}"
            print(msg)
            sys_exit(1)

    @property
    def session(self) -> requests.Session:
        """
        getter: return the requests.Session object.
        setter: set and validate the requests.Session object.
        """
        return self._session

    @session.setter
    def session(self, value: requests.Session) -> None:
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        if not isinstance(value, requests.Session):
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.session must be set to a requests.Session object, exiting."
            print(msg)
            sys_exit(1)

        self._session = value
