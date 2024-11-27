import matplotlib.pyplot as plt
import networkx as nx
import json
from itertools import permutations
from geopy.distance import geodesic
from package.tarjan_planner.logger import log_execution_time

class Route:
    @log_execution_time
    def __init__(self, transport_modes: json, locations: json, bicycle_available=False, prioritize_cost=False) -> None:
        """Transport modes and locations takes in JSON files, where locations is a list"""
        # Define transportation modes
        with open(transport_modes, 'r') as file:
            try:
                self.transport = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in {transport_modes}: {e}")

        with open(locations, 'r') as file:
            try:
                self.nodes = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in {locations}: {e}")

        self.bicycle_available = bicycle_available
        self.prioritize_cost = prioritize_cost
        self.best_route = False
        self.best_distance = False
        self.edge_colors = []
        self.route_description = []
        self.total_time = 0  # Total time in hours
        self.total_cost = 0  # Total cost of the trip
        
        self.distance_matrix = [[0] * len(self.nodes) for _ in range(len(self.nodes))]

        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                dist = geodesic(
                    (self.nodes[i]["latitude"], self.nodes[i]["longitude"]),
                    (self.nodes[j]["latitude"], self.nodes[j]["longitude"]),
                ).kilometers
                self.distance_matrix[i][j] = dist
                self.distance_matrix[j][i] = dist
        
        
        if not self.best_route and not self.best_distance:
            self.get_shortest_route()

        for i in range(len(self.best_route) - 1):
            start, end = self.best_route[i], self.best_route[i + 1]
            distance = self.distance_matrix[start][end]
            mode = self.determine_transport_mode(distance)
            self.edge_colors.append(self.transport[mode]["color"])

            speed = self.transport[mode]["speed"]
            cost = self.transport[mode]["cost"]
            transfer_time = self.transport[mode]["transfer_time"] / 60  # Convert minutes to hours
            trip_time = distance / speed + transfer_time
            self.total_time += trip_time
            self.total_cost += cost

            self.route_description.append(
                f"{self.nodes[start]['name']} ({distance:.2f} km, {trip_time * 60:.1f} min, {mode})"
            )
        
        self.route_description.append("Tarjan Home")


    def get_nodes(self):
        return self.nodes
    
    def get_transport(self):
        return self.transport
    
    def get_shortest_route(self):
        best_distance = float("inf")
        best_route = None

        start_node = 0
        other_nodes = range(1, len(self.nodes))

        for perm in permutations(other_nodes):
            total_distance = 0
            current_route = [start_node] + list(perm) + [start_node]

            for i in range(len(current_route) - 1):
                total_distance += self.distance_matrix[current_route[i]][current_route[i + 1]]
                if total_distance >= best_distance:
                    break

            if total_distance < best_distance:
                best_distance = total_distance
                best_route = current_route

        self.best_route = best_route
        self.best_distance = best_distance

        return best_route, best_distance
    
    # Visualization using NetworkX with Transport Modes
    def plot_graph(self):
        try:
            if not self.best_route and not self.best_distance:
                self.get_shortest_route()
        
            G = nx.DiGraph()

            for i, node in enumerate(self.nodes):
                G.add_node(i, label=node["name"])

            edges = [(self.best_route[i], self.best_route[i + 1]) for i in range(len(self.best_route) - 1)]

            pos = {i: (node["longitude"], node["latitude"]) for i, node in enumerate(self.nodes)}
            node_colors = ["lightgreen" if i == self.best_route[0] else "skyblue" for i in range(len(self.nodes))]
            labels = nx.get_node_attributes(G, "label")

            plt.figure(figsize=(12, 10))
            nx.draw_networkx_nodes(G, pos, node_size=100, node_color=node_colors)
            nx.draw_networkx_labels(G, pos, labels, font_size=5, font_weight="bold")
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=self.edge_colors, arrows=True)

            # Create a legend
            legend_labels = []
            for transport_mode, attributes in self.transport.items():
                legend_labels.append(plt.Line2D([0], [0], color=attributes["color"], lw=2, label=transport_mode))
            plt.legend(handles=legend_labels, title="Transport Modes", loc='upper right')
            
            plt.title("Optimal Route with Transport Modes")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.show()
        
        except nx.NetworkXError as e:
            print(f"Error in NetworkX graph generation: {e}")
        except Exception as e:
            print(f"Unexpected error during plotting: {e}")

    # Determine transport mode with prioritization for cost or time
    def determine_transport_mode(self, distance):
        """
        Determines the best transport mode based on distance, availability, and prioritization.
        """
        if self.prioritize_cost:
            # Avoid trains and use cost-effective options
            if self.bicycle_available and distance <= 3:
                return "Bicycle"
            elif distance <= 2:
                return "Walking"
            return "Bus"  # Fall back to Bus for longer trips
        else:
            # Prioritize time: No bicycles, use fastest mode
            if self.bicycle_available and distance <= 4:
                # Use bus if it takes less time than walking
                bicycle_time = distance / self.transport["Bicycle"]["speed"]
                bus_time = distance / self.transport["Bus"]["speed"] + self.transport["Bus"]["transfer_time"] / 60

                if bus_time < bicycle_time:
                    return "Bus"
                return "Bicycle"
            
            if distance <= 4:
                # Use bus if it takes less time than walking
                walking_time = distance / self.transport["Walking"]["speed"]
                bus_time = distance / self.transport["Bus"]["speed"] + self.transport["Bus"]["transfer_time"] / 60
                if bus_time < walking_time:
                    return "Bus"
                return "Walking"
            return "Train"
    
    def print_best_route(self):
        print("Shortest Route:")
        print(" -> ".join(self.route_description))
        print(f"Total Distance: {self.best_distance:.2f} km")
        print(f"Total Time: {self.total_time * 60:.1f} minutes")
        print(f"Total Cost: ${self.total_cost:.2f}")