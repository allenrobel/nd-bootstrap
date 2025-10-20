"""
Nexus Dashboard Install Status Polling

Polls cluster install status.
"""

# pylint: disable=broad-exception-caught

import inspect
import re
from sys import exit as sys_exit
from time import sleep

import requests

from nd_bootstrap.environment import NdEnvironment
from nd_bootstrap.login import NdLogin


class NdPollInstallStatus:
    """
    # Summary

    Poll cluster installation status.

    - If NdPollInstallStatus.poll_once() is called, poll one time and return the overall progress percentage.
    - If NdPollInstallStatus.commit() is called, poll until response.overallProgress == 100, or retries are exhausted.

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
    instance = NdPollInstallStatus()
    instance.session = requests.Session()
    overall_progress = instance.poll_once()
    ```

    ### Poll until overallProgress == 100, or retries are exhausted

    ```python
    instance = NdPollInstallStatus()
    instance.session = requests.Session()
    instance.retries = 50
    instance.interval = 20
    instance.commit()
    ```

    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._interval: int = 10
        self._retries: int = 10
        self._login_attempt_retries: int = 10
        self._last_overall_progress: int = 0
        self._last_overall_status: str = "Unknown"
        self._last_state: str = "Unknown"
        self._session: requests.Session | None = None
        self.nd_environment = NdEnvironment()
        self._url: str = f"https://{self.nd_environment.nd_ip}/clusterstatus/install"

    def login_refresh(self) -> None:
        """
        Refresh the login session.

        Exits if:
            - Unable to re-authenticate after self._login_attempt_retries attempts
        """
        method_name = inspect.stack()[0][3]

        msg = f"{self.class_name}.{method_name}: "
        msg += "Refreshing login. You may see this message multiple times during install polling."
        print(msg)

        nd_login = NdLogin()
        login_counter = 0
        msg = f"{self.class_name}.{method_name}: "
        msg += "Sleeping 10 seconds before attempting re-authentication."
        print(msg)
        sleep(10)
        while nd_login.status is False and login_counter < self._login_attempt_retries:
            login_counter += 1
            try:
                nd_login.commit()
            except Exception as error:
                msg = f"{self.class_name}.{method_name}: "
                if "refused" in str(error):
                    msg += "Connection refused. Retrying login refresh."
                else:
                    msg += f"Retrying login refresh due to exception: {error}"
                print(msg)
            sleep(10)
        if nd_login.status is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Exceeded maximum login attempts during install polling, exiting."
            print(msg)
            sys_exit(1)
        self._session = nd_login.session
        msg = f"{self.class_name}.{method_name}: "
        msg += "Re-authentication successful."
        print(msg)

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

        if self._session is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.session must be set before calling instance.poll_once, exiting."
            print(msg)
            sys_exit(1)

        try:
            response = self._session.get(self._url)
        except requests.RequestException:
            # Attempt to handle network/connection errors
            self.login_refresh()
            return self._last_overall_progress

        # print(f"{self.class_name}.{method_name}: response.status_code: {response.status_code}")
        # print(f"{self.class_name}.{method_name}: response.text: {response.text}")

        if response.status_code == 401:
            self.login_refresh()
            return self._last_overall_progress

        if response.status_code == 404:
            # install will return 404 for a short time (about 20 seconds) after login completes
            # Verify this...
            return self._last_overall_progress

        if response.status_code != 200:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Failed to get install status. status code: {response.status_code}, response.text: {response.text}. "
            print(msg)
            return self._last_overall_progress

        overall_progress: int = response.json().get("overallProgress", self._last_overall_progress)
        overall_status = response.json().get("overallStatus", "Unknown")
        state = response.json().get("state", "Unknown")
        msg = f"{self.class_name}.{method_name}: "
        msg += f"Install status: retries {self._retries}, state: {state}, overall_progress: {overall_progress}, overall_status: {overall_status}"
        print(msg)

        self._last_overall_progress = overall_progress
        self._last_overall_status = overall_status
        self._last_state = state
        # Exit if install failed
        if re.search(r"fail", state, re.IGNORECASE):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Install encountered an error, exiting. "
            msg += f"overallProgress: {self._last_overall_progress}, "
            msg += f"overallStatus: {self._last_overall_status}, "
            msg += f"state: {self._last_state}"
            print(msg)
            sys_exit(1)
        # While self._last_overall_progress will be 100% for failures, we exit above on failure.
        # Hence, self._last_overall_progress will reflect actual progress toward success
        return self._last_overall_progress

    def commit(self) -> None:
        """
        Poll the install status until overallProgress == 100 and overallStatus indicates success.

        Exits if:
            - instance.session is not set

        Returns:
            None
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        if self._session is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.session must be set before calling instance.commit, exiting."
            print(msg)
            sys_exit(1)

        msg = f"{self.class_name}.{method_name}: "
        msg += "Polling install status until complete. "
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
                print(f"{self.class_name}.{method_name}: Install complete.")
                return

            sleep(self._interval)

    @property
    def session(self) -> requests.Session | None:
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
