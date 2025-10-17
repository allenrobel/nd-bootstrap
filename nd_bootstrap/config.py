"""
Nexus Dashboard Bootstrap Configuration

Loads and validates bootstrap configuration files.
"""

import inspect
from sys import exit as sys_exit

from yaml import safe_load


class NdBootstrapConfig:
    """
    Load and validate a Nexus Dashboard bootstrap configuration file.

    Properties:
        - config: (getter) Returns the configuration dictionary loaded from config_file
        - config_file: (getter/setter) The path to the YAML configuration file
        - nd_cluster_name: (getter) The name of the cluster, retrieved from config_file clusterConfig.name
    """

    def __init__(self) -> None:
        self.class_name: str = self.__class__.__name__
        self._config: dict = {}
        self._config_file: str = ""
        self._nd_cluster_name: str = ""

    def load_config(self) -> None:
        """
        Load and parse a YAML configuration file.

        Args:
            self._config_file: Path to the YAML configuration file

        Sets:
            self._config: Dictionary containing the parsed YAML configuration

        Exits with error message if:
            - the configuration file doesn't exist
            - the YAML file is malformed
            - 'clusterConfig' is not in the configuration
            - 'nodes' is not in the configuration or is empty
            - 'clusterConfig.name' is empty
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""
        if not self._config_file:
            msg = f"{self.class_name}.{method_name}: "
            msg += "instance.config_file must be set before calling instance.load_yaml_config, exiting."
            print(msg)
            sys_exit(1)
        try:
            with open(self._config_file, "r", encoding="utf-8") as config_file:
                self._config = safe_load(config_file)
        except FileNotFoundError:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error: Configuration file '{self._config_file}' not found."
            print(msg)
            sys_exit(1)
        except IOError as e:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error reading configuration file '{self._config_file}': {str(e)}"
            print(msg)
            sys_exit(1)

    def validate_config(self) -> None:
        """
        Validate the loaded configuration.
        """
        method_name: str = inspect.stack()[0][3]
        msg: str = ""

        if "clusterConfig" not in self._config:
            msg = f"{self.class_name}.{method_name}: "
            msg += "'clusterConfig' not found in config, exiting."
            print(msg)
            sys_exit(1)
        if not self._config.get("nodes", []):
            msg = f"{self.class_name}.{method_name}: "
            msg += "No nodes defined in 'config', exiting."
            print(msg)
            sys_exit(1)
        self._nd_cluster_name = self._config["clusterConfig"].get("name", "")
        if not self._nd_cluster_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "'clusterConfig.name' is empty, exiting."
            print(msg)
            sys_exit(1)

    def commit(self) -> None:
        """
        Load and validate the configuration file.
        """
        self.load_config()
        self.validate_config()

    @property
    def config_file(self) -> str:
        """
        getter: return the configuration file path.
        setter: set the configuration file path.
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
        Return the configuration dictionary.

        Returns:
            dict: The configuration dictionary.
        """
        return self._config

    @config.setter
    def config(self, value: dict) -> None:
        if not isinstance(value, dict):
            print("Invalid config: not a dictionary, exiting.")
            sys_exit(1)
        self._config = value

    @property
    def nd_cluster_name(self) -> str:
        """
        Return the cluster name from the configuration.

        Returns:
            str: The cluster name.
        """
        return self._nd_cluster_name
