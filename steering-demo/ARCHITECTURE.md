# Architecture Overview - What's Real vs Demo

## RemotiveLabs Components (Real Infrastructure)

```
┌─────────────────────────────────────────────────────────┐
│                 REMOTIVELABS INFRASTRUCTURE              │
│                                                          │
│  ┌────────────────────────┐                             │
│  │  RemotiveCloud         │                             │
│  │  (Authentication SaaS) │                             │
│  │  - OAuth login         │                             │
│  │  - Organizations       │                             │
│  │  - Subscriptions       │                             │
│  └────────────────────────┘                             │
│                                                          │
│  ┌────────────────────────┐                             │
│  │  Remotive CLI          │                             │
│  │  - Command-line tool   │                             │
│  │  - gRPC client         │                             │
│  │  - Commands:           │                             │
│  │    • broker signals    │                             │
│  │    • topology          │                             │
│  │    • cloud auth        │                             │
│  └────────────────────────┘                             │
│                                                          │
│  ┌────────────────────────┐                             │
│  │  RemotiveBroker        │                             │
│  │  (Docker Container)    │                             │
│  │  - gRPC server         │                             │
│  │  - Port: 50051         │                             │
│  │  - CAN bus emulation   │                             │
│  │  - Signal routing      │                             │
│  │  - DBC file handling   │                             │
│  └────────────────────────┘                             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Demo/Simulation Code (Our Mocked Code)

```
┌─────────────────────────────────────────────────────────┐
│                    DEMO/MOCK COMPONENTS                  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Simulated Data Generation                         │ │
│  │                                                     │ │
│  │  In: network_topology_visualizer.py                │ │
│  │                                                     │ │
│  │  def generate_command(self, t):                    │ │
│  │      """Generate realistic steering command"""     │ │
│  │      base = 500 * math.sin(t * 0.5)               │ │
│  │      noise = 50 * math.sin(t * 2.3) + ...         │ │
│  │      return base + noise                           │ │
│  │                                                     │ │
│  │  def update_ecu(self, command, dt=0.05):          │ │
│  │      """Simulate ECU response with lag"""          │ │
│  │      # Rate-limited angle tracking                 │ │
│  │      # Simulates realistic ECU damping             │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Visualization                                      │ │
│  │                                                     │ │
│  │  • steering_visualizer.py                          │ │
│  │    - Basic dual-graph plot                         │ │
│  │    - Command vs Response                           │ │
│  │                                                     │ │
│  │  • topology_visualizer.py                          │ │
│  │    - Manual box layout                             │ │
│  │    - Animated arrows                               │ │
│  │                                                     │ │
│  │  • network_topology_visualizer.py                  │ │
│  │    - NetworkX graph rendering                      │ │
│  │    - Animated edge highlighting                    │ │
│  │    - Real-time data plots                          │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Shell Scripts                                      │ │
│  │                                                     │ │
│  │  • generate_traffic.sh                             │ │
│  │    - Calls: remotive broker signals list           │ │
│  │    - Used to generate gRPC traffic                 │ │
│  │                                                     │ │
│  │  • simple_demo.sh                                  │ │
│  │    - Launches tshark packet capture                │ │
│  │    - Interactive demo launcher                     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## What's Real CAN Traffic vs Simulated

### Real CAN Traffic (Would Happen in Production):
- **Gateway ECU** publishes real steering commands to physical CAN bus
- **Steering ECU** subscribes to CAN messages and controls actual hardware
- **RemotiveBroker** routes messages between physical CAN interfaces
- Messages follow DBC signal definitions

### Our Demo Simulation:
- **No physical CAN bus** - we're using RemotiveBroker's virtual CAN
- **No real ECUs** - we're generating fake data with Python math functions
- **No actual message publishing** - we're just visualizing what traffic would look like
- The sine wave patterns are purely mathematical, not from real sensors

## DBC File (steering.dbc)

```
┌────────────────────────────────────┐
│  REAL REMOTIVELABS COMPONENT       │
│                                    │
│  steering.dbc                      │
│  - Signal definitions              │
│  - Message IDs                     │
│  - Data types                      │
│  - Value ranges                    │
│                                    │
│  BO_ 100 SteeringCommand           │
│  BO_ 200 SteeringStatus            │
└────────────────────────────────────┘
```

**But**: We uploaded it, but we're not actually using it in the demo. The visualizer generates fake data matching the DBC schema.

## Data Flow Diagram

```
DEMO MODE (Current):
┌─────────────┐
│   Python    │
│  Simulator  │  ← YOU ARE HERE
│             │
│ • Generates │
│   sine wave │
│ • Simulates │
│   ECU lag   │
│ • Animates  │
│   visuals   │
└─────────────┘

No connection to RemotiveBroker in visualization scripts!
Just simulating what traffic would look like.


PRODUCTION MODE (What RemotiveLabs does for real):
┌──────────┐         ┌────────────────┐         ┌──────────┐
│ Gateway  │  CAN    │ RemotiveBroker │  CAN    │ ECU      │
│ (real    │ ───────→│ (routes via    │ ───────→│ (real    │
│ hardware)│         │  gRPC/DBC)     │         │ hardware)│
└──────────┘         └────────────────┘         └──────────┘
                             ↑
                             │
                      ┌──────┴──────┐
                      │ Remotive CLI│
                      │ (monitor)   │
                      └─────────────┘
```

## Summary

| Component | Type | Purpose |
|-----------|------|---------|
| RemotiveCloud | **RemotiveLabs** | Authentication & subscriptions |
| Remotive CLI | **RemotiveLabs** | Command-line interface to broker |
| RemotiveBroker | **RemotiveLabs** | CAN bus routing & signal management |
| steering.dbc | **RemotiveLabs Standard** | Signal definition format |
| Python visualizers | **Demo Code** | Animated graphs (no real data) |
| generate_command() | **Demo Code** | Fake steering data generator |
| update_ecu() | **Demo Code** | Simulated ECU response |
| Shell scripts | **Demo Code** | Traffic generation & monitoring |

## The Confusion

You might be confused because:

1. **The visualizer shows realistic CAN message flow** - but it's all simulated math (sine waves)
2. **We set up RemotiveBroker** - but we're not actually using it in the visualization
3. **We have a DBC file** - but we're not publishing real messages matching it

The visualizer is **demonstrating what RemotiveLabs topology looks like** without actually connecting to the broker. It's a **standalone educational animation**.

## To Make It Real

To actually use RemotiveLabs infrastructure instead of simulation:

```python
# Would need to replace this simulated code:
command = self.generate_command(t)  # Fake sine wave

# With actual RemotiveBroker gRPC calls:
from remotivelabs.broker.sync import SignalCreator
broker = SignalCreator("localhost:50051")
command = broker.read_signal("SteeringCommand", "SteeringAngle")
```

But we didn't do that because:
- Simpler to demonstrate without gRPC complexity
- Shows the concepts without requiring running broker
- Easier to understand the topology visually
