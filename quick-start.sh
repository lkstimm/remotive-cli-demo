#!/bin/bash

# Remotive CLI Quick Start Demo Script
# This script demonstrates basic Remotive CLI commands

echo "==================================="
echo "Remotive CLI Quick Start Demo"
echo "==================================="
echo ""

# 1. Check version
echo "1. Checking Remotive CLI version..."
remotive --version
echo ""

# 2. Check topology version
echo "2. Checking RemotiveTopology version..."
remotive topology version
echo ""

# 3. Check subscription status
echo "3. Checking subscription status..."
remotive topology subscription status
echo ""

# 4. Discover brokers
echo "4. Discovering brokers on network..."
echo "(This may take a moment...)"
remotive broker discover
echo ""

# 5. Show available commands
echo "5. Main command categories:"
echo "   - topology: Manage signal databases and ECU configurations"
echo "   - broker: Interact with brokers (local or cloud)"
echo "   - cloud: Manage cloud resources"
echo "   - tools: Additional utilities"
echo "   - tui: Interactive text interface"
echo ""

echo "==================================="
echo "Demo Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "  - Try the interactive TUI: remotive tui"
echo "  - Read the README.md for more examples"
echo "  - Visit https://docs.remotivelabs.com for full documentation"
echo ""
