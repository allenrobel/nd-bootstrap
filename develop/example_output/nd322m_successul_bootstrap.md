# ND 3.2(2)m (322m), successful bootstrap

```text
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap % ./nd_bootstrap.py nd_bootstrap_vnode_322m.yaml --poll --retries 200 --interval 5
NdBootstrap.commit: Bootstrapping cluster 'ND14-3' on Nexus Dashboard at 192.168.7.13.
NdBootstrap.update_node_serial_numbers: Updated node with managementNetwork.ipSubnet 192.168.7.13/24 to serialNumber 94D03F101E9E.
NdNtpServersValidate.commit: NTP servers validation succeeded.
NdBootstrap.send_bootstrap_configuration: Sending bootstrap configuration to Nexus Dashboard at https://192.168.7.13/v2/bootstrap/cluster.
NdBootstrap.send_bootstrap_configuration: Cluster bootstrap initiated successfully.
NdPollBootstrapStatus.commit: Polling bootstrap status until complete. Max retries: 200, interval: 5 seconds.
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 199, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 198, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 197, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 196, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 195, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 194, state: InProgress, overall_progress: 13, overall_status: Setup Security
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 193, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 192, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 191, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 190, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 189, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 188, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 187, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 186, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 185, state: InProgress, overall_progress: 50, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.poll_once: Bootstrap status: retries: 184, state: Completed, overall_progress: 100, overall_status: Bootstrap Kubernetes Cluster
NdPollBootstrapStatus.commit: Bootstrap complete.
NdPollInstallStatus.commit: Polling install status until complete. Max retries: 200, interval: 5 seconds.
NdPollInstallStatus.poll_once: Install status: retries 199, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 198, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 197, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 196, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 195, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.poll_once: Install status: retries 194, state: InProgress, overall_progress: 17, overall_status: Deploy Base System Services
NdPollInstallStatus.login_refresh: Refreshing login. You may see this message multiple times during install polling.
NdPollInstallStatus.login_refresh: Sleeping 10 seconds before attempting re-authentication.
NdPollInstallStatus.login_refresh: Re-authentication successful.
NdPollInstallStatus.poll_once: Install status: retries 192, state: InProgress, overall_progress: 28, overall_status: Setup ND Cluster
NdPollInstallStatus.poll_once: Install status: retries 191, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 190, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 189, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 188, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 187, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 186, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 185, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 184, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 183, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 182, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 181, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 180, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 179, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 178, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 177, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 176, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 175, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 174, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 173, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 172, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 171, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 170, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 169, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 168, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 167, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 166, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 165, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 164, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 163, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 162, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 161, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 160, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 159, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 158, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 157, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 156, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 155, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 154, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 153, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 152, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 151, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 150, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 149, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 148, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 147, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 146, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 145, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 144, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 143, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 142, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 141, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 140, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 139, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 138, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 137, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 136, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 135, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 134, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 133, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 132, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 131, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 130, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 129, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 128, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 127, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 126, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 125, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 124, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 123, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 122, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 121, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 120, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 119, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 118, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 117, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 116, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 115, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 114, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 113, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 112, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 111, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 110, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 109, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 108, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 107, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 106, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 105, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 104, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 103, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 102, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 101, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 100, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 99, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 98, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 97, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 96, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 95, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 94, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 93, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 92, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 91, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 90, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 89, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 88, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 87, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 86, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 85, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 84, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 83, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 82, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 81, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 80, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 79, state: InProgress, overall_progress: 32, overall_status: Deploy ND Core Infra Services
NdPollInstallStatus.poll_once: Install status: retries 78, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 77, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 76, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 75, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 74, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 73, state: InProgress, overall_progress: 99, overall_status: Wait for infra services to be ready
NdPollInstallStatus.poll_once: Install status: retries 72, state: Completed, overall_progress: 100, overall_status: Wait for infra services to be ready
NdPollInstallStatus.commit: Install complete.
(nd-bootstrap) arobel@Allen-M4 nd-bootstrap %
```
