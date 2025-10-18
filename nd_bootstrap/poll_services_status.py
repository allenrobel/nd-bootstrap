"""
Nexus Dashboard Services Status Polling

Polls service packages operational status after bootstrap installation.
"""

# pylint: disable=too-many-locals

import inspect
from sys import exit as sys_exit
from time import sleep

import requests

from nd_bootstrap.environment import NdEnvironment


class NdPollServicesStatus:
    """
    # Summary

    Poll service packages status after bootstrap installation.

    - If NdPollServicesStatus.poll_once() is called, poll one time and return the current status.
    - If NdPollServicesStatus.commit() is called, poll until services are healthy, or retries are exhausted.

    ## Endpoint

    Path: /api/v1/release/servicepackages
    Verb: GET

    ## Polling Logic

    The class waits for:
    1. items[0].status.operState.timeStamp to be non-null (operState.state field will be missing while timestamp is null)
    2. items[0].status.operState.state == "Healthy"
    3. items[0].status.deploymentState.state == "Enabled"
    4. items[0].status.installState.state == "Installed"

    ## Properties

    - session: (getter/setter) The requests.Session object instance with authentication cookies set
    - retries: (getter/setter) The number of retries for polling the services status. Default is 30.
    - interval: (getter/setter) The interval in seconds between polling attempts. Default is 20 seconds.

    ## Usage

    ### Poll once

    ```python
    instance = NdPollServicesStatus()
    instance.session = requests.Session()
    status_info = instance.poll_once()
    print(f"Deployment state: {status_info['deployment_state']}")
    print(f"Operational state: {status_info['oper_state']}")
    print(f"Timestamp: {status_info['timestamp']}")
    ```

    ### Poll until services are healthy, or retries are exhausted

    ```python
    instance = NdPollServicesStatus()
    instance.session = requests.Session()
    instance.retries = 50
    instance.interval = 30
    instance.commit()
    ```

    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._interval: int = 20
        self._retries: int = 30
        self._session: requests.Session
        self.nd_environment = NdEnvironment()
        self._url: str = f"https://{self.nd_environment.nd_ip}/api/v1/release/servicepackages"

    def poll_once(self) -> dict:
        """
        Poll the services status once.

        Exits if:
            - instance.session is not set
        Returns:
            status_info: dict: A dictionary containing:
                - deployment_state: str or None
                - oper_state: str or None
                - timestamp: str or None
                - install_state: str or None
                - is_ready: bool True if services are ready
                  - operState.timeStamp is non-null
                  - operState.state == "Healthy"
                  - deploymentState.state == "Enabled"
                  - installState.state == "Installed"
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        if not self._session:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.session must be set before calling instance.poll_once, exiting."
            print(msg)
            sys_exit(1)

        response = self._session.get(self._url)
        if response.status_code != 200:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Failed to get services status. status code: {response.status_code}, response.text: {response.text}. "
            msg += "Returning empty status."
            print(msg)
            return {
                "deployment_state": None,
                "oper_state": None,
                "timestamp": None,
                "install_state": None,
                "is_ready": False,
            }

        try:
            response_data = response.json()
            items = response_data.get("items", [])
            if not items:
                msg = f"{self.class_name}.{method_name}: "
                msg += "No service packages found in response."
                print(msg)
                return {
                    "deployment_state": None,
                    "oper_state": None,
                    "timestamp": None,
                    "install_state": None,
                    "is_ready": False,
                }

            status = items[0].get("status", {})
            oper_state_obj = status.get("operState", {})
            deployment_state_obj = status.get("deploymentState", {})
            install_state_obj = status.get("installState", {})

            timestamp = oper_state_obj.get("timeStamp")
            oper_state = oper_state_obj.get("state")
            deployment_state = deployment_state_obj.get("state")
            install_state = install_state_obj.get("state")

            # Check if services are ready:
            # 1. operState.timeStamp must be non-null
            # 2. operState.state must be "Healthy"
            # 3. deployment_state must be "Enabled"
            # 4. install_state must be "Installed"
            is_ready = timestamp is not None and oper_state == "Healthy" and deployment_state == "Enabled" and install_state == "Installed"

            return {
                "deployment_state": deployment_state,
                "oper_state": oper_state,
                "timestamp": timestamp,
                "install_state": install_state,
                "is_ready": is_ready,
            }
        except (ValueError, KeyError, IndexError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error parsing response: {error}. Returning empty status."
            print(msg)
            return {
                "deployment_state": None,
                "oper_state": None,
                "timestamp": None,
                "install_state": None,
                "is_ready": False,
            }

    def commit(self) -> None:
        """
        Poll the services status until they are healthy.

        Exits if:
            - instance.session is not set

        Success criteria:
            - items[0].status.operState.timeStamp is non-null
            - items[0].status.operState.state == "Healthy"

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
        msg += "Polling services status until healthy. "
        msg += f"Max retries: {self._retries}, interval: {self._interval} seconds."
        print(msg)

        while True:
            self._retries -= 1
            if self._retries <= 0:
                msg = f"{self.class_name}.{method_name}: "
                msg += "Exceeded maximum retries. Returning."
                print(msg)
                return

            status_info = self.poll_once()

            # Check if services are ready
            if status_info["is_ready"]:
                msg = f"{self.class_name}.{method_name}: Services are healthy. "
                msg += f"operState: {status_info['oper_state']}, "
                msg += f"deploymentState: {status_info['deployment_state']}, "
                msg += f"timestamp: {status_info['timestamp']}"
                print(msg)
                return

            # Print progress
            deployment_state = status_info["deployment_state"] or "Unknown"
            oper_state = status_info["oper_state"] or "Not available"
            timestamp = status_info["timestamp"]

            if timestamp is None:
                msg = f"{self.class_name}.{method_name}: Waiting for operState timestamp... "
                msg += f"deploymentState: {deployment_state}, retries remaining: {self._retries}"
            else:
                msg = f"{self.class_name}.{method_name}: Waiting for services to become healthy... "
                msg += f"operState: {oper_state}, deploymentState: {deployment_state}, retries remaining: {self._retries}"
            print(msg)
            sleep(self._interval)

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
