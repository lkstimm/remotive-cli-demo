# RemotiveLabs CLI Demo - Complete Working Example

A complete demonstration of RemotiveLabs CLI and broker infrastructure for automotive CAN bus development, including interactive visualizations and real-time network topology.

**Status**: ✅ Fully functional | **Created**: 2026-02-10 | **Trial Expires**: 2026-03-10

## 🚀 Quick Start (2 commands!)

```bash
# 1. Start RemotiveBroker
cd broker-setup && docker compose up -d

# 2. Run visualization
cd ../steering-demo && source venv/bin/activate && python3 network_topology_visualizer.py
```

You'll see an interactive window showing real-time CAN bus topology with animated message flow!

## 📦 What's Included

### Working Components
- ✅ **RemotiveBroker** - Docker container on localhost:50051
- ✅ **Virtual CAN Bus** - SteeringBus with steering signals
- ✅ **Interactive Visualizations** - NetworkX-based topology + real-time graphs
- ✅ **DBC Signals** - SteeringCommand (ID 100) and SteeringStatus (ID 200)
- ✅ **Boundary Boxes** - Clearly shows RemotiveLabs infrastructure vs demo code
- ✅ **Traffic Monitoring** - Scripts for Wireshark/tshark
- ✅ **Complete Documentation** - All learnings captured

### Visualizations

**network_topology_visualizer.py** ⭐ (Main)
- NetworkX graph showing Gateway → Broker → ECU
- Green box: RemotiveLabs infrastructure
- Orange boxes: Demo/simulation code
- Animated edges (blue=command, red=status)
- Real-time data plots on the right
- Optimized performance (10 FPS, smooth on macOS)

**Also included:**
- `topology_visualizer.py` - Alternate layout style
- `steering_visualizer.py` - Simple dual-graph view

## 📚 Documentation

| File | Purpose |
|------|---------|
| **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** | 📖 Full guide with all learnings, troubleshooting, and reference |
| **[steering-demo/ARCHITECTURE.md](steering-demo/ARCHITECTURE.md)** | 🏗️ What's RemotiveLabs vs demo code |
| **[steering-demo/QUICK_START.md](steering-demo/QUICK_START.md)** | ⚡ Two-terminal quick start with tshark |

## 🎯 What is Remotive CLI?

The Remotive CLI is a command-line tool for managing RemotiveLabs cloud resources, brokers, and signal topologies for automotive software development.

## Main Commands

### 1. TUI (Text User Interface)
Launch an interactive interface to explore commands:
```bash
remotive tui
```

### 2. Topology Management
Work with RemotiveTopology resources (signal databases, ECU configurations):
```bash
# Show version
remotive topology version

# Show subscription status
remotive topology subscription status

# List workspaces
remotive topology workspace list
```

### 3. Broker Management
Manage local or cloud brokers:
```bash
# Discover brokers on your network
remotive broker discover

# List signals (requires running broker)
remotive broker signals list

# View broker license info
remotive broker license info
```

### 4. Cloud Management
Manage RemotiveCloud resources:
```bash
remotive cloud --help
```

### 5. Tools
Additional CLI utilities:
```bash
remotive tools --help
```

## Quick Start Examples

### Example 1: Check Your Setup
```bash
# Check CLI version
remotive --version

# Check topology version
remotive topology version

# Check subscription status
remotive topology subscription status
```

### Example 2: Explore with TUI
The easiest way to explore is using the interactive TUI:
```bash
remotive tui
```

### Example 3: Discover Brokers
Find brokers running on your network:
```bash
remotive broker discover
```

### Example 4: Work with Signals (requires broker)
```bash
# List available signals
remotive broker signals list

# Subscribe to a signal
remotive broker signals subscribe <signal-name>
```

## Common Workflows

### Working with Topologies
1. Create or import a signal database
2. Validate the topology
3. Generate environment configurations
4. Deploy to broker

### Recording and Playback
1. Start recording from a broker
2. Export recording data
3. Playback recordings for testing

### Cloud Operations
1. List cloud resources
2. Deploy brokers to cloud
3. Manage cloud configurations

## Environment Variables

