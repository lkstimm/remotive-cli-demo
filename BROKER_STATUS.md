# RemotiveBroker Setup Status

## ✅ Successfully Completed

1. **Authentication**:
   - Logged into RemotiveCloud (lkstimm@gmail.com)
   - Default organization set (Lukas's Organisation)
   - 30-day trial subscription activated (expires 2026-03-10)

2. **Broker Running**:
   - RemotiveBroker container running successfully
   - gRPC API accessible at `localhost:50051`
   - Web interface running at `http://localhost:8083`
   - CLI commands working: `remotive broker signals list`

3. **Configuration Files Created**:
   - `steering.dbc` - Custom steering signal definitions
   - `interfaces.json` - Virtual CAN bus configuration
   - Files mounted in broker container

## ⚠️ Current Issues

### macOS Docker Networking
- **Issue**: `network_mode: "host"` doesn't work on macOS
- **Solution Applied**: Changed to explicit port mappings
- **Result**: Broker now accessible via localhost

### Signal Loading
- Broker is running but hasn't loaded signals from DBC file yet
- Configuration files are mounted but may need activation via web interface
- Files uploaded to broker but show `:einval` error

## 🎯 Working Commands

```bash
# Check if broker is running
docker compose ps

# View broker logs
docker compose logs signal-broker

# Test broker connectivity
remotive broker signals list

# Upload configuration
remotive broker files upload configuration/interfaces.json

# Restart broker
docker compose restart signal-broker
```

## 🌐 Access Points

- **Broker gRPC**: http://localhost:50051
- **Web Interface**: http://localhost:8083
- **Configuration**: `./configuration/`

## 📝 Key Learnings

1. **macOS Docker Limitation**: Host networking (`network_mode: "host"`) doesn't work on macOS/Windows, only Linux
2. **Port Mappings Required**: Must explicitly map ports (50051, 4040, 4000) for macOS
3. **Credentials Mount**: RemotiveCloud credentials must be mounted: `~/.config/remotive:/root/.config/remotive:ro`
4. **Web Interface**: The web app may show "disconnected" if accessing via localhost:8083, but the broker API is working via CLI

## 🔧 Troubleshooting

### Web Interface Shows Blank/Disconnected
The web interface is a React app running in browser that needs to connect to the broker. On macOS with Docker, this sometimes has connectivity issues. **Use the CLI instead**:

```bash
# Set default broker URL
export REMOTIVE_BROKER_URL=http://localhost:50051

# All broker commands now use this URL
remotive broker signals list
remotive broker signals subscribe <signal-name>
```

### Signals Not Appearing
The broker may need the configuration to be activated through the web interface or API. The mounted files are visible but the broker needs to load them.

Alternative approach: Use RemotiveCloud brokers or access the web interface at localhost:8083 to manually upload and activate the configuration.

## 📚 Next Steps

1. **Access Web Interface**: Try http://localhost:8083 in browser
2. **Upload Config via Web**: Use web UI to upload and activate steering.dbc
3. **Or Use CLI**: Continue using `remotive broker` commands
4. **Create Scripts**: Build Python scripts to publish/subscribe to signals

## 🔗 Resources

- Broker Bootstrap: https://github.com/remotivelabs/remotivebroker-bootstrap
- RemotiveCloud Console: https://console.cloud.remotivelabs.com
- Documentation: https://docs.remotivelabs.com
