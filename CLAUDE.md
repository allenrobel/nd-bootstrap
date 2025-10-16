# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python script that bootstraps a Cisco Nexus Dashboard cluster using REST APIs. The script authenticates to an existing Nexus Dashboard instance, validates configuration, performs pre-flight checks (NTP server validation), and then posts the bootstrap configuration to create a cluster.

## Architecture

The codebase follows a class-based architecture with single-responsibility classes:

- **NdEnvironment**: Reads environment variables (ND_IP4, ND_IP6, ND_USERNAME, ND_PASSWORD, ND_DOMAIN, ND_IP_PROTOCOL) and provides property-based access with validation
- **NdLogin**: Authenticates to Nexus Dashboard via `/login` endpoint and maintains a requests.Session object
- **NdBootstrapConfig**: Loads and validates the YAML configuration file containing cluster and node definitions
- **NdNtpServersValidate**: Pre-flight validation of NTP servers using `/v2/bootstrap/verifyntp` endpoint
- **NdBootstrap**: Orchestrates the entire bootstrap workflow by composing the above classes

### Key Workflow (NdBootstrap.commit)

1. Load and validate YAML configuration
2. Update node credentials from environment variables (if nodes use "ND_USERNAME" or "ND_PASSWORD" placeholders)
3. Fetch node serial numbers from ND and match them to nodes in config by managementNetwork.ipSubnet
4. Validate NTP servers can be reached from ND
5. POST bootstrap configuration to `/v2/bootstrap/cluster` (or skip if --dry-run)

### Environment Variables Required

All ND connection details are provided via environment variables for security:

- `ND_USERNAME`, `ND_PASSWORD`: Authentication credentials
- `ND_IP4` or `ND_IP6`: IP address of ND instance
- `ND_IP_PROTOCOL`: Either "IP4" (default) or "IP6"
- `ND_DOMAIN`: Authentication domain (default: "local")

## Development Commands

### Running the script

```bash
# Set required environment variables first
export ND_USERNAME=admin
export ND_PASSWORD=YourPassword
export ND_IP4=192.168.1.1

# Run with a YAML config file
./nd_bootstrap.py path/to/config.yaml

# Dry run (validate only, skip POST)
./nd_bootstrap.py path/to/config.yaml --dry-run
```

### Dependencies

This project uses `uv` for dependency management. Install dependencies with:

```bash
# Install runtime dependencies only
uv sync

# Install with development dependencies (linters, type checkers)
uv sync --extra dev
```

Or run directly with:

```bash
uv run nd_bootstrap.py path/to/config.yaml
```

### Linting and Formatting

All linters are configured for 180 character line length in `pyproject.toml`.

```bash
# Format code with black
uv run black nd_bootstrap.py

# Sort imports with isort
uv run isort nd_bootstrap.py

# Run pylint
uv run pylint nd_bootstrap.py

# Run type checking with mypy
uv run mypy nd_bootstrap.py

# Run all linters (example script)
uv run black nd_bootstrap.py && \
uv run isort nd_bootstrap.py && \
uv run pylint nd_bootstrap.py && \
uv run mypy nd_bootstrap.py
```

## Configuration File Structure

The YAML configuration file (see `nd_bootstrap_vnode.yaml` for example) contains:

- `clusterConfig`: Cluster-level settings including NTP servers, DNS, network ranges, deployment mode
- `nodes`: Array of node definitions with management/data network configs, hostnames, roles, and optional nodeController credentials

## Important Implementation Details

- All classes use `sys_exit(1)` on validation failures rather than exceptions
- The script disables SSL warnings (`urllib3.disable_warnings`) for self-signed certificates
- Serial numbers are dynamically retrieved from ND and matched to config nodes by managementNetwork.ipSubnet
- Node credentials can use "ND_USERNAME" and "ND_PASSWORD" as placeholders that get replaced with environment variable values
- The requests.Session object is passed between classes to maintain authentication state
