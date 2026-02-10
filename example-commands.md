# Remotive CLI Example Commands

This file contains copy-paste ready commands for exploring the Remotive CLI.

## Basic Information

```bash
# Show CLI version
remotive --version

# Show help
remotive --help

# Show topology version
remotive topology version
```

## Interactive Exploration

```bash
# Launch the Text User Interface (RECOMMENDED for beginners)
remotive tui

# Install tab completion for your shell
remotive --install-completion
```

## Topology Commands

```bash
# Check subscription status
remotive topology subscription status

# Start a trial subscription
remotive topology start-trial

# List workspaces
remotive topology workspace list

# Show topology help
remotive topology --help

# Validate a topology file (example)
# remotive topology validate <path-to-file>

# Show information from a database file (example)
# remotive topology show <path-to-db-file>
```

## Broker Commands

```bash
# Discover brokers on the network
remotive broker discover

# Show broker help
remotive broker --help

# View license information (requires broker connection)
remotive broker license info

# List signals (requires running broker)
remotive broker signals list

# Discover signals with pattern (requires running broker)
# remotive broker signals list --pattern "vehicle*"
```

## Broker with Custom URL

```bash
# Connect to a specific broker
remotive broker --url http://your-broker-url:50051 license info

# Or set environment variable
export REMOTIVE_BROKER_URL=http://your-broker-url:50051
remotive broker license info
```

## Cloud Commands

```bash
# Show cloud help
remotive cloud --help

# List cloud resources (requires authentication)
# remotive cloud list
```

## Recording and Playback

```bash
# Show playback options
remotive broker playback --help

# Show recording options
remotive broker record --help

# List recording sessions
# remotive broker playback list
```

## File Operations

```bash
# Show file operations help
remotive broker files --help

# Upload/download configurations and recordings
# remotive broker files upload <local-path>
# remotive broker files download <remote-path>
```

## Tools

```bash
# Show available tools
remotive tools --help
```

## Advanced Examples

### Working with Signals

```bash
# List all signals
remotive broker signals list

# Search for specific signals
remotive broker signals list --pattern "speed"

# Subscribe to signals (interactive mode)
remotive broker signals subscribe
```

### Recording Session Management

```bash
# List recording sessions
remotive topology recording-session list

# Show recording session details
# remotive topology recording-session show <session-id>
```

### Export Operations

```bash
# Show export options
remotive broker export --help

# Export data in different formats
# remotive broker export <format> <source>
```

## Tips

1. Always use `--help` to see available options for any command
2. The TUI (`remotive tui`) is the easiest way to explore
3. Set `REMOTIVE_BROKER_URL` environment variable to avoid typing `--url` repeatedly
4. Use tab completion after installing it with `remotive --install-completion`
5. Most commands require either a local broker running or connection to a cloud broker

## Environment Setup

```bash
# Set default broker URL
export REMOTIVE_BROKER_URL=http://localhost:50051

# Set topology workspace
export REMOTIVE_TOPOLOGY_WORKSPACE=/path/to/workspace

# Choose container engine (docker or podman)
export CONTAINER_ENGINE=docker
```

## Common Workflows

### Workflow 1: First Time Setup
```bash
remotive --version
remotive topology version
remotive topology subscription status
remotive topology start-trial  # if needed
```

### Workflow 2: Discover and Connect to Broker
```bash
remotive broker discover
export REMOTIVE_BROKER_URL=<discovered-broker-url>
remotive broker license info
remotive broker signals list
```

### Workflow 3: Work with Recordings
```bash
remotive broker record --help
remotive broker playback list
# Start recording, then playback
```
