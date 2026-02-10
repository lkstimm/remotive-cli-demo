#!/usr/bin/env python3
"""
Steering Command Publisher
Publishes steering angle commands to the RemotiveBroker
"""

import time
import math
from remotivelabs.broker.sync import SignalCreator, PublisherConfig, create_channel

BROKER_URL = "http://localhost:50051"

def main():
    print("🚗 Steering Command Publisher")
    print(f"📡 Connecting to broker at {BROKER_URL}...")

    # Create channel to broker
    channel = create_channel(BROKER_URL)

    # Create signal publisher
    publisher_config = PublisherConfig(
        clientId="steering_gateway",
        signals=SignalCreator()
            .signal("SteeringCommand", "SteeringAngle")
            .signal("SteeringCommand", "SteeringSpeed")
    )

    print("✓ Connected to broker")
    print("\n📊 Publishing steering commands...")
    print("   (Sine wave pattern: -500° to +500°)\n")

    try:
        # Publish steering commands in a sine wave pattern
        angle = 0
        while True:
            # Generate sine wave steering angle (-500 to +500 degrees)
            steering_angle = 500 * math.sin(angle)
            steering_speed = 100  # degrees per second

            # Publish signals
            publisher_config.signals.signal("SteeringCommand", "SteeringAngle").raw(int(steering_angle * 10))
            publisher_config.signals.signal("SteeringCommand", "SteeringSpeed").raw(int(steering_speed))

            print(f"📤 Steering Angle: {steering_angle:6.1f}° | Speed: {steering_speed} deg/s")

            # Increment angle
            angle += 0.1
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\n⏹️  Publisher stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
