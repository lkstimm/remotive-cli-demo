# RemotiveBroker Demo Setup - Complete Guide

## What We've Accomplished

Successfully set up a complete RemotiveBroker environment with:
1. ✅ RemotiveCloud authentication
2. ✅ Active 30-day trial subscription
3. ✅ Local RemotiveBroker running in Docker
4. ✅ Custom steering signal topology (DBC file)
5. ✅ Web interface accessible at http://localhost:8083

## Authentication Flow (Completed)

### Step 1: Cloud Authentication
```bash
# Login to RemotiveCloud (opens browser)
remotive cloud auth login
```
- Opens browser for OAuth authentication
- Stores credentials in `~/.config/remotive/`

### Step 2: Set Default Organization
```bash
# List available organizations
remotive cloud organizations list

# Set default (interactive or programmatic)
echo "1" | remotive cloud organizations default
```

### Step 3: Start Trial Subscription
```bash
# Start 30-day free trial
echo "Y" | remotive topology start-trial
```
- Trial expires: 2026-03-10
- Organization: Lukas's Organisation (uid: tgatsvwwbzgkekjnflia)

### Step 4: Verify Authentication
```bash
# Check who you're logged in as
remotive cloud auth whoami

# Check subscription status
remotive topology subscription status
```

## Broker Setup

### Directory Structure
```
broker-setup/
├── docker-compose.yml          # Modified for port 8083 and credentials
├── configuration/
│   ├── interfaces.json         # Virtual CAN with steering.dbc
│   └── can/
│       └── steering.dbc        # Custom steering signal definitions
```

### Key Configuration Changes

1. **docker-compose.yml**:
   - Web interface: Port 8083 (changed from 8080 to avoid conflicts)
   - Mounted credentials: `~/.config/remotive:/root/.config/remotive:ro`

2. **interfaces.json**:
   - Added virtual CAN bus "SteeringBus"
   - Loaded steering.dbc database
   - gRPC server on port 50051

3. **steering.dbc**:
   - ECU_Steering and Gateway nodes
   - SteeringCommand message (ID 100):
     - SteeringAngle: -2000 to +2000 degrees
     - SteeringSpeed: 0-255 deg/s
   - SteeringStatus message (ID 200):
     - CurrentAngle: Current steering position
     - ECU_Ready: ECU status flag

## Running the Broker

### Start the Broker
```bash
cd broker-setup
docker compose up -d
```

### Check Status
```bash
# View container status
docker compose ps

# View broker logs
docker compose logs signal-broker

# View web client logs
docker compose logs web-client
```

### Access Points
- **Web Interface**: http://localhost:8083
- **gRPC API**: localhost:50051 (configured)
- **HTTP API**: localhost:8081 (broker REST API)

### Stop the Broker
```bash
docker compose down
```

## Remotive CLI Commands Reference

### Authentication Commands
```bash
# Login
remotive cloud auth login

# Check current user
remotive cloud auth whoami

# List available accounts
remotive cloud auth list

# Logout (deactivate)
remotive cloud auth deactivate
```

### Organization Management
```bash
# List organizations
remotive cloud organizations list

# Set default organization
remotive cloud organizations default
```

### Subscription Management
```bash
# Check subscription status
remotive topology subscription status

# Start trial (30 days)
remotive topology start-trial
```

### Broker Interaction
```bash
# List signals (requires running broker)
remotive broker --url http://localhost:50051 signals list

# Discover brokers on network
remotive broker discover

# Set default broker URL
export REMOTIVE_BROKER_URL=http://localhost:50051
```

## Troubleshooting

### Port Conflicts
If port 8083 is in use:
1. Edit `docker-compose.yml`
2. Change `"8083:8080"` to another port
3. Restart: `docker compose down && docker compose up -d`

### Credentials Not Found
The broker needs access to your RemotiveCloud credentials:
- Credentials location: `~/.config/remotive/`
- docker-compose.yml must mount this directory
- Current mount: `${HOME}/.config/remotive:/root/.config/remotive:ro`

### Broker Won't Start
```bash
# Check logs
docker compose logs signal-broker

# Remove old boot configuration
rm configuration/boot

# Restart fresh
docker compose down && docker compose up -d
```

### Clear Everything and Start Over
```bash
# Stop and remove containers
docker compose down

# Remove boot config
rm -f configuration/boot

# Start fresh
docker compose up -d
```

## Next Steps

Now that the broker is running with authentication, you can:

1. **Access Web Interface**: http://localhost:8083
   - View signals
   - Record data
   - Playback recordings

2. **Use CLI Tools**:
   ```bash
   remotive broker signals list
   remotive broker signals subscribe SteeringAngle
   ```

3. **Build Applications**:
   - Create ECU simulators
   - Publish steering commands
   - Subscribe to signal updates
   - Build visualization UIs

## Credentials and Trial Info

- **Email**: lkstimm@gmail.com
- **Organization**: Lukas's Organisation
- **Organization UID**: tgatsvwwbzgkekjnflia
- **Trial Expires**: 2026-03-10
- **Credentials Path**: `~/.config/remotive/`

## Important Files

1. **Credentials**: `~/.config/remotive/personal-token-*.json`
2. **Config**: `~/.config/remotive/config.json`
3. **DBC File**: `broker-setup/configuration/can/steering.dbc`
4. **Interfaces**: `broker-setup/configuration/interfaces.json`
5. **Docker Compose**: `broker-setup/docker-compose.yml`

## Resources

- Documentation: https://docs.remotivelabs.com
- RemotiveCloud Console: https://console.cloud.remotivelabs.com
- GitHub Bootstrap: https://github.com/remotivelabs/remotivebroker-bootstrap
- License Agreement: https://www.remotivelabs.com/license
