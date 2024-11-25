import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations
from geopy.distance import geodesic
from package.tarjan_planner.logger import log_execution_time

class Route:
    @log_execution_time
    def __init__(self, bicycle_available=False, prioritize_cost=False) -> None:
        # Define transportation modes
        self.transport = {
            "Bus": {
                "speed": 40,           # Speed in km/h
                "cost": 2,             # Cost per km in currency units
                "transfer_time": 5,    # Transfer time in minutes
                "color": "blue",
            },
            "Train": {
                "speed": 80,
                "cost": 5,
                "transfer_time": 2,
                "color": "green",
            },
            "Bicycle": {
                "speed": 15,
                "cost": 0,
                "transfer_time": 1,
                "color": "orange",
            },
            "Walking": {
                "speed": 5,
                "cost": 0,
                "transfer_time": 0,
                "color": "red",
            },
        }
            
        self.nodes = [
            {
                "name": "Tarjan Home",
                "street": "Han River",
                "district": "Yeouido",
                "latitude": 37.5260,
                "longitude": 126.9287
            },
            {
                "name": "Relative 1",
                "street": "Gangnam-daero",
                "district": "Gangnam-gu",
                "latitude": 37.4979,
                "longitude": 127.0276
            },
            {
                "name": "Relative 2",
                "street": "Yangjae-daero",
                "district": "Seocho-gu",
                "latitude": 37.4833,
                "longitude": 127.0322
            },
            {
                "name": "Relative 3",
                "street": "Sinsa-daero",
                "district": "Gangnam-gu",
                "latitude": 37.5172,
                "longitude": 127.0286
            },
            {
                "name": "Relative 4",
                "street": "Apgujeong-ro",
                "district": "Gangnam-gu",
                "latitude": 37.5219,
                "longitude": 127.0411
            },
            {
                "name": "Relative 5",
                "street": "Hannam-daero",
                "district": "Yongsan-gu",
                "latitude": 37.5340,
                "longitude": 127.0026
            },
            {
                "name": "Relative 6",
                "street": "Seongsu-daero",
                "district": "Seongdong-gu",
                "latitude": 37.5443,
                "longitude": 127.0557
            },
            {
                "name": "Relative 7",
                "street": "Cheongdam-ro",
                "district": "Gangnam-gu",
                "latitude": 37.5172,
                "longitude": 127.0391
            },
            {
                "name": "Relative 8",
                "street": "Bukhan-ro",
                "district": "Jongno-gu",
                "latitude": 37.5800,
                "longitude": 126.9844
            },
            {
                "name": "Relative 9",
                "street": "Samseong-ro",
                "district": "Gangnam-gu",
                "latitude": 37.5110,
                "longitude": 127.0590
            },
            {
                "name": "Relative 10",
                "street": "Jamsil-ro",
                "district": "Songpa-gu",
                "latitude": 37.5133,
                "longitude": 127.1028
            }
        ]

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
        if not self.best_route and not self.best_distance:
            self.get_shortest_route()
        
        G = nx.DiGraph()

        for i, node in enumerate(self.nodes):
            G.add_node(i, label=node["name"])

        edges = [(self.best_route[i], self.best_route[i + 1]) for i in range(len(self.best_route) - 1)]

        pos = {i: (node["longitude"], node["latitude"]) for i, node in enumerate(self.nodes)}
        node_colors = ["green" if i == self.best_route[0] else "skyblue" for i in range(len(self.nodes))]
        labels = nx.get_node_attributes(G, "label")

        plt.figure(figsize=(12, 10))
        nx.draw_networkx_nodes(G, pos, node_size=100, node_color=node_colors)
        nx.draw_networkx_labels(G, pos, labels, font_size=5, font_weight="bold")
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=self.edge_colors, arrows=True)

        plt.title("Optimal Route with Transport Modes")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()

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