#!/usr/bin/env python3
"""
CAN Bus Topology & Real-time Data Visualizer
Shows the deployed topology with ECU nodes and live message flow
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import networkx as nx
from collections import deque
import numpy as np
import time
import math

# Configuration
MAX_POINTS = 100
UPDATE_INTERVAL = 50

class CANTopologyVisualizer:
    def __init__(self):
        # Data buffers
        self.times = deque(maxlen=MAX_POINTS)
        self.commands = deque(maxlen=MAX_POINTS)
        self.responses = deque(maxlen=MAX_POINTS)

        # Simulation state
        self.current_angle = 0.0
        self.target_angle = 0.0
        self.start_time = time.time()
        self.message_flash = {'command': 0, 'status': 0}

        # Create figure with 3 sections
        self.fig = plt.figure(figsize=(16, 10))
        gs = self.fig.add_gridspec(3, 2, height_ratios=[1.5, 1, 1], hspace=0.3, wspace=0.3)

        # Topology diagram (top, spans both columns)
        self.ax_topo = self.fig.add_subplot(gs[0, :])

        # Data plots (bottom)
        self.ax_cmd = self.fig.add_subplot(gs[1, :])
        self.ax_resp = self.fig.add_subplot(gs[2, :])

        self.fig.suptitle('CAN Bus Topology & Real-time Signal Flow',
                         fontsize=16, fontweight='bold')

        # Initialize topology
        self._setup_topology()

        # Initialize data plots
        self._setup_data_plots()

    def _setup_topology(self):
        """Draw the CAN bus topology diagram"""
        self.ax_topo.clear()
        self.ax_topo.set_xlim(0, 10)
        self.ax_topo.set_ylim(0, 6)
        self.ax_topo.axis('off')
        self.ax_topo.set_title('CAN Bus Topology - SteeringBus (Virtual CAN)',
                               fontsize=14, fontweight='bold', pad=20)

        # Define positions
        self.positions = {
            'gateway': (2, 4),
            'broker': (5, 3),
            'ecu': (8, 4),
            'bus': [(1, 2.5), (9, 2.5)]
        }

        # Draw CAN bus line
        bus_y = 2.5
        self.ax_topo.plot([1, 9], [bus_y, bus_y], 'k-', linewidth=4, label='CAN Bus')
        self.ax_topo.text(5, bus_y - 0.4, 'Virtual CAN Bus (SteeringBus)',
                         ha='center', fontsize=10, style='italic')

        # Draw Gateway node
        gw_box = FancyBboxPatch((1.3, 3.5), 1.4, 1,
                               boxstyle="round,pad=0.1",
                               facecolor='lightblue',
                               edgecolor='blue', linewidth=2)
        self.ax_topo.add_patch(gw_box)
        self.ax_topo.text(2, 4.5, 'Gateway', ha='center', fontsize=11, fontweight='bold')
        self.ax_topo.text(2, 4.0, 'Publishes:', ha='center', fontsize=8)
        self.ax_topo.text(2, 3.75, 'SteeringCommand', ha='center', fontsize=8, style='italic')

        # Draw connection from Gateway to bus
        self.ax_topo.plot([2, 2], [3.5, bus_y], 'b--', linewidth=1.5, alpha=0.6)

        # Draw RemotiveBroker
        broker_box = FancyBboxPatch((4.0, 2.3), 2, 1.4,
                                   boxstyle="round,pad=0.1",
                                   facecolor='lightgreen',
                                   edgecolor='green', linewidth=3)
        self.ax_topo.add_patch(broker_box)
        self.ax_topo.text(5, 3.4, 'RemotiveBroker', ha='center', fontsize=12, fontweight='bold')
        self.ax_topo.text(5, 3.0, 'localhost:50051', ha='center', fontsize=8)
        self.ax_topo.text(5, 2.7, 'Routes CAN messages', ha='center', fontsize=8, style='italic')
        self.ax_topo.text(5, 2.45, 'Signal DB: steering.dbc', ha='center', fontsize=7, style='italic')

        # Draw Steering ECU node
        ecu_box = FancyBboxPatch((7.3, 3.5), 1.4, 1,
                                boxstyle="round,pad=0.1",
                                facecolor='lightcoral',
                                edgecolor='red', linewidth=2)
        self.ax_topo.add_patch(ecu_box)
        self.ax_topo.text(8, 4.5, 'Steering ECU', ha='center', fontsize=11, fontweight='bold')
        self.ax_topo.text(8, 4.0, 'Subscribes:', ha='center', fontsize=8)
        self.ax_topo.text(8, 3.75, 'SteeringCommand', ha='center', fontsize=8, style='italic')

        # Draw connection from ECU to bus
        self.ax_topo.plot([8, 8], [3.5, bus_y], 'r--', linewidth=1.5, alpha=0.6)

        # Store arrow objects for animation
        self.arrow_cmd = None
        self.arrow_resp = None

        # Add legend for messages
        legend_y = 5.5
        self.ax_topo.text(0.5, legend_y, 'CAN Messages:', fontsize=10, fontweight='bold')

        # Command message (ID: 100)
        cmd_arrow = mpatches.FancyArrow(1, legend_y - 0.5, 1, 0,
                                       width=0.15, color='blue', alpha=0.7)
        self.ax_topo.add_patch(cmd_arrow)
        self.ax_topo.text(2.5, legend_y - 0.5, 'ID 100: SteeringCommand',
                         fontsize=9, va='center')

        # Status message (ID: 200)
        status_arrow = mpatches.FancyArrow(5, legend_y - 0.5, 1, 0,
                                          width=0.15, color='red', alpha=0.7)
        self.ax_topo.add_patch(status_arrow)
        self.ax_topo.text(6.5, legend_y - 0.5, 'ID 200: SteeringStatus',
                         fontsize=9, va='center')

    def _setup_data_plots(self):
        """Setup the data visualization plots"""
        # Command plot
        self.line_cmd, = self.ax_cmd.plot([], [], 'b-', linewidth=2,
                                          label='Steering Command (Gateway TX)')
        self.ax_cmd.set_ylabel('Angle (°)', fontsize=11)
        self.ax_cmd.set_title('CAN Message ID 100: SteeringCommand', fontsize=11, fontweight='bold')
        self.ax_cmd.grid(True, alpha=0.3)
        self.ax_cmd.legend(loc='upper right')
        self.ax_cmd.set_ylim(-600, 600)

        # Response plot
        self.line_resp, = self.ax_resp.plot([], [], 'r-', linewidth=2,
                                            label='ECU Response (ECU TX)')
        self.ax_resp.set_xlabel('Time (seconds)', fontsize=11)
        self.ax_resp.set_ylabel('Angle (°)', fontsize=11)
        self.ax_resp.set_title('CAN Message ID 200: SteeringStatus', fontsize=11, fontweight='bold')
        self.ax_resp.grid(True, alpha=0.3)
        self.ax_resp.legend(loc='upper right')
        self.ax_resp.set_ylim(-600, 600)

    def _draw_message_arrows(self):
        """Draw animated message flow arrows"""
        # Remove old arrows
        if self.arrow_cmd:
            self.arrow_cmd.remove()
        if self.arrow_resp:
            self.arrow_resp.remove()

        # Command arrow intensity based on flash counter
        cmd_alpha = max(0.3, 1.0 - self.message_flash['command'] / 10.0)

        # Command: Gateway -> Broker -> ECU
        self.arrow_cmd = FancyArrowPatch(
            (2.7, 4), (7.3, 4),
            arrowstyle='->', mutation_scale=30,
            linewidth=3, color='blue', alpha=cmd_alpha,
            connectionstyle="arc3,rad=.2"
        )
        self.ax_topo.add_patch(self.arrow_cmd)

        # Status arrow intensity
        resp_alpha = max(0.3, 1.0 - self.message_flash['status'] / 10.0)

        # Status: ECU -> Broker -> Gateway
        self.arrow_resp = FancyArrowPatch(
            (7.3, 3.7), (2.7, 3.7),
            arrowstyle='->', mutation_scale=30,
            linewidth=3, color='red', alpha=resp_alpha,
            connectionstyle="arc3,rad=.2"
        )
        self.ax_topo.add_patch(self.arrow_resp)

        # Decay flash counters
        if self.message_flash['command'] > 0:
            self.message_flash['command'] -= 1
        if self.message_flash['status'] > 0:
            self.message_flash['status'] -= 1

    def generate_command(self, t):
        """Generate realistic steering command"""
        base = 500 * math.sin(t * 0.5)
        noise = 50 * math.sin(t * 2.3) + 30 * math.sin(t * 3.7)
        return base + noise

    def update_ecu(self, command, dt=0.05):
        """Simulate ECU response"""
        self.target_angle = command
        diff = self.target_angle - self.current_angle
        max_change = 150 * dt

        if abs(diff) > max_change:
            step = max_change if diff > 0 else -max_change
        else:
            step = diff

        self.current_angle += step
        return self.current_angle

    def update(self, frame):
        """Animation update function"""
        t = time.time() - self.start_time

        # Generate new data
        command = self.generate_command(t)
        response = self.update_ecu(command)

        # Trigger message flash
        if frame % 20 == 0:  # Flash every 20 frames
            self.message_flash['command'] = 10
        if frame % 20 == 10:  # Offset status flash
            self.message_flash['status'] = 10

        # Update topology arrows
        self._draw_message_arrows()

        # Store data
        self.times.append(t)
        self.commands.append(command)
        self.responses.append(response)

        # Update data plots
        if len(self.times) > 1:
            times_list = list(self.times)

            self.line_cmd.set_data(times_list, list(self.commands))
            self.ax_cmd.set_xlim(max(0, t - 10), t + 1)

            self.line_resp.set_data(times_list, list(self.responses))
            self.ax_resp.set_xlim(max(0, t - 10), t + 1)

        # Update title with current values
        status = f'CAN Bus Activity | Command: {command:6.1f}° | ECU: {response:6.1f}° | Lag: {abs(command-response):5.1f}°'
        self.fig.suptitle(status, fontsize=13, fontweight='bold')

        return [self.line_cmd, self.line_resp]

    def run(self):
        """Start the visualization"""
        print("=" * 70)
        print("  CAN Bus Topology & Real-time Visualizer")
        print("=" * 70)
        print()
        print("Topology Diagram:")
        print("  • Gateway (Blue)      - Publishes SteeringCommand messages")
        print("  • RemotiveBroker      - Routes CAN messages")
        print("  • Steering ECU (Red)  - Subscribes and responds")
        print()
        print("Live Data:")
        print("  • Top plot: CAN TX from Gateway (ID 100)")
        print("  • Bottom plot: CAN RX from ECU (ID 200)")
        print()
        print("Watch the animated arrows show message flow!")
        print("Close window to stop.")
        print("=" * 70)
        print()

        ani = animation.FuncAnimation(
            self.fig,
            self.update,
            interval=UPDATE_INTERVAL,
            blit=False,
            cache_frame_data=False
        )

        plt.show()

def main():
    try:
        viz = CANTopologyVisualizer()
        viz.run()
    except KeyboardInterrupt:
        print("\n\nVisualization stopped")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
