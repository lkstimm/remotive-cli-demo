#!/usr/bin/env python3
"""
Modern CAN Bus Network Topology Visualizer
Uses NetworkX for professional graph rendering with animated message flow
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from collections import deque
import numpy as np
import time
import math

# Configuration
MAX_POINTS = 50  # Reduced from 100 to reduce memory
UPDATE_INTERVAL = 100  # Increased from 50ms to 100ms (10 FPS instead of 20 FPS)

class ModernCANTopology:
    def __init__(self):
        # Data buffers
        self.times = deque(maxlen=MAX_POINTS)
        self.commands = deque(maxlen=MAX_POINTS)
        self.responses = deque(maxlen=MAX_POINTS)

        # Simulation state
        self.current_angle = 0.0
        self.target_angle = 0.0
        self.start_time = time.time()
        self.message_activity = {'command': 0, 'status': 0}

        # Create network graph
        self.G = nx.DiGraph()
        self._build_network()

        # Create figure
        self.fig = plt.figure(figsize=(18, 10))
        gs = self.fig.add_gridspec(2, 2, height_ratios=[2, 1], width_ratios=[1.5, 1],
                                   hspace=0.3, wspace=0.3)

        # Network topology (left side, spans both rows)
        self.ax_network = self.fig.add_subplot(gs[:, 0])

        # Data plots (right side)
        self.ax_cmd = self.fig.add_subplot(gs[0, 1])
        self.ax_resp = self.fig.add_subplot(gs[1, 1])

        self.fig.suptitle('CAN Bus Network Topology - Real-time Visualization',
                         fontsize=16, fontweight='bold')

        # Setup
        self._setup_network_view()
        self._setup_data_plots()

    def _build_network(self):
        """Build the network graph using NetworkX"""
        # Add nodes with attributes
        self.G.add_node('Gateway',
                       node_type='ecu',
                       color='lightblue',
                       size=3000,
                       label='Gateway\n(Publisher)')

        self.G.add_node('RemotiveBroker',
                       node_type='broker',
                       color='lightgreen',
                       size=4000,
                       label='RemotiveBroker\nlocalhost:50051')

        self.G.add_node('Steering_ECU',
                       node_type='ecu',
                       color='lightcoral',
                       size=3000,
                       label='Steering ECU\n(Subscriber)')

        self.G.add_node('CAN_Bus',
                       node_type='bus',
                       color='gold',
                       size=2500,
                       label='Virtual CAN\nSteeringBus')

        # Add edges with message types
        # Gateway publishes commands to bus
        self.G.add_edge('Gateway', 'CAN_Bus',
                       message='SteeringCommand',
                       msg_id='100',
                       direction='TX',
                       color='blue',
                       weight=2)

        # Bus routes to broker
        self.G.add_edge('CAN_Bus', 'RemotiveBroker',
                       message='CAN Traffic',
                       msg_id='*',
                       direction='RX/TX',
                       color='gray',
                       weight=3)

        # Broker routes to ECU
        self.G.add_edge('RemotiveBroker', 'Steering_ECU',
                       message='SteeringCommand',
                       msg_id='100',
                       direction='RX',
                       color='blue',
                       weight=2)

        # ECU responds with status
        self.G.add_edge('Steering_ECU', 'RemotiveBroker',
                       message='SteeringStatus',
                       msg_id='200',
                       direction='TX',
                       color='red',
                       weight=2)

        # Broker routes back to bus
        self.G.add_edge('RemotiveBroker', 'CAN_Bus',
                       message='CAN Traffic',
                       msg_id='*',
                       direction='RX/TX',
                       color='gray',
                       weight=3)

        # Bus delivers to gateway
        self.G.add_edge('CAN_Bus', 'Gateway',
                       message='SteeringStatus',
                       msg_id='200',
                       direction='RX',
                       color='red',
                       weight=2)

    def _setup_network_view(self):
        """Setup the network topology visualization"""
        self.ax_network.clear()
        self.ax_network.set_title('CAN Bus Network Architecture',
                                 fontsize=14, fontweight='bold', pad=20)
        self.ax_network.axis('off')

        # Use better spacing for clear visualization
        # Arrange in a diamond/star pattern with broker in center
        pos = {
            'Gateway': (0, 1),           # Left
            'CAN_Bus': (1, 2),           # Top
            'RemotiveBroker': (1, 1),    # Center
            'Steering_ECU': (2, 1)       # Right
        }
        self.pos = pos

        # Adjust axis limits for better view
        self.ax_network.set_xlim(-0.5, 2.5)
        self.ax_network.set_ylim(0.3, 2.7)

        # Draw boundary boxes to separate RemotiveLabs infrastructure from demo
        from matplotlib.patches import FancyBboxPatch

        # RemotiveLabs Infrastructure box (covers broker and CAN bus)
        remotive_box = FancyBboxPatch(
            (0.4, 0.5), 1.3, 1.9,
            boxstyle="round,pad=0.05",
            facecolor='lightgreen',
            edgecolor='darkgreen',
            linewidth=3,
            alpha=0.15,
            zorder=0
        )
        self.ax_network.add_patch(remotive_box)
        self.ax_network.text(1.05, 2.55, 'RemotiveLabs Infrastructure',
                           ha='center', fontsize=10, fontweight='bold',
                           color='darkgreen', bbox=dict(boxstyle='round,pad=0.3',
                                                       facecolor='lightgreen',
                                                       alpha=0.8))

        # Demo/Simulation box (covers gateway and ECU)
        demo_box_left = FancyBboxPatch(
            (-0.4, 0.5), 0.7, 1.0,
            boxstyle="round,pad=0.05",
            facecolor='lightyellow',
            edgecolor='orange',
            linewidth=3,
            alpha=0.15,
            zorder=0
        )
        self.ax_network.add_patch(demo_box_left)

        demo_box_right = FancyBboxPatch(
            (1.8, 0.5), 0.7, 1.0,
            boxstyle="round,pad=0.05",
            facecolor='lightyellow',
            edgecolor='orange',
            linewidth=3,
            alpha=0.15,
            zorder=0
        )
        self.ax_network.add_patch(demo_box_right)

        self.ax_network.text(-0.05, 0.45, 'Demo Code',
                           ha='center', fontsize=9, fontweight='bold',
                           color='darkorange', bbox=dict(boxstyle='round,pad=0.3',
                                                        facecolor='lightyellow',
                                                        alpha=0.8))
        self.ax_network.text(2.15, 0.45, 'Demo Code',
                           ha='center', fontsize=9, fontweight='bold',
                           color='darkorange', bbox=dict(boxstyle='round,pad=0.3',
                                                        facecolor='lightyellow',
                                                        alpha=0.8))

        # Get node attributes
        node_colors = [self.G.nodes[node]['color'] for node in self.G.nodes()]
        node_sizes = [self.G.nodes[node]['size'] for node in self.G.nodes()]
        node_labels = {node: self.G.nodes[node]['label'] for node in self.G.nodes()}

        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos,
                              node_color=node_colors,
                              node_size=node_sizes,
                              node_shape='o',
                              alpha=0.9,
                              ax=self.ax_network,
                              edgecolors='black',
                              linewidths=2)

        # Draw node labels
        nx.draw_networkx_labels(self.G, pos,
                               labels=node_labels,
                               font_size=9,
                               font_weight='bold',
                               ax=self.ax_network)

        # Store edge artists for animation
        self.edge_artists = {}

    def _draw_animated_edges(self):
        """Draw edges with animation based on message activity"""
        # Remove old edge drawings
        for artist in self.edge_artists.values():
            if artist in self.ax_network.collections or artist in self.ax_network.patches:
                artist.remove()
        self.edge_artists.clear()

        # Draw each edge with appropriate styling
        for edge in self.G.edges(data=True):
            src, dst, data = edge

            # Calculate edge intensity based on message type
            alpha = 0.4
            width = data.get('weight', 1)

            # Animate command flow (blue edges)
            if data.get('color') == 'blue':
                if self.message_activity['command'] > 0:
                    alpha = 0.9
                    width = width * 1.5

            # Animate status flow (red edges)
            elif data.get('color') == 'red':
                if self.message_activity['status'] > 0:
                    alpha = 0.9
                    width = width * 1.5

            # Draw edge
            edge_collection = nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=[(src, dst)],
                edge_color=data.get('color', 'gray'),
                width=width,
                alpha=alpha,
                arrows=True,
                arrowsize=20,
                arrowstyle='->',
                connectionstyle='arc3,rad=0.1',
                ax=self.ax_network
            )

            if edge_collection:
                self.edge_artists[f"{src}-{dst}"] = edge_collection

        # Draw edge labels (message info)
        edge_labels = {}
        for src, dst, data in self.G.edges(data=True):
            if data.get('message'):
                label = f"{data['message']}\n(ID: {data.get('msg_id', '?')})"
                edge_labels[(src, dst)] = label

        nx.draw_networkx_edge_labels(self.G, self.pos,
                                     edge_labels=edge_labels,
                                     font_size=7,
                                     font_color='darkblue',
                                     bbox=dict(boxstyle='round,pad=0.3',
                                             facecolor='white',
                                             alpha=0.7,
                                             edgecolor='none'),
                                     ax=self.ax_network)

        # Decay message activity
        if self.message_activity['command'] > 0:
            self.message_activity['command'] -= 1
        if self.message_activity['status'] > 0:
            self.message_activity['status'] -= 1

        # Add legend
        self._add_legend()

    def _add_legend(self):
        """Add legend for network elements"""
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w',
                      markerfacecolor='lightblue', markersize=10,
                      label='Gateway (Publisher)', markeredgecolor='black'),
            plt.Line2D([0], [0], marker='o', color='w',
                      markerfacecolor='lightgreen', markersize=12,
                      label='RemotiveBroker', markeredgecolor='black'),
            plt.Line2D([0], [0], marker='o', color='w',
                      markerfacecolor='lightcoral', markersize=10,
                      label='ECU (Subscriber)', markeredgecolor='black'),
            plt.Line2D([0], [0], marker='o', color='w',
                      markerfacecolor='gold', markersize=10,
                      label='CAN Bus', markeredgecolor='black'),
            plt.Line2D([0], [0], color='blue', linewidth=3,
                      label='Command Flow (ID 100)'),
            plt.Line2D([0], [0], color='red', linewidth=3,
                      label='Status Flow (ID 200)')
        ]

        self.ax_network.legend(handles=legend_elements,
                              loc='upper left',
                              fontsize=8,
                              framealpha=0.9)

    def _setup_data_plots(self):
        """Setup the data visualization plots"""
        # Command plot
        self.line_cmd, = self.ax_cmd.plot([], [], 'b-', linewidth=2,
                                          label='TX: SteeringCommand')
        self.ax_cmd.set_ylabel('Angle (°)', fontsize=10)
        self.ax_cmd.set_title('CAN ID 100: SteeringCommand',
                             fontsize=11, fontweight='bold')
        self.ax_cmd.grid(True, alpha=0.3)
        self.ax_cmd.legend(loc='upper right', fontsize=8)
        self.ax_cmd.set_ylim(-600, 600)

        # Response plot
        self.line_resp, = self.ax_resp.plot([], [], 'r-', linewidth=2,
                                            label='RX: SteeringStatus')
        self.ax_resp.set_xlabel('Time (seconds)', fontsize=10)
        self.ax_resp.set_ylabel('Angle (°)', fontsize=10)
        self.ax_resp.set_title('CAN ID 200: SteeringStatus',
                              fontsize=11, fontweight='bold')
        self.ax_resp.grid(True, alpha=0.3)
        self.ax_resp.legend(loc='upper right', fontsize=8)
        self.ax_resp.set_ylim(-600, 600)

    def generate_command(self, t):
        """Generate realistic steering command"""
        base = 500 * math.sin(t * 0.5)
        noise = 50 * math.sin(t * 2.3) + 30 * math.sin(t * 3.7)
        return base + noise

    def update_ecu(self, command, dt=0.05):
        """Simulate ECU response with lag"""
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

        # Trigger message activity (less frequent)
        if frame % 20 == 0:
            self.message_activity['command'] = 10
        if frame % 20 == 10:
            self.message_activity['status'] = 10

        # Update network topology (only every 2 frames to reduce load)
        if frame % 2 == 0:
            self._draw_animated_edges()

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

        # Update title
        status = (f'Live CAN Traffic | Command: {command:6.1f}° | '
                 f'ECU Response: {response:6.1f}° | Lag: {abs(command-response):5.1f}°')
        self.fig.suptitle(status, fontsize=12, fontweight='bold')

        return [self.line_cmd, self.line_resp]

    def run(self):
        """Start the visualization"""
        print("=" * 80)
        print("  Modern CAN Bus Network Topology Visualizer")
        print("=" * 80)
        print()
        print("Network Architecture:")
        print("  • Gateway (blue) → CAN Bus → RemotiveBroker → Steering ECU (red)")
        print("  • Watch edges light up as messages flow through the network!")
        print()
        print("Message Flow:")
        print("  • Blue edges: SteeringCommand (ID 100) - Gateway → ECU")
        print("  • Red edges: SteeringStatus (ID 200) - ECU → Gateway")
        print("  • Gray edges: CAN Bus infrastructure")
        print()
        print("Real-time Data:")
        print("  • Top-right: Command signals from Gateway")
        print("  • Bottom-right: Response signals from ECU")
        print()
        print("Close window to stop.")
        print("=" * 80)
        print()

        ani = animation.FuncAnimation(
            self.fig,
            self.update,
            interval=UPDATE_INTERVAL,
            blit=False,
            cache_frame_data=False
        )

        plt.tight_layout()
        plt.show()

def main():
    try:
        viz = ModernCANTopology()
        viz.run()
    except KeyboardInterrupt:
        print("\n\nVisualization stopped")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
