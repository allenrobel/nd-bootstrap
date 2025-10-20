# Example output (411g), successful bootstrap

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode_411g.yaml --poll --retries 200 --interval 5
NdBootstrap.commit: Bootstrapping cluster 'ND411g-2' on Nexus Dashboard at 192.168.7.14.
NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.14/24 to serialNumber 7290C46C15AB.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.send_bootstrap_configuration: Sending bootstrap configuration to Nexus Dashboard at https://192.168.7.14/v2/bootstrap/cluster.
NdBootstrap.send_bootstrap_configuration: Cluster bootstrap initiated successfully.
NdPollBootstrapStatus.commit: Polling bootstrap status until complete. Max retries: 200, interval: 5 seconds.
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 199, state: InProgress, overall_progress: 1, overall_status: Initialize node
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 198, state: InProgress, overall_progress: 1, overall_status: Initialize node
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 197, state: InProgress, overall_progress: 1, overall_status: Initialize node
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 196, state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 195, state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 194, state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 193, state: InProgress, overall_progress: 25, overall_status: Duplicate IPs check for nodes data network and external services
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 192, state: InProgress, overall_progress: 32, overall_status: Setup boot time configuration
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 191, state: InProgress, overall_progress: 37, overall_status: Upload system configuration to all nodes
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 190, state: InProgress, overall_progress: 37, overall_status: Upload system configuration to all nodes
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 189, state: InProgress, overall_progress: 42, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 188, state: InProgress, overall_progress: 42, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 187, state: InProgress, overall_progress: 51, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 186, state: InProgress, overall_progress: 51, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 185, state: InProgress, overall_progress: 54, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 184, state: InProgress, overall_progress: 42, overall_status: Execute cluster validation tests
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 183, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 182, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 181, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 180, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 179, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 178, state: InProgress, overall_progress: 54, overall_status: Admit nodes to cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 177, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 176, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 175, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 174, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 173, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 172, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 171, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 170, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 169, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 168, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 167, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 166, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 165, state: InProgress, overall_progress: 59, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 164, state: Completed, overall_progress: 100, overall_status: Bootstrap Kubernetes cluster
NdPollBootstrapStatus.commit: Bootstrap complete.
NdPollInstallStatus.commit: Polling install status until complete. Max retries: 200, interval: 5 seconds.
NdPollInstallStatus.poll_once: Install status: retries 199, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 198, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 197, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 196, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 195, state: InProgress, overall_progress: 39, overall_status: Deploy base infrastructure services
NdPollInstallStatus.login_refresh: Refreshing login. You may see this message multiple times during install polling.
NdPollInstallStatus.login_refresh: Sleeping 10 seconds before attempting re-authentication.
NdPollInstallStatus.login_refresh: Re-authenticated during install polling.
NdPollInstallStatus.poll_once: Install status: retries 193, state: InProgress, overall_progress: 57, overall_status: Deploy Kubernetes stack
NdPollInstallStatus.login_refresh: Refreshing login. You may see this message multiple times during install polling.
NdPollInstallStatus.login_refresh: Sleeping 10 seconds before attempting re-authentication.
NdPollInstallStatus.login_refresh: Retry login refresh due to exception: HTTPSConnectionPool(host='192.168.7.14', port=443): Max retries exceeded with url: /login (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x10a78afd0>: Failed to establish a new connection: [Errno 61] Connection refused'))
NdPollInstallStatus.login_refresh: Retry login refresh due to exception: HTTPSConnectionPool(host='192.168.7.14', port=443): Max retries exceeded with url: /login (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x10a78b250>: Failed to establish a new connection: [Errno 61] Connection refused'))
NdPollInstallStatus.login_refresh: Re-authenticated during install polling.
NdPollInstallStatus.poll_once: Install status: retries 191, state: InProgress, overall_progress: 76, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 190, state: InProgress, overall_progress: 76, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 189, state: InProgress, overall_progress: 76, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 188, state: InProgress, overall_progress: 76, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 187, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 186, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 185, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 184, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 183, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 182, state: InProgress, overall_progress: 79, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 181, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 180, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 179, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 178, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 177, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 176, state: InProgress, overall_progress: 82, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 175, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 174, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 173, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 172, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 171, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 170, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 169, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 168, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 167, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 166, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 165, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 164, state: InProgress, overall_progress: 89, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 163, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 162, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 161, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 160, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 159, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 158, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 157, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 156, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 155, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 154, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 153, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 152, state: InProgress, overall_progress: 91, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 151, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 150, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 149, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 148, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 147, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 146, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 145, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 144, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 143, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 142, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 141, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 140, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 139, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 138, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 137, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 136, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 135, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 134, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 133, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 132, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 131, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 130, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 129, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 128, state: InProgress, overall_progress: 97, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.poll_once: Install status: retries 127, state: Completed, overall_progress: 100, overall_status: Deploy ND core infrastructure services
NdPollInstallStatus.commit: Install complete.
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```
