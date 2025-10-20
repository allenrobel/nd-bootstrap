"""
Nexus Dashboard Login

Handles authentication to Nexus Dashboard and maintains the session.
"""

import inspect

import requests
import urllib3

from nd_bootstrap.environment import NdEnvironment

# Disable warnings for self-signed certificates (if applicable)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
        self._status = False  # True if logged in, False otherwise
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
            self._status = False
        self._status = True

    @property
    def session(self) -> requests.Session:
        """
        getter: return the requests.Session object.
        setter: set and validate the requests.Session object.
        """
        return self._session

    @property
    def status(self) -> bool:
        """
        getter: return the login status.
        """
        return self._status
