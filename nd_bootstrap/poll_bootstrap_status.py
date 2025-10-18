"""
Nexus Dashboard Bootstrap Status Polling

Polls cluster bootstrap installation status.
"""

import inspect
from sys import exit as sys_exit
from time import sleep

import requests

from nd_bootstrap.environment import NdEnvironment
from nd_bootstrap.login import NdLogin

class NdPollBootstrapStatus:
    """
    # Summary

    Poll cluster bootstrap status.

    - If NdPollBootstrapStatus.poll_once() is call, poll one time and return the overall progress percentage.
    - If NdPollBootstrapStatus.commit() is called, poll until response.overallProgress == 100, or retries are exhausted.

    ## Endpoint

    Path: /clusterstatus/install
    Verb: GET

    ## Properties

    - session: (getter/setter) The requests.Session object instance with authentication cookies set
    - retries: (getter/setter) The number of retries for polling the install status. Default is 10.
    - interval: The interval in seconds between polling attempts. Default is 10 seconds.

    ## Usage

    ### Poll once

    ```python
    instance = NdPollBootstrapStatus()
    instance.session = requests.Session()
    overall_progress = instance.poll_once()
    ```

    ### Poll until overallProgress == 100, or retries are exhausted

    ```python
    instance = NdPollBootstrapStatus()
    instance.session = requests.Session()
    instance.retries = 10
    instance.interval = 15
    instance.commit()
    ```

    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._interval: int = 10
        self._retries: int = 10
        self._session: requests.Session
        self.nd_environment = NdEnvironment()
        self._url: str = f"https://{self.nd_environment.nd_ip}/clusterstatus/install"

    def poll_once(self) -> int:
        """
        Poll the install status once.

        Exits if:
            - instance.session is not set
        Returns:
            overall_progress: int: The overall progress percentage.
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        if not self._session:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.session must be set before calling instance.poll_once, exiting."
            print(msg)
            sys_exit(1)

        response = self._session.get(self._url)
        if response.status_code not in (200, 401, 404):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Failed to get install status. status code: {response.status_code}, response.text: {response.text}. "
            msg += "Returning 0% overall progress."
            print(msg)
            return 0

        if response.status_code == 404:
            # Bootstrap will return 404 for a short time (about 20 seconds) after login completes
            return 0

        if response.status_code == 401:
            nd_login = NdLogin()
            nd_login.commit()
            self._session = nd_login.session
            msg = f"{self.class_name}.{method_name}: "
            msg += "Re-authenticated during bootstrap polling.  Returning 0% overall progress."
            print(msg)
            return 0

        overall_progress: int = response.json().get("overallProgress", 0)
        return overall_progress

    def commit(self) -> None:
        """
        Poll the install status until overallProgress == 100.

        Exits if:
            - instance.session is not set

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

        msg = f"{self.class_name}.{method_name}: "
        msg += "Polling bootstrap status until complete. "
        msg += f"Max retries: {self._retries}, interval: {self._interval} seconds."
        print(msg)

        while True:
            self._retries -= 1
            if self._retries <= 0:
                msg = f"{self.class_name}.{method_name}: "
                msg += "Exceeded maximum retries. Returning."
                print(msg)
                return

            overall_progress = self.poll_once()

            if overall_progress == 100:
                print(f"{self.class_name}.{method_name}: Bootstrap complete.")
                return

            print(f"{self.class_name}.{method_name}: Bootstrap in progress... {overall_progress}%, retries remaining: {self._retries}")
            sleep(self._interval)

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
    def retries(self) -> int:
        """
        getter: return the number of retries.
        setter: set and validate the number of retries.
        """
        return self._retries

    @retries.setter
    def retries(self, value: int) -> None:
        if not isinstance(value, int):
            print("Invalid retries: not an int, exiting.")
            sys_exit(1)
        self._retries = value

    @property
    def interval(self) -> int:
        """
        getter: return the polling interval in seconds.
        setter: set and validate the polling interval in seconds.
        """
        return self._interval

    @interval.setter
    def interval(self, value: int) -> None:
        if not isinstance(value, int):
            print("Invalid interval: not an int, exiting.")
            sys_exit(1)
        self._interval = value
