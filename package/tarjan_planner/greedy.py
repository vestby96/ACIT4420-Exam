from geopy.distance import geodesic

# Given transport modes and nodes are unchanged
nodes = [
    {"name": "Tarjan Home", "latitude": 37.5260, "longitude": 126.9287},
    {"name": "Relative 1", "latitude": 37.4979, "longitude": 127.0276},
    {"name": "Relative 2", "latitude": 37.4833, "longitude": 127.0322},
    {"name": "Relative 3", "latitude": 37.5172, "longitude": 127.0286},
    {"name": "Relative 4", "latitude": 37.5219, "longitude": 127.0411},
    {"name": "Relative 5", "latitude": 37.5340, "longitude": 127.0026},
    {"name": "Relative 6", "latitude": 37.5443, "longitude": 127.0557},
    {"name": "Relative 7", "latitude": 37.5172, "longitude": 127.0391},
    {"name": "Relative 8", "latitude": 37.5800, "longitude": 126.9844},
    {"name": "Relative 9", "latitude": 37.5110, "longitude": 127.0590},
    {"name": "Relative 10", "latitude": 37.5133, "longitude": 127.1028},
]

# Function to calculate distance between two nodes
def calculate_distance(node1, node2):
    return geodesic(
        (node1["latitude"], node1["longitude"]),
        (node2["latitude"], node2["longitude"]),
    ).kilometers

# Function to find a greedy route
def find_greedy_route(nodes):
    n = len(nodes)
    visited = [False] * n  # Track visited nodes
    route = [0]            # Start at the first node (nodes[0])
    total_distance = 0

    current_node = 0       # Start at nodes[0]
    visited[current_node] = True

    for _ in range(n - 1):  # Visit all nodes except the starting one
        nearest_node = None
        nearest_distance = float("inf")

        # Find the closest unvisited node
        for i in range(n):
            if not visited[i]:
                distance = calculate_distance(nodes[current_node], nodes[i])
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_node = i

        # Visit the closest node
        route.append(nearest_node)
        total_distance += nearest_distance
        visited[nearest_node] = True
        current_node = nearest_node

    # Return to the starting node
    total_distance += calculate_distance(nodes[current_node], nodes[0])
    route.append(0)

    return route, total_distance

# Main execution
if __name__ == "__main__":
    route, distance = find_greedy_route(nodes)
    print("Greedy Route:", " -> ".join(nodes[i]["name"] for i in route))
    print("Total Distance:", distance, "km")
