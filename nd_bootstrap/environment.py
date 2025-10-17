"""
Nexus Dashboard Environment Configuration

Reads and provides property-based access to ND environment variables.
"""
import inspect
from os import environ
from sys import exit as sys_exit


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
