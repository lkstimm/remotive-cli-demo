#!/bin/bash

echo "🚗 RemotiveBroker Steering Demo"
echo "================================"
echo ""
echo "This demo shows how to:"
echo "  1. Check broker connectivity"
echo "  2. List available signals"
echo "  3. Monitor signals with CLI"
echo "  4. Use tshark to observe traffic"
echo ""

# Check broker
echo "1️⃣  Checking broker connection..."
if remotive broker signals list > /dev/null 2>&1; then
    echo "   ✅ Broker is running at localhost:50051"
else
    echo "   ❌ Broker not accessible"
    echo "   Start with: cd ../broker-setup && docker compose up -d"
    exit 1
fi
echo ""

# List signals
echo "2️⃣  Listing available signals..."
SIGNALS=$(remotive broker signals list)
if [ -z "$SIGNALS" ] || [ "$SIGNALS" = "[]" ]; then
    echo "   ⚠️  No signals currently configured"
    echo "   The broker is running but needs signal definitions loaded"
else
    echo "   Available signals:"
    echo "$SIGNALS" | python3 -m json.tool
fi
echo ""

# Show monitoring options
echo "3️⃣  Monitoring Options:"
echo ""
echo "   📊 Option A - Use Remotive CLI:"
echo "      remotive broker signals subscribe <signal-name>"
echo ""
echo "   🔍 Option B - Use tshark (Wireshark CLI):"
echo "      tshark -i lo0 -f 'tcp port 50051'"
echo ""
echo "   📈 Option C - Use Wireshark GUI:"
echo "      wireshark -i lo0 -f 'tcp port 50051'"
echo ""

# Offer to start tshark monitoring
echo "4️⃣  Start Traffic Monitoring?"
echo ""
read -p "   Start tshark monitoring? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔍 Starting tshark on loopback interface..."
    echo "   Monitoring port 50051 (broker gRPC)"
    echo "   Press Ctrl+C to stop"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Check if tshark is available
    if command -v tshark &> /dev/null; then
        sudo tshark -i lo0 -f "tcp port 50051" -Y "http2" 2>/dev/null || \
        sudo tshark -i lo0 -f "tcp port 50051" 2>/dev/null
    else
        echo "   ❌ tshark not found"
        echo "   Install with: brew install wireshark"
    fi
else
    echo ""
    echo "✅ Demo complete!"
    echo ""
    echo "📚 Next steps:"
    echo "   - List signals: remotive broker signals list"
    echo "   - Subscribe: remotive broker signals subscribe <name>"
    echo "   - View docs: https://docs.remotivelabs.com"
    echo ""
fi
