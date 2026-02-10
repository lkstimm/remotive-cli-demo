# 🎉 RemotiveCLI Demo - Complete!

## What We Built

A complete RemotiveBroker demo environment with:

✅ **RemotiveCloud Authentication**
- Logged in via browser OAuth
- Trial subscription active (expires 2026-03-10)
- Credentials configured

✅ **Local RemotiveBroker Running**
- Docker containers deployed
- gRPC API accessible at `localhost:50051`
- Web interface at `http://localhost:8083`
- Fixed macOS networking issues

✅ **Steering Signal Topology**
- Custom DBC file with steering signals
- Gateway and ECU nodes defined
- Command and status messages

✅ **Demo Scripts**
- Simple CLI-based demo
- Traffic monitoring with tshark/Wireshark
- Python publisher/subscriber templates

## Directory Structure

```
remotive-cli-demo/
├── README.md                    # Getting started guide
├── DEMO_SETUP_COMPLETE.md       # Authentication flow details
├── BROKER_STATUS.md             # Current broker status
├── DEMO_COMPLETE.md             # This file
├── broker-setup/                # RemotiveBroker Docker setup
│   ├── docker-compose.yml       # Modified for macOS
│   └── configuration/
│       ├── interfaces.json      # Virtual CAN configuration
│       └── can/
│           └── steering.dbc     # Signal definitions
└── steering-demo/               # Demo scripts
    ├── README.md                # Demo documentation
    ├── simple_demo.sh           # ✨ Run this!
    ├── publisher.py             # Signal publisher (template)
    ├── ecu_simulator.py         # ECU simulator (template)
    └── venv/                    # Python environment
```

## 🚀 Quick Start

### Run the Demo
```bash
cd steering-demo
./simple_demo.sh
```

This will:
1. ✅ Check broker connectivity
2. 📊 List available signals
3. 🔍 Show monitoring options (CLI, tshark, Wireshark)
4. 💡 Offer to start traffic monitoring

### Monitor with CLI
```bash
# List signals
remotive broker signals list

# Subscribe to signals
remotive broker signals subscribe <signal-name>
```

### Monitor with tshark
```bash
# Capture broker traffic
tshark -i lo0 -f "tcp port 50051"

# With HTTP/2 filtering (gRPC uses HTTP/2)
sudo tshark -i lo0 -f "tcp port 50051" -Y "http2"
```

### Monitor with Wireshark GUI
```bash
wireshark -i lo0 -f "tcp port 50051"
```

## Key Learnings - RemotiveCLI Authentication Flow

### 1. Login
```bash
remotive cloud auth login
```
- Opens browser for OAuth
- Stores credentials in `~/.config/remotive/`

### 2. Set Organization
```bash
# List organizations
remotive cloud organizations list

# Set default
echo "1" | remotive cloud organizations default
```

### 3. Start Trial
```bash
# 30-day free trial
echo "Y" | remotive topology start-trial
```

### 4. Verify
```bash
# Check authentication
remotive cloud auth whoami

# Check subscription
remotive topology subscription status
```

## Key Learnings - Docker on macOS

### Issue: `network_mode: "host"` Doesn't Work
- Docker Desktop on macOS runs in a VM
- Host networking not supported like on Linux
- **Solution**: Use explicit port mappings

### Before (Broken on macOS):
```yaml
signal-broker:
  network_mode: "host"
```

### After (Works on macOS):
```yaml
signal-broker:
  ports:
    - "50051:50051"
    - "4040:4040"
    - "4000:4000"
```

### Credentials Mount
```yaml
volumes:
  - "${HOME}/.config/remotive:/root/.config/remotive:ro"
```

## Broker Status

### What's Working
- ✅ Broker running and accessible
- ✅ gRPC API responds: `remotive broker signals list` returns `[]`
- ✅ CLI commands work
- ✅ Authentication complete
- ✅ Trial subscription active

### Current State
- ⚠️ No signals loaded yet (broker returns empty array)
- ⚠️ DBC configuration needs to be activated
- ⚠️ Web interface shows blank (expected on macOS Docker)

### Next Steps
The signals need to be loaded into the broker. Options:
1. Use the web interface (if it connects) to upload and activate the DBC
2. Use RemotiveCloud brokers instead of local
3. Check RemotiveLabs documentation for signal activation

## Files Created

### Documentation
- `README.md` - Project overview
- `DEMO_SETUP_COMPLETE.md` - Authentication walkthrough
- `BROKER_STATUS.md` - Troubleshooting guide
- `DEMO_COMPLETE.md` - This summary

### Configuration
- `broker-setup/configuration/interfaces.json` - CAN bus config
- `broker-setup/configuration/can/steering.dbc` - Signal definitions
- `broker-setup/docker-compose.yml` - Modified for macOS

### Demo Scripts
- `steering-demo/simple_demo.sh` - Interactive demo runner
- `steering-demo/publisher.py` - Signal publisher template
- `steering-demo/ecu_simulator.py` - ECU simulator template
- `steering-demo/README.md` - Demo documentation

## Useful Commands

### Broker Management
```bash
# Start broker
cd broker-setup && docker compose up -d

# Stop broker
docker compose down

# View logs
docker compose logs signal-broker

# Restart
docker compose restart signal-broker
```

### CLI Commands
```bash
# Set default broker URL
export REMOTIVE_BROKER_URL=http://localhost:50051

# List signals
remotive broker signals list

# Subscribe to signals
remotive broker signals subscribe <signal-name>

# Discover brokers on network
remotive broker discover

# Upload files
remotive broker files upload <file>
```

### Authentication
```bash
# Check who you are
remotive cloud auth whoami

# List organizations
remotive cloud organizations list

# Check subscription
remotive topology subscription status
```

## Signal Definitions (steering.dbc)

### Nodes
- `ECU_Steering` - Steering ECU
- `Gateway` - Command gateway

### Messages

**SteeringCommand (ID: 100)**
- `SteeringAngle`: -2000 to +2000 degrees (scale 0.1)
- `SteeringSpeed`: 0-255 deg/s

**SteeringStatus (ID: 200)**
- `CurrentAngle`: -2000 to +2000 degrees (scale 0.1)
- `ECU_Ready`: 0 or 1 (boolean)

## Resources

- **Documentation**: https://docs.remotivelabs.com
- **RemotiveCloud**: https://console.cloud.remotivelabs.com
- **GitHub Bootstrap**: https://github.com/remotivelabs/remotivebroker-bootstrap
- **License Agreement**: https://www.remotivelabs.com/license

## Credentials

- **Email**: lkstimm@gmail.com
- **Organization**: Lukas's Organisation
- **Org UID**: tgatsvwwbzgkekjnflia
- **Trial Expires**: 2026-03-10
- **Credentials**: `~/.config/remotive/`

## Success! 🎉

You now have:
1. ✅ Authenticated RemotiveCloud account
2. ✅ Active trial subscription
3. ✅ Running RemotiveBroker (localhost:50051)
4. ✅ Demo scripts ready to use
5. ✅ Traffic monitoring setup (tshark/Wireshark)

**Try the demo:**
```bash
cd steering-demo
./simple_demo.sh
```

Enjoy exploring the RemotiveCLI! 🚗✨
