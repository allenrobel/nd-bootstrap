# Example output (411g), failure due to duplicate IP address assigned to cluster node data network interface

The resolution would be to fix your configuration.  Specifically, the value for `nodes[x].dataNetwork.ipSubnet`

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode_411g.yaml --poll --retries 50 --interval 20
NdBootstrap.commit: Bootstrapping cluster 'ND411g-2' on Nexus Dashboard at 192.168.7.14.
NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.14/24 to serialNumber 6F3CE014936C.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.send_bootstrap_configuration: Sending bootstrap configuration to Nexus Dashboard at https://192.168.7.14/v2/bootstrap/cluster.
NdBootstrap.send_bootstrap_configuration: Cluster bootstrap initiated successfully.
NdPollBootstrapStatus.commit: Polling bootstrap status until complete. Max retries: 50, interval: 20 seconds.
NdPollBootstrapStatus.poll_once: Bootstrap status: state: InProgress, overall_progress: 1, overall_status: Initialize node, retries remaining: 49
NdPollBootstrapStatus.poll_once: Bootstrap status: state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services, retries remaining: 48
NdPollBootstrapStatus.poll_once: Bootstrap status: state: Failed, overall_progress: 100, overall_status: Cluster bring up failed at install stage: 'Duplicate IPs check for nodes data network and external services', please check and retry, retries remaining: 47
NdPollBootstrapStatus.poll_once: Bootstrap encountered an error, exiting. overallProgress: 100, overallStatus: Cluster bring up failed at install stage: 'Duplicate IPs check for nodes data network and external services', please check and retry, state: Failed
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```
