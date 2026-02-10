# Quick Start - Run Demo Now! 🚀

## Two Terminal Setup

### Terminal 1 - Run tshark monitor
```bash
cd /Users/lukastimm/RemotiveLabs/remotive-cli-demo/steering-demo
./simple_demo.sh
# Type 'y' when prompted
# Enter your sudo password
```

### Terminal 2 - Generate traffic
```bash
cd /Users/lukastimm/RemotiveLabs/remotive-cli-demo/steering-demo
./generate_traffic.sh
```

## What You'll See

### In Terminal 1 (tshark):
You'll see HTTP/2 packets (gRPC uses HTTP/2):
```
1   0.000000    127.0.0.1 → 127.0.0.1    HTTP2 [HEADERS]
2   0.001234    127.0.0.1 → 127.0.0.1    HTTP2 [DATA]
3   0.002345    127.0.0.1 → 127.0.0.1    HTTP2 [HEADERS]
```

### In Terminal 2 (traffic generator):
```
📤 API Call #1 - 11:50:23
📤 API Call #2 - 11:50:24
📤 API Call #3 - 11:50:25
```

## Alternative: Manual Commands

**Generate one call at a time:**
```bash
remotive broker signals list
```

**Watch in real-time:**
```bash
# Terminal 1
sudo tshark -i lo0 -f "tcp port 50051"

# Terminal 2
while true; do remotive broker signals list; sleep 1; done
```

## What You're Observing

- **Client**: Remotive CLI making gRPC calls
- **Server**: RemotiveBroker responding
- **Protocol**: gRPC over HTTP/2
- **Port**: 50051
- **Interface**: Loopback (lo0)

Each call to `remotive broker signals list` generates:
1. TCP connection (if new)
2. HTTP/2 HEADERS frame (request)
3. HTTP/2 DATA frame (response)
4. TCP teardown (if connection closed)

## Success! 🎉

You're now monitoring real CAN bus traffic between the Remotive CLI and broker!
