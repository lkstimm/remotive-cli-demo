#!/bin/bash

echo "📡 Generating Traffic to RemotiveBroker"
echo "========================================"
echo ""
echo "This script makes repeated API calls to the broker"
echo "Run tshark in another terminal to observe the traffic:"
echo ""
echo "  sudo tshark -i lo0 -f 'tcp port 50051'"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Counter
COUNT=0

while true; do
    COUNT=$((COUNT + 1))
    echo -ne "\r📤 API Call #$COUNT - $(date '+%H:%M:%S')"

    # Make API call to broker
    remotive broker signals list > /dev/null 2>&1

    sleep 1
done
