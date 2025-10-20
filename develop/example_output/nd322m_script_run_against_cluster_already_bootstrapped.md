# Example output, with polling enabled, after bootstrap is complete and all services are up/healthy

The following is to show that you can run the script against a fully booted Nexus Dashboard instance with no ill effects.

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode_322m.yaml --poll --retries 200 --interval 5
NdBootstrap.commit: Bootstrapping cluster 'ND14-3' on Nexus Dashboard at 192.168.7.13.
NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.13/24 to serialNumber 94D03F101E9E.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.send_bootstrap_configuration: Sending bootstrap configuration to Nexus Dashboard at https://192.168.7.13/v2/bootstrap/cluster.
NdBootstrap.send_bootstrap_configuration: Bootstrap configuration already sent. Returning.
NdPollBootstrapStatus.commit: Polling bootstrap status until complete. Max retries: 200, interval: 5 seconds.
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 199, state: Completed, overall_progress: 100, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.commit: Bootstrap complete.
NdPollInstallStatus.commit: Polling install status until complete. Max retries: 200, interval: 5 seconds.
NdPollInstallStatus.poll_once: Install status: retries 199, state: Completed, overall_progress: 100, overall_status: Wait for infra services to be ready
NdPollInstallStatus.commit: Install complete.
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```
