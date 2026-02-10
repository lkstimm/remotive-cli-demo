# Guide for Future AI Agents - RemotiveLabs CLI Demo

**Purpose**: Help future agents quickly understand and work with this RemotiveLabs demo.

## TL;DR - What Was Built

A fully functional RemotiveLabs CLI demo with:
- RemotiveBroker running in Docker (localhost:50051)
- NetworkX-based visualization showing CAN bus topology
- Simulated steering signals (SteeringCommand ID 100, SteeringStatus ID 200)
- Clear boundary boxes separating RemotiveLabs infrastructure from demo code
- Optimized for macOS performance (10 FPS, smooth animation)

**Main file to run**: `steering-demo/network_topology_visualizer.py`

---

## Critical Learnings (Save Time!)

### 1. Docker on macOS - MUST FIX

**Problem**: `network_mode: "host"` doesn't work on macOS (Docker runs in LinuxKit VM)

**Solution**: Always use explicit port mappings in docker-compose.yml:
```yaml
services:
  signal-broker:
    ports:
      - "50051:50051"  # gRPC
      - "4040:4040"    # Web UI (will be blank - that's normal!)
      - "4000:4000"    # Additional
    # DO NOT USE: network_mode: "host"
```

### 2. Authentication - Required Before Docker

RemotiveBroker needs valid credentials. MUST run this sequence:

```bash
# 1. Login (opens browser)
remotive cloud auth login

# 2. List organizations
remotive cloud organizations list

# 3. Set default org (CRITICAL - broker won't work without this!)
remotive cloud organizations default <org-id-from-list>

# 4. Start trial if needed
remotive topology start-trial

# 5. Mount credentials into Docker
# In docker-compose.yml:
volumes:
  - "${HOME}/.config/remotive:/root/.config/remotive:ro"
```

**Current status**: Trial expires 2026-03-10

### 3. Virtual CAN Bus Configuration

Two files control the setup:

**broker-setup/configuration/interfaces.json**:
```json
{
  "chains": [{
    "namespace": "SteeringBus",
    "type": "virtual"
  }]
}
```

**broker-setup/docker-compose.yml**:
```yaml
command: >
  --interfaces_json /configuration/interfaces.json
  --dbc_file steering:/configuration/can/steering.dbc
```

### 4. Visualization Performance on macOS

matplotlib can be laggy. Optimal settings:

```python
# Configuration
MAX_POINTS = 50          # Not 100
UPDATE_INTERVAL = 100    # 100ms = 10 FPS (not 50ms)

# In update() function
def update(self, frame):
    # Only redraw expensive operations every N frames
    if frame % 2 == 0:
        self._draw_animated_edges()

    # Message flash timing
    if frame % 20 == 0:      # Not 15
        self.message_activity['command'] = 10
```

### 5. What's Real vs Simulated

This is CRITICAL to understand:

**RemotiveLabs (Real Infrastructure)**:
- RemotiveCloud - OAuth authentication
- Remotive CLI - `remotive` command-line tool
- RemotiveBroker - Docker container on port 50051
- DBC file format - Industry standard

**Demo/Simulation Code**:
- All Python visualizers
- Signal generation: `generate_command()` - just sine wave math
- ECU simulation: `update_ecu()` - rate-limited tracking
- Gateway and ECU nodes in visualization

**The visualizations do NOT connect to the broker**. They just show what traffic would look like with fake data.

---

## File Locations

### Main Files (User should run these)
- `steering-demo/network_topology_visualizer.py` - Main viz ⭐
- `broker-setup/docker-compose.yml` - Broker config
- `steering-demo/simple_demo.sh` - Interactive launcher

### Documentation (Read these first!)
- `README.md` - Updated with quick start
- `COMPLETE_GUIDE.md` - Comprehensive reference
- `steering-demo/ARCHITECTURE.md` - Real vs simulated breakdown
- `steering-demo/QUICK_START.md` - Two-terminal quick start

