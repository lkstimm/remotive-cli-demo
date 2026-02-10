# Documentation Index

Quick reference for all documentation in this demo.

## Start Here 👈

**New to this demo?** Start with:
1. [README.md](README.md) - Overview and quick start (2 commands!)
2. Run the visualization to see it in action
3. Then read the guides below as needed

## Documentation Files

### For Users

| File | Purpose | Read When |
|------|---------|-----------|
| **[README.md](README.md)** | Overview, quick start, key learnings | First time using demo |
| **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** | Comprehensive reference with all details | Need troubleshooting or deep dive |
| **[steering-demo/QUICK_START.md](steering-demo/QUICK_START.md)** | Two-terminal quick start with tshark | Want to monitor traffic |
| **[steering-demo/ARCHITECTURE.md](steering-demo/ARCHITECTURE.md)** | What's RemotiveLabs vs demo code | Confused about boundaries |

### For AI Agents

| File | Purpose |
|------|---------|
| **[FOR_FUTURE_AGENTS.md](FOR_FUTURE_AGENTS.md)** | Comprehensive guide for future AI agents |
| **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** | Detailed technical reference |

## Quick Links by Topic

### Getting Started
- Quick start: [README.md](README.md#-quick-start-2-commands)
- Authentication: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md#1-authentication-flow)
- Docker setup: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md#2-docker-networking-on-macos)

### Running the Demo
- Main visualization: `steering-demo/network_topology_visualizer.py`
- Interactive launcher: `steering-demo/simple_demo.sh`
- Traffic monitoring: [QUICK_START.md](steering-demo/QUICK_START.md)

### Understanding the Architecture
- Component boundaries: [ARCHITECTURE.md](steering-demo/ARCHITECTURE.md)
- Network topology: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md#network-topology)
- Message flow: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md#message-flow)

### Troubleshooting
- Common issues: [README.md](README.md#-quick-troubleshooting)
- Detailed troubleshooting: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md#troubleshooting)
- For agents: [FOR_FUTURE_AGENTS.md](FOR_FUTURE_AGENTS.md#troubleshooting-checklist)

### Technical Deep Dives
- Docker on macOS: [FOR_FUTURE_AGENTS.md](FOR_FUTURE_AGENTS.md#1-docker-on-macos---must-fix)
- Visualization performance: [FOR_FUTURE_AGENTS.md](FOR_FUTURE_AGENTS.md#4-visualization-performance-on-macos)
- NetworkX implementation: [FOR_FUTURE_AGENTS.md](FOR_FUTURE_AGENTS.md#visualization-architecture)
- Signal simulation: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md#5-signal-simulation)

## File Structure

```
remotive-cli-demo/
├── INDEX.md                    # This file
├── README.md                   # Main overview
├── COMPLETE_GUIDE.md          # Comprehensive guide
├── FOR_FUTURE_AGENTS.md       # AI agent reference
│
├── broker-setup/
│   ├── docker-compose.yml      # Broker configuration
│   └── configuration/
│       ├── interfaces.json     # CAN bus config
│       └── can/
│           └── steering.dbc    # Signal definitions
│
└── steering-demo/
    ├── network_topology_visualizer.py  # ⭐ Main viz
    ├── topology_visualizer.py
    ├── steering_visualizer.py
    ├── simple_demo.sh
    ├── generate_traffic.sh
    ├── ARCHITECTURE.md            # Component boundaries
    ├── QUICK_START.md             # Quick reference
    └── venv/                      # Python environment
```

## Documentation Stats

- **Total documentation files**: 7
- **For users**: 4 files
- **For AI agents**: 2 files  
- **Config files**: Multiple in broker-setup/
- **Python scripts**: 3 visualizers
- **Shell scripts**: 2 helpers

## What's Documented

✅ Complete setup and installation  
✅ Authentication flow  
✅ Docker configuration (macOS compatible)  
✅ Virtual CAN bus setup  
✅ DBC signal definitions  
✅ Visualization implementation  
✅ Performance optimization  
✅ Troubleshooting guide  
✅ Architecture diagrams  
✅ Code patterns and examples  
✅ Common pitfalls and solutions  
✅ Reference commands  

## Need Help?

1. **Quick answer**: Check [README.md](README.md) troubleshooting section
2. **Detailed help**: See [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)
3. **AI agents**: Read [FOR_FUTURE_AGENTS.md](FOR_FUTURE_AGENTS.md)
4. **Official docs**: https://docs.remotivelabs.com

---

**Last Updated**: 2026-02-10  
**Demo Status**: ✅ Fully functional  
**Trial Expires**: 2026-03-10
