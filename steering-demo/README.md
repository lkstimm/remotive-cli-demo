# Steering Demo - RemotiveBroker

Complete demo showing publisher/subscriber pattern with RemotiveBroker using steering commands.

## Overview

This demo simulates a realistic automotive scenario:
- **Gateway** publishes steering commands (sine wave pattern)
- **ECU** subscribes to commands and publishes current steering angle
- **Monitor** observes all CAN traffic using CLI or Wireshark

## Components

### 1. Publisher (`publisher.py`)
- Publishes `SteeringCommand` messages
- Sends sine wave pattern (-500° to +500°)
- Simulates gateway sending commands to ECU

### 2. ECU Simulator (`ecu_simulator.py`)
- Subscribes to `SteeringCommand` messages
- Simulates realistic steering movement (max 50°/s)
- Publishes `SteeringStatus` with current angle

### 3. Monitor (CLI/Wireshark)
- **CLI**: `remotive broker signals subscribe`
- **Wireshark**: `tshark` to capture CAN traffic

## Quick Start

### Option 1: Run Complete Demo
```bash
./run_demo.sh
```

This starts all components and monitors signals using the Remotive CLI.

### Option 2: Manual Start (Separate Terminals)

**Terminal 1 - Publisher:**
```bash
source venv/bin/activate
python3 publisher.py
```

**Terminal 2 - ECU Simulator:**
```bash
source venv/bin/activate
python3 ecu_simulator.py
```

**Terminal 3 - Monitor with CLI:**
```bash
remotive broker signals subscribe SteeringCommand.SteeringAngle
```

**Terminal 4 - Monitor with tshark (if available):**
```bash
# Monitor localhost traffic on broker port
tshark -i lo0 -f "tcp port 50051" -Y "http"
```

## Signal Definitions

From `steering.dbc`:

### SteeringCommand (ID: 100)
- `SteeringAngle`: -2000 to +2000 degrees (scale: 0.1)
- `SteeringSpeed`: 0-255 deg/s

### SteeringStatus (ID: 200)
- `CurrentAngle`: -2000 to +2000 degrees (scale: 0.1)
- `ECU_Ready`: 0 or 1

## Architecture

```
┌──────────────┐        SteeringCommand        ┌──────────────┐
│              │────────────────────────────────>│              │
│  Gateway     │                                 │  Steering    │
│  (Publisher) │        SteeringStatus          │  ECU         │
│              │<────────────────────────────────│  (Subscriber)│
└──────────────┘                                 └──────────────┘
       │                                                  │
       │                                                  │
       └──────────────────┬───────────────────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │               │
                  │ RemotiveBroker│
                  │ (localhost    │
                  │  :50051)      │
                  └───────────────┘
                          │
                          ▼
                    ┌─────────┐
                    │ Monitor │
                    │ (CLI/   │
                    │ tshark) │
                    └─────────┘
```

## Observing Traffic

### Using Remotive CLI
```bash
# List all signals
remotive broker signals list

# Subscribe to specific signals
remotive broker signals subscribe SteeringCommand.SteeringAngle

# Subscribe with pattern matching
remotive broker signals subscribe "Steering*"
```

### Using tshark (Wireshark CLI)
```bash
# Capture on loopback interface
tshark -i lo0 -f "tcp port 50051"

# With HTTP/2 filtering (gRPC uses HTTP/2)
tshark -i lo0 -f "tcp port 50051" -Y "http2"

# Save to file for later analysis
tshark -i lo0 -f "tcp port 50051" -w steering_demo.pcapng

# Analyze saved capture
tshark -r steering_demo.pcapng
```

### Using Wireshark GUI
```bash
# Start Wireshark and capture on loopback
wireshark -i lo0 -f "tcp port 50051"
```

Filter in Wireshark: `tcp.port == 50051`

## Expected Output

### Publisher
```
🚗 Steering Command Publisher
📡 Connecting to broker at http://localhost:50051...
✓ Connected to broker

📊 Publishing steering commands...
   (Sine wave pattern: -500° to +500°)

📤 Steering Angle:    0.0° | Speed: 100 deg/s
📤 Steering Angle:   49.9° | Speed: 100 deg/s
📤 Steering Angle:   98.7° | Speed: 100 deg/s
...
```

### ECU Simulator
```
🎮 Steering ECU Simulator
📡 Connecting to broker at http://localhost:50051...
✓ Connected to broker

🎯 ECU ready - listening for steering commands...

📥 Received command: Target =    0.0°
📤 ECU Status: Current =    0.0° | Target =    0.0°
📥 Received command: Target =   49.9°
📤 ECU Status: Current =    5.0° | Target =   49.9°
📤 ECU Status: Current =   10.0° | Target =   49.9°
...
```

## Troubleshooting

### Broker Not Running
```bash
cd ../broker-setup
docker compose up -d
```

### No Signals Appearing
The broker may need the DBC file loaded. Check:
```bash
remotive broker signals list
```

If empty, the configuration needs to be activated via the broker API or web interface.

### Python Import Errors
```bash
source venv/bin/activate
pip install remotivelabs-broker
```

### tshark Permission Issues
```bash
# macOS - run with sudo or add user to access_bpf group
sudo tshark -i lo0 -f "tcp port 50051"
```

## Files

- `publisher.py` - Steering command publisher
- `ecu_simulator.py` - ECU that responds to commands
- `run_demo.sh` - Automated demo runner
- `README.md` - This file
- `venv/` - Python virtual environment

## Next Steps

1. Modify the publisher to use keyboard input instead of sine wave
2. Add visualization using matplotlib or terminal graphics
3. Record and playback sessions
4. Add more ECUs (braking, throttle, etc.)
5. Implement CAN error simulation

## Resources

- RemotiveBroker Docs: https://docs.remotivelabs.com
- Python API: https://github.com/remotivelabs/remotivelabs-apis
- DBC File: `../broker-setup/configuration/can/steering.dbc`
