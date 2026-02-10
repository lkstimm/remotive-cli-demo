# RemotiveLabs CLI Complete Demo Guide

**Created**: 2026-02-10
**Demo Location**: `/Users/lukastimm/RemotiveLabs/remotive-cli-demo/`

## Table of Contents
1. [Overview](#overview)
2. [What You Built](#what-you-built)
3. [Quick Start](#quick-start)
4. [Architecture](#architecture)
5. [Key Learnings](#key-learnings)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

---

## Overview

This demo showcases the RemotiveLabs CLI and broker infrastructure for automotive CAN bus development. It includes:
- Working RemotiveBroker setup (Docker)
- Interactive visualizations showing network topology
- Simulated steering CAN traffic
- Documentation of RemotiveLabs vs demo code boundaries

**Trial Subscription**: Expires 2026-03-10

---

## What You Built

### Directory Structure
```
remotive-cli-demo/
├── broker-setup/
│   ├── docker-compose.yml          # RemotiveBroker Docker configuration
│   └── configuration/
│       ├── interfaces.json         # Virtual CAN bus config
│       └── can/
│           └── steering.dbc        # CAN signal definitions
│
└── steering-demo/
    ├── network_topology_visualizer.py  # Main visualization (with boundary boxes)
    ├── topology_visualizer.py          # Alternate visualization
    ├── steering_visualizer.py          # Simple dual-graph view
    ├── simple_demo.sh                  # Interactive demo launcher
    ├── generate_traffic.sh             # Traffic generator for Wireshark
    ├── ARCHITECTURE.md                 # What's RemotiveLabs vs demo code
    ├── QUICK_START.md                  # Quick reference guide
    └── venv/                           # Python environment
```

### What's Real vs Simulated

**RemotiveLabs Infrastructure (Real):**
- RemotiveCloud - Authentication & subscriptions (cloud service)
- Remotive CLI - Command-line tool (`remotive` command)
- RemotiveBroker - Docker container on localhost:50051
- DBC file format - Industry standard signal definitions

**Demo/Simulation Code:**
- Python visualizers - All three `.py` visualization scripts
- Signal generation - Sine wave math functions (not real sensors)
- ECU simulation - Rate-limited angle tracking (not real hardware)
- Shell scripts - Traffic generation helpers

---

## Quick Start

### 1. Start RemotiveBroker
```bash
cd /Users/lukastimm/RemotiveLabs/remotive-cli-demo/broker-setup
docker compose up -d
```

### 2. Run Visualization
```bash
cd /Users/lukastimm/RemotiveLabs/remotive-cli-demo/steering-demo
source venv/bin/activate
python3 network_topology_visualizer.py
```

### 3. Monitor Traffic (Optional)
```bash
# Terminal 1
cd /Users/lukastimm/RemotiveLabs/remotive-cli-demo/steering-demo
./simple_demo.sh

# Terminal 2
./generate_traffic.sh
```

---

## Architecture

### Network Topology

```
┌─────────────────────────────────────────────────────────┐
│                    DEMO CODE (Simulated)                │
│                                                          │
│  ┌──────────┐                              ┌──────────┐ │
│  │ Gateway  │                              │ Steering │ │
│  │          │                              │   ECU    │ │
│  │ Publishes│                              │Subscribes│ │
│  └────┬─────┘                              └─────┬────┘ │
│       │                                          │      │
└───────┼──────────────────────────────────────────┼──────┘
        │                                          │
        │         ┌────────────────────┐          │
        │         │  REMOTIVELABS      │          │
        │         │  INFRASTRUCTURE    │          │
        │         │                    │          │
        │    ┌────┴─────┐         ┌────┴─────┐   │
        └───→│ CAN Bus  │←───────→│ Remotive │←──┘
             │(Virtual) │         │  Broker  │
             │Steering  │         │localhost │
             │   Bus    │         │  :50051  │
             └──────────┘         └──────────┘
```

### Message Flow

**CAN ID 100 - SteeringCommand**
- Gateway (demo) → CAN Bus → Broker → ECU (demo)
- Blue edges in visualization
- Contains: SteeringAngle, SteeringSpeed

**CAN ID 200 - SteeringStatus**
- ECU (demo) → Broker → CAN Bus → Gateway (demo)
- Red edges in visualization
- Contains: CurrentAngle, ECU_Ready

---

## Key Learnings

### 1. Authentication Flow

RemotiveLabs uses OAuth through RemotiveCloud:

```bash
# Step 1: Login (opens browser)
remotive cloud auth login

# Step 2: Set organization
remotive cloud organizations list
remotive cloud organizations default <org-id>

# Step 3: Start trial (if needed)
remotive topology start-trial
```

**Important**: Credentials stored in `~/.config/remotive/` must be mounted into Docker:
```yaml
volumes:
  - "${HOME}/.config/remotive:/root/.config/remotive:ro"
```

### 2. Docker Networking on macOS

**Problem**: `network_mode: "host"` doesn't work on macOS (Docker runs in VM)

**Solution**: Use explicit port mappings:
```yaml
ports:
  - "50051:50051"  # gRPC
  - "4040:4040"    # Web UI
  - "4000:4000"    # Additional services
```

### 3. Virtual CAN Bus Configuration

Define virtual buses in `interfaces.json`:
```json
{
  "chains": [{
    "namespace": "SteeringBus",
    "type": "virtual"
  }]
}
```

Link to DBC file in `docker-compose.yml`:
```yaml
command: >
  --interfaces_json /configuration/interfaces.json
  --dbc_file steering:/configuration/can/steering.dbc
```

### 4. Visualization Performance

For smooth matplotlib animations on macOS:
- Update interval: 100ms (10 FPS)
- Reduce data points: 50 instead of 100
- Skip frames for expensive operations (edge redrawing every 2 frames)
- Use `blit=False` for complex overlays

```python
MAX_POINTS = 50
UPDATE_INTERVAL = 100

def update(self, frame):
    # Only redraw edges every 2 frames
    if frame % 2 == 0:
        self._draw_animated_edges()
```

### 5. Signal Simulation

Realistic CAN traffic simulation:

```python
def generate_command(self, t):
    """Generate realistic steering command"""
    base = 500 * math.sin(t * 0.5)
    noise = 50 * math.sin(t * 2.3) + 30 * math.sin(t * 3.7)
    return base + noise

def update_ecu(self, command, dt=0.05):
    """Simulate ECU response with lag"""
    diff = self.target_angle - self.current_angle
    max_change = 150 * dt  # Rate limiting
    step = max_change if abs(diff) > max_change else diff
    self.current_angle += step
    return self.current_angle
```

### 6. Monitoring Traffic

RemotiveBroker uses gRPC (HTTP/2) on port 50051:

```bash
# Monitor with tshark (requires sudo on macOS)
sudo tshark -i lo0 -f "tcp port 50051"

# Generate traffic
remotive broker signals list
```

### 7. NetworkX Graph Visualization

Better than manual box drawing:

```python
import networkx as nx

G = nx.DiGraph()
G.add_node('Broker', color='lightgreen', size=4000)
G.add_edge('Gateway', 'Broker', message='Command', color='blue')

pos = {'Broker': (1, 1), 'Gateway': (0, 1)}
nx.draw_networkx_nodes(G, pos, node_color=[...])
nx.draw_networkx_edges(G, pos, edge_color=[...])
```

**Key insight**: Use manual positioning for clarity instead of automatic layouts like `spring_layout()`.

---

## Troubleshooting

### Broker Not Starting

```bash
# Check containers
docker compose ps

# View logs
docker compose logs signal-broker

# Restart
docker compose down
docker compose up -d
```

### Authentication Errors

```bash
# Re-authenticate
remotive cloud auth login

# Verify token
cat ~/.config/remotive/credentials.json

# Check subscription
remotive cloud subscriptions list
```

### Web UI Shows Blank

This is expected on macOS with Docker. The broker is working if:
```bash
remotive broker signals list  # Returns successfully
docker compose logs signal-broker  # Shows "gRPC listening on :50051"
```

### Visualization Laggy

Reduce update rate in the Python script:
```python
UPDATE_INTERVAL = 200  # 5 FPS instead of 10 FPS
MAX_POINTS = 30        # Even fewer data points
```

### Import Errors

```bash
# Recreate virtual environment
cd steering-demo
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install matplotlib networkx numpy
```

### tshark Permission Errors

```bash
# Install ChmodBPF for password-free packet capture
cd /tmp
curl -O https://www.wireshark.org/download/osx/ChmodBPF.dmg
# Install the package, then restart
```

---

## Next Steps

### To Make It Real

Replace simulated data with actual RemotiveBroker communication:

```python
from remotivelabs.broker.sync import SignalCreator, BrokerException

# Connect to broker
broker = SignalCreator("localhost:50051")

# Read signals
angle = broker.read_signal("SteeringBus", "SteeringCommand", "SteeringAngle")

# Publish signals
broker.publish_signal("SteeringBus", "SteeringStatus", "CurrentAngle", angle)
```

### Explore More Features

```bash
# List all CLI commands
remotive --help

# Topology management
remotive topology list
remotive topology info <id>

# Signal operations
remotive broker signals list
remotive broker signals read <signal-name>
remotive broker signals write <signal-name> <value>
```

### Add More CAN Buses

Edit `broker-setup/configuration/interfaces.json`:
```json
{
  "chains": [
    {"namespace": "SteeringBus", "type": "virtual"},
    {"namespace": "PowertrainBus", "type": "virtual"},
    {"namespace": "BodyBus", "type": "virtual"}
  ]
}
```

Create corresponding DBC files and update docker-compose.yml.

---

## Reference Commands

### Docker Management
```bash
cd broker-setup/
docker compose up -d              # Start broker
docker compose down               # Stop broker
docker compose logs -f            # Follow logs
docker compose restart            # Restart services
```

### Remotive CLI
```bash
remotive cloud auth login                    # Authenticate
remotive cloud organizations list            # List orgs
remotive cloud organizations default <id>    # Set default org
remotive topology list                       # List topologies
remotive topology start-trial                # Start trial
remotive broker signals list                 # List signals
```

### Demo Scripts
```bash
cd steering-demo/
source venv/bin/activate                     # Activate Python env
python3 network_topology_visualizer.py       # Main visualization
python3 topology_visualizer.py               # Alternate view
python3 steering_visualizer.py               # Simple view
./simple_demo.sh                             # Interactive demo
./generate_traffic.sh                        # Traffic generator
```

### Monitoring
```bash
sudo tshark -i lo0 -f "tcp port 50051"       # Monitor gRPC traffic
docker stats                                 # Monitor Docker resources
docker compose logs signal-broker            # View broker logs
```

---

## Important Files

### Configuration Files
- `broker-setup/docker-compose.yml` - Broker Docker setup
- `broker-setup/configuration/interfaces.json` - CAN bus definitions
- `broker-setup/configuration/can/steering.dbc` - Signal definitions
- `~/.config/remotive/credentials.json` - Authentication token

### Documentation
- `steering-demo/ARCHITECTURE.md` - RemotiveLabs vs demo boundaries
- `steering-demo/QUICK_START.md` - Two-terminal quick start
- `COMPLETE_GUIDE.md` - This file

### Python Scripts
- `network_topology_visualizer.py` - Full topology with boundary boxes (BEST)
- `topology_visualizer.py` - Topology with manual box layout
- `steering_visualizer.py` - Simple dual-graph view

### Shell Scripts
- `simple_demo.sh` - Interactive CLI demo
- `generate_traffic.sh` - Generate API calls for monitoring

---

## Contact & Support

- **RemotiveLabs Documentation**: https://docs.remotivelabs.com
- **CLI Repository**: Check `remotive --help` for version info
- **Trial Expires**: 2026-03-10
- **Organization**: Check with `remotive cloud organizations list`

---

## Summary

You successfully created a complete RemotiveLabs CLI demo featuring:
✅ Working RemotiveBroker in Docker with authentication
✅ Virtual CAN bus configuration (SteeringBus)
✅ DBC file with steering signals (ID 100, 200)
✅ NetworkX-based topology visualization with boundary boxes
✅ Real-time animated message flow
✅ Clear documentation of real vs simulated components
✅ Traffic monitoring with tshark/Wireshark
✅ Optimized performance (10 FPS, 50 data points)

The demo clearly shows how RemotiveLabs infrastructure (broker + CAN bus) routes messages between simulated ECUs, providing an excellent foundation for understanding automotive CAN bus development.
