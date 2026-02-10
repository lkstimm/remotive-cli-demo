#!/usr/bin/env python3
"""
Real-time Steering CAN Bus Visualizer
Shows simulated CAN traffic: input commands and ECU output
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np
import time
import math

# Configuration
MAX_POINTS = 100  # Show last 100 data points
UPDATE_INTERVAL = 50  # Update every 50ms

class SteeringSimulator:
    def __init__(self):
        # Data buffers
        self.times = deque(maxlen=MAX_POINTS)
        self.commands = deque(maxlen=MAX_POINTS)  # Input: steering commands
        self.responses = deque(maxlen=MAX_POINTS)  # Output: ECU response

        # Simulation state
        self.current_angle = 0.0
        self.target_angle = 0.0
        self.start_time = time.time()

        # Create figure with two subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.fig.suptitle('🚗 CAN Bus Steering Simulation - Real-time Visualization',
                         fontsize=16, fontweight='bold')

        # Initialize plots
        self.line_command, = self.ax1.plot([], [], 'b-', linewidth=2, label='Steering Command (Input)')
        self.line_response, = self.ax2.plot([], [], 'r-', linewidth=2, label='ECU Response (Output)')

        # Configure axes
        self._setup_axes()

    def _setup_axes(self):
        """Configure plot axes"""
        # Command plot (top)
        self.ax1.set_ylabel('Angle (degrees)', fontsize=12)
        self.ax1.set_title('CAN TX: Gateway → ECU (SteeringCommand)', fontsize=12)
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(loc='upper right')
        self.ax1.set_ylim(-600, 600)

        # Response plot (bottom)
        self.ax2.set_xlabel('Time (seconds)', fontsize=12)
        self.ax2.set_ylabel('Angle (degrees)', fontsize=12)
        self.ax2.set_title('CAN RX: ECU → Gateway (SteeringStatus)', fontsize=12)
        self.ax2.grid(True, alpha=0.3)
        self.ax2.legend(loc='upper right')
        self.ax2.set_ylim(-600, 600)

        plt.tight_layout()

    def generate_command(self, t):
        """Generate realistic steering command (sine wave + noise)"""
        # Main sine wave pattern
        base = 500 * math.sin(t * 0.5)

        # Add smaller oscillations for realism
        noise = 50 * math.sin(t * 2.3) + 30 * math.sin(t * 3.7)

        return base + noise

    def update_ecu(self, command, dt=0.05):
        """Simulate ECU response with realistic lag and smoothing"""
        self.target_angle = command

        # ECU responds with damping (can't follow instantly)
        diff = self.target_angle - self.current_angle
        max_change = 150 * dt  # Max 150 degrees per second

        if abs(diff) > max_change:
            step = max_change if diff > 0 else -max_change
        else:
            step = diff

        self.current_angle += step
        return self.current_angle

    def update(self, frame):
        """Animation update function"""
        # Get current time
        t = time.time() - self.start_time

        # Generate new command
        command = self.generate_command(t)

        # ECU processes command
        response = self.update_ecu(command)

        # Store data
        self.times.append(t)
        self.commands.append(command)
        self.responses.append(response)

        # Update plots
        if len(self.times) > 1:
            times_list = list(self.times)

            # Update command line
            self.line_command.set_data(times_list, list(self.commands))
            self.ax1.set_xlim(max(0, t - 10), t + 1)

            # Update response line
            self.line_response.set_data(times_list, list(self.responses))
            self.ax2.set_xlim(max(0, t - 10), t + 1)

        # Update status in title
        status = f'🚗 CAN Bus Steering Simulation | Command: {command:6.1f}° | ECU Output: {response:6.1f}° | Δ: {abs(command-response):5.1f}°'
        self.fig.suptitle(status, fontsize=12, fontweight='bold')

        return self.line_command, self.line_response

    def run(self):
        """Start the visualization"""
        print("🚗 Starting Steering CAN Bus Visualizer...")
        print("📊 Real-time graph showing:")
        print("   • Top plot: CAN TX - Steering commands (Gateway → ECU)")
        print("   • Bottom plot: CAN RX - ECU responses (ECU → Gateway)")
        print("")
        print("💡 Notice the delay between command and response (realistic ECU lag)")
        print("⏸️  Close the window to stop")
        print("")

        # Create animation
        ani = animation.FuncAnimation(
            self.fig,
            self.update,
            interval=UPDATE_INTERVAL,
            blit=True,
            cache_frame_data=False
        )

        plt.show()

def main():
    """Main entry point"""
    try:
        sim = SteeringSimulator()
        sim.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Visualization stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