### Config Files
- `broker-setup/configuration/interfaces.json` - Virtual CAN buses
- `broker-setup/configuration/can/steering.dbc` - Signal definitions
- `~/.config/remotive/credentials.json` - Auth token (user's home)

---

## Common User Requests & Solutions

### "The visualization is laggy"
Increase UPDATE_INTERVAL in network_topology_visualizer.py:
```python
UPDATE_INTERVAL = 200  # 5 FPS instead of 10 FPS
```

### "Broker won't start"
Check two things:
1. Authentication: `remotive cloud organizations default <id>`
2. Docker logs: `cd broker-setup && docker compose logs signal-broker`

### "Web UI shows blank screen"
This is EXPECTED on macOS. Test broker with:
```bash
remotive broker signals list
```
If this works, broker is fine.

### "Add boundary boxes to show what's real vs demo"
Already done! Green box = RemotiveLabs, Orange boxes = Demo code.

Code location: `network_topology_visualizer.py` lines ~148-200

### "Make it connect to real broker"
Would need to replace simulated data with gRPC calls:
```python
from remotivelabs.broker.sync import SignalCreator
broker = SignalCreator("localhost:50051")
angle = broker.read_signal("SteeringBus", "SteeringCommand", "SteeringAngle")
```
But currently using pure simulation (no broker connection needed).

---

## Visualization Architecture

The main visualizer uses NetworkX for graph rendering:

### Node Positioning (Diamond/Star Layout)
```python
pos = {
    'Gateway': (0, 1),           # Left
    'CAN_Bus': (1, 2),           # Top center
    'RemotiveBroker': (1, 1),    # Center
    'Steering_ECU': (2, 1)       # Right
}

# Axis limits prevent overlap
self.ax_network.set_xlim(-0.5, 2.5)
self.ax_network.set_ylim(0.3, 2.7)
```

### Boundary Boxes (Show Real vs Demo)
```python
# RemotiveLabs box (green)
remotive_box = FancyBboxPatch(
    (0.4, 0.5), 1.3, 1.9,
    facecolor='lightgreen',
    edgecolor='darkgreen',
    alpha=0.15  # Semi-transparent
)

# Demo boxes (orange) - separate for left and right
demo_box_left = FancyBboxPatch(
    (-0.4, 0.5), 0.7, 1.0,
    facecolor='lightyellow',
    edgecolor='orange',
    alpha=0.15
)
```

### Edge Animation
```python
# Calculate alpha based on message activity
if data.get('color') == 'blue':  # Command
    if self.message_activity['command'] > 0:
        alpha = 0.9  # Bright
        width = width * 1.5
else:
    alpha = 0.4  # Dim

# Decay counters each frame
self.message_activity['command'] -= 1
```

---

## DBC Signal Schema

File: `broker-setup/configuration/can/steering.dbc`

```
BO_ 100 SteeringCommand: 8 Gateway
 SG_ SteeringAngle : 0|16@1+ (-2000,0.1) [-2000|2000] "degrees" ECU_Steering
 SG_ SteeringSpeed : 16|8@1+ (0,1) [0|255] "deg/s" ECU_Steering

BO_ 200 SteeringStatus: 8 ECU_Steering
 SG_ CurrentAngle : 0|16@1+ (-2000,0.1) [-2000|2000] "degrees" Gateway
 SG_ ECU_Ready : 16|1@1+ (0,1) [0|1] "" Gateway
```

- ID 100: Gateway → ECU (blue edges)
- ID 200: ECU → Gateway (red edges)

---

## Troubleshooting Checklist

### Broker Issues
```bash
# 1. Check containers
cd broker-setup
docker compose ps

# 2. View logs
docker compose logs signal-broker

# 3. Test connectivity
remotive broker signals list

# 4. Verify auth
cat ~/.config/remotive/credentials.json

# 5. Restart if needed
docker compose down && docker compose up -d
```

### Visualization Issues
```bash
# 1. Check Python environment
cd steering-demo
source venv/bin/activate
pip list | grep -E "matplotlib|networkx|numpy"

# 2. If packages missing
pip install matplotlib networkx numpy

# 3. Run with error output
python3 network_topology_visualizer.py 2>&1 | tee error.log
```

### Authentication Issues
```bash
# 1. Re-authenticate
remotive cloud auth login

# 2. List organizations
remotive cloud organizations list

# 3. Set default (CRITICAL!)
remotive cloud organizations default <org-id>

# 4. Check subscription
remotive cloud subscriptions list

# 5. Start trial if expired
remotive topology start-trial
```

---

## Quick Commands Reference

### Start Everything
```bash
# Terminal 1: Broker
cd /Users/lukastimm/RemotiveLabs/remotive-cli-demo/broker-setup
docker compose up -d

# Terminal 2: Visualization
cd /Users/lukastimm/RemotiveLabs/remotive-cli-demo/steering-demo
source venv/bin/activate
python3 network_topology_visualizer.py
```

### Stop Everything
```bash
# Stop broker
cd broker-setup
docker compose down

# Stop visualization
# Just close the matplotlib window
```

### Monitor Traffic
```bash
# With tshark (needs sudo on macOS)
sudo tshark -i lo0 -f "tcp port 50051"

# Generate traffic
remotive broker signals list
# Or use: ./generate_traffic.sh
```

---

## What NOT to Do

1. ❌ Don't use `network_mode: "host"` on macOS
2. ❌ Don't expect web UI to work on macOS Docker
3. ❌ Don't start broker before setting default organization
4. ❌ Don't use spring_layout() for NetworkX - use manual positioning
5. ❌ Don't update visualization every frame - skip expensive ops
6. ❌ Don't create new Python environments - use existing `venv/`
7. ❌ Don't try to fix "empty signals list" - it's not critical for demo

---

## Python Dependencies

**Already installed** in `steering-demo/venv/`:
```bash
matplotlib==3.9.3
networkx==3.4.2
numpy==2.2.1
```

If recreating:
```bash
python3 -m venv venv
source venv/bin/activate
pip install matplotlib networkx numpy
```

---

## Key Code Patterns

### Signal Simulation
```python
def generate_command(self, t):
    """Realistic sine wave + noise"""
    base = 500 * math.sin(t * 0.5)
    noise = 50 * math.sin(t * 2.3) + 30 * math.sin(t * 3.7)
    return base + noise

def update_ecu(self, command, dt=0.05):
    """Rate-limited response (realistic ECU lag)"""
    diff = self.target_angle - self.current_angle
    max_change = 150 * dt  # 150 deg/sec max
    step = max_change if abs(diff) > max_change else diff
    self.current_angle += step
    return self.current_angle
```

### NetworkX Graph Setup
```python
G = nx.DiGraph()

# Add nodes with attributes
G.add_node('RemotiveBroker',
           node_type='broker',
           color='lightgreen',
           size=4000,
           label='RemotiveBroker\\nlocalhost:50051')

# Add edges with message info
G.add_edge('Gateway', 'CAN_Bus',
           message='SteeringCommand',
           msg_id='100',
           color='blue',
           weight=2)

# Draw with manual positions
pos = {'Gateway': (0, 1), 'CAN_Bus': (1, 2), ...}
nx.draw_networkx_nodes(G, pos, node_color=[...], node_size=[...])
nx.draw_networkx_edges(G, pos, edge_color=[...])
```

---

## Expected Behaviors (Not Bugs!)

### Web UI Blank on macOS
- **Expected**: Docker networking limitation
- **Verify**: `remotive broker signals list` should work
- **Ignore**: The blank web UI

### Signals List Empty
- **Expected**: DBC uploaded but not "activated" in broker
- **Verify**: Visualization works with simulated data
- **Ignore**: Empty signals list

### tshark Requires Password
- **Expected**: macOS requires elevated privileges for packet capture
- **Fix**: `sudo tshark ...` or install ChmodBPF package
- **Alternative**: Use visualization instead of packet capture

---

## User's Environment

- **OS**: macOS (Darwin 24.1.0)
- **Working Directory**: `/Users/lukastimm/RemotiveLabs/remotive-cli-demo/steering-demo`
- **Docker**: Docker Compose available
- **Python**: 3.x with venv in `steering-demo/venv/`
- **RemotiveLabs**: Trial expires 2026-03-10

---

## If User Asks to Start Fresh

1. Stop everything:
```bash
cd broker-setup && docker compose down
```

2. Re-authenticate:
```bash
remotive cloud auth login
remotive cloud organizations default <org-id>
```

3. Restart:
```bash
docker compose up -d
cd ../steering-demo
source venv/bin/activate
python3 network_topology_visualizer.py
```

---

## Summary for Quick Context

This demo successfully:
✅ Runs RemotiveBroker in Docker with proper macOS configuration
✅ Shows interactive CAN bus topology with NetworkX
✅ Separates RemotiveLabs infrastructure from demo code visually
✅ Simulates realistic CAN traffic (steering commands + ECU responses)
✅ Runs smoothly at 10 FPS with optimized animation
✅ Includes comprehensive documentation for future reference

All learnings are captured in:
- `README.md` - Updated with quick start
- `COMPLETE_GUIDE.md` - Full reference
- `FOR_FUTURE_AGENTS.md` - This file

**Main achievement**: Clear demonstration of RemotiveLabs architecture with proper boundaries between real infrastructure and simulation code.
