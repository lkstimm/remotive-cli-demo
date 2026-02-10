#!/bin/bash

# Steering Demo Runner
# This script runs the complete demo with multiple terminals

echo "🚗 RemotiveBroker Steering Demo"
echo "================================"
echo ""

# Check if broker is running
if ! curl -s http://localhost:50051 > /dev/null 2>&1; then
    echo "❌ Error: Broker not running at localhost:50051"
    echo "   Start it with: cd ../broker-setup && docker compose up -d"
    exit 1
fi

echo "✓ Broker is running"
echo ""

# Activate virtual environment
source venv/bin/activate

echo "📋 Demo Components:"
echo "   1. Publisher  - Sends steering commands (sine wave)"
echo "   2. ECU        - Simulates steering ECU, responds to commands"
echo "   3. Monitor    - Uses remotive CLI to monitor signals"
echo ""
echo "🎬 Starting demo..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all components..."
    kill $PUB_PID $ECU_PID $MON_PID 2>/dev/null
    wait
    echo "✓ Demo stopped"
}

trap cleanup EXIT INT TERM

# Start publisher in background
echo "▶️  Starting Publisher..."
python3 publisher.py &
PUB_PID=$!
sleep 2

# Start ECU simulator in background
echo "▶️  Starting ECU Simulator..."
python3 ecu_simulator.py &
ECU_PID=$!
sleep 2

# Monitor signals using CLI
echo "▶️  Monitoring signals..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Press Ctrl+C to stop the demo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Use remotive CLI to subscribe to signals
remotive broker signals subscribe SteeringCommand.SteeringAngle SteeringStatus.CurrentAngle

# Wait for background processes
wait
