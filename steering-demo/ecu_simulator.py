#!/usr/bin/env python3
"""
Steering ECU Simulator
Subscribes to steering commands and publishes current status
"""

import time
from remotivelabs.broker.sync import SignalCreator, SubscriberConfig, PublisherConfig, create_channel

BROKER_URL = "http://localhost:50051"

class SteeringECU:
    def __init__(self):
        self.current_angle = 0.0
        self.target_angle = 0.0
        self.ready = True

    def update(self, dt=0.1):
        """Update ECU state - smoothly move towards target angle"""
        if abs(self.target_angle - self.current_angle) > 1:
            # Move towards target at specified speed
            diff = self.target_angle - self.current_angle
            step = min(abs(diff), 50 * dt)  # Max 50 deg/s movement
            self.current_angle += step if diff > 0 else -step
        else:
            self.current_angle = self.target_angle

    def set_target(self, angle):
        """Set new target steering angle"""
        self.target_angle = max(-2000, min(2000, angle))  # Clamp to valid range

def main():
    print("🎮 Steering ECU Simulator")
    print(f"📡 Connecting to broker at {BROKER_URL}...")

    channel = create_channel(BROKER_URL)
    ecu = SteeringECU()

    # Subscribe to steering commands
    subscriber_config = SubscriberConfig(
        clientId="steering_ecu",
        signals=SignalCreator()
            .signal("SteeringCommand", "SteeringAngle")
            .signal("SteeringCommand", "SteeringSpeed"),
        onChange=True
    )

    # Publisher for status
    publisher_config = PublisherConfig(
        clientId="steering_ecu_status",
        signals=SignalCreator()
            .signal("SteeringStatus", "CurrentAngle")
            .signal("SteeringStatus", "ECU_Ready")
    )

    print("✓ Connected to broker")
    print("\n🎯 ECU ready - listening for steering commands...\n")

    try:
        last_update = time.time()

        while True:
            # Read incoming steering commands
            try:
                for signal in subscriber_config.signals:
                    value = signal.read()
                    if signal.signal_name == "SteeringAngle":
                        target_angle = value / 10.0  # Convert from raw value
                        ecu.set_target(target_angle)
                        print(f"📥 Received command: Target = {target_angle:6.1f}°")
            except Exception as e:
                pass  # No new data

            # Update ECU state
            current_time = time.time()
            dt = current_time - last_update
            ecu.update(dt)
            last_update = current_time

            # Publish current status
            publisher_config.signals.signal("SteeringStatus", "CurrentAngle").raw(int(ecu.current_angle * 10))
            publisher_config.signals.signal("SteeringStatus", "ECU_Ready").raw(1 if ecu.ready else 0)

            print(f"📤 ECU Status: Current = {ecu.current_angle:6.1f}° | Target = {ecu.target_angle:6.1f}°")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\n⏹️  ECU simulator stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