Key environment variables you can set:
- `REMOTIVE_BROKER_URL`: Default broker URL (default: http://localhost:50051)
- `REMOTIVE_TOPOLOGY_IMAGE`: Docker image for RemotiveTopology
- `REMOTIVE_TOPOLOGY_WORKSPACE`: Workspace path override
- `CONTAINER_ENGINE`: Choose docker or podman

## Next Steps

1. Try the TUI: `remotive tui`
2. Explore the documentation: https://docs.remotivelabs.com
3. Check subscription status: `remotive topology subscription status`
4. Start a trial if needed: `remotive topology start-trial`

## Tips

- Use `--help` with any command to see detailed options
- The TUI is the easiest way to discover commands
- Most commands work with both local and cloud brokers
- You can tab-complete commands if you run: `remotive --install-completion`

## 🔑 Key Learnings for Future Agents

### Docker on macOS
- ❌ `network_mode: "host"` doesn't work (Docker runs in VM)
- ✅ Use explicit port mappings: `ports: ["50051:50051"]`
- ✅ Mount auth: `~/.config/remotive:/root/.config/remotive:ro`

### Authentication Flow
```bash
remotive cloud auth login                    # Opens browser OAuth
remotive cloud organizations default <id>     # Set org first!
remotive topology start-trial                 # Start trial (expires 2026-03-10)
```

### Performance Optimization
- Update interval: 100ms (10 FPS) for smooth animation
- Reduce data points: 50 instead of 100
- Skip expensive redraws: `if frame % 2 == 0: draw_edges()`

### Visualization Best Practices
- ✅ NetworkX better than manual box drawing
- ✅ Use manual positioning for clarity, not automatic layouts
- ✅ Add boundary boxes to show component separation
- ✅ Semi-transparent overlays (alpha=0.15)

### Common Pitfalls
- Web UI will be blank on macOS Docker (this is normal!)
- Verify broker works with: `remotive broker signals list`
- tshark requires sudo on macOS (or install ChmodBPF)
- Signals list may be empty (DBC uploaded but not activated - not critical)

See **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** for detailed explanations.

## 📁 Directory Structure

```
remotive-cli-demo/
├── README.md                    # This file
├── COMPLETE_GUIDE.md           # Comprehensive documentation
│
├── broker-setup/
│   ├── docker-compose.yml      # ⚙️  Broker configuration (macOS compatible!)
│   └── configuration/
│       ├── interfaces.json     # Virtual CAN bus definitions
│       └── can/
│           └── steering.dbc    # Signal database (ID 100, 200)
│
└── steering-demo/
    ├── network_topology_visualizer.py  # ⭐ Main visualization
    ├── topology_visualizer.py          # Alternate layout
    ├── steering_visualizer.py          # Simple view
    ├── simple_demo.sh                  # 🚀 Interactive demo launcher
    ├── generate_traffic.sh             # Traffic generator
    ├── ARCHITECTURE.md                 # Component boundaries
    ├── QUICK_START.md                  # Quick reference
    └── venv/                           # Python environment
```

## 🏗️ Architecture

```
┌───────────────────┐         ┌────────────────┐         ┌───────────────────┐
│ Gateway (Demo)    │         │ RemotiveLabs   │         │ Steering ECU      │
│                   │         │ Infrastructure │         │ (Demo)            │
│ • Simulates       │────────→│                │────────→│                   │
│   steering cmds   │         │ • Broker       │         │ • Simulates       │
│ • Sine waves      │         │ • CAN Bus      │         │   ECU response    │
│   (fake data)     │←────────│ • gRPC routing │←────────│ • Rate limiting   │
└───────────────────┘         └────────────────┘         └───────────────────┘
     Orange Box               Green Box                      Orange Box
     (Demo Code)           (Real Infrastructure)            (Demo Code)
```

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Broker won't start | `docker compose logs signal-broker` - check auth or ports |
| Web UI blank | Normal on macOS! Test with `remotive broker signals list` |
| Visualization laggy | Increase UPDATE_INTERVAL to 200ms in Python script |
| Auth errors | `remotive cloud auth login` and set default org |
| tshark asks password | Need sudo on macOS, or install ChmodBPF package |

Full troubleshooting: **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md#troubleshooting)**

## 📖 Full Documentation

- **RemotiveLabs Docs**: https://docs.remotivelabs.com
- **This Demo's Guide**: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)
