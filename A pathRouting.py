import numpy as np  #for numerical operations, particularly calculating Euclidean distances.
import heapq    #Implements a priority queue for efficiently selecting the next node to explore in the A* algorithm.

# Use Euclidean distance as heuristic (a measure of the straight-line distance between two points)
def heuristic(location, deliveries):
    distances = []
    for delivery in deliveries:
        distance = np.linalg.norm(np.array(location) - np.array(delivery))
        distances.append(distance)
    return min(distances)

def get_neighbors(current, all_locations):
    neighbors = []
    for loc in all_locations:
        if loc != current:
            neighbors.append(loc)
    return neighbors

# Look up the cost to travel from start to destination, considering traffic information
def get_cost(start, destination, traffic_info):
    cost = traffic_info.get((start, destination))
    if cost is not None:
        return cost
    else:
        return float('inf')

# determining the actual route taken once the algorithm has finished processing
def reconstruct_path(came_from, current):
    total_path_covered = [current]
    while True:
        if current not in came_from:
            break
        current = came_from[current]
        total_path_covered.append(current)
    return total_path_covered[::-1]  # Return reversed path

def A_algorithm(start, deliveries, traffic_info):
    open_set = []   # nodes that are to be explored
    heapq.heappush(open_set, (0, start))    # Add the starting node to the open set
    came_from = {}
    g_cost = {start: 0}
    f_score = {start: heuristic(start, deliveries)}
    
    while open_set:
        current = heapq.heappop(open_set)[1]    # The one node with the lowest priority/cost is popped from the heap first.
        
        all_deliveries_reached = True  # Assume all deliveries are reached        
        for delivery in deliveries:
            if delivery not in came_from:
                all_deliveries_reached = False  # Found a delivery not reached
                break  # Exit the loop early        
        
        if all_deliveries_reached:
            return reconstruct_path(came_from, current)
        
# This loop iterates over all neighboring nodes (potential delivery points) of the current node. It calculates the tentative g-score, which is the cost to reach this neighbor from the start.      
        for neighbor in get_neighbors(current, deliveries):
            tentative_g_score = g_cost[current] + get_cost(current, neighbor, traffic_info)

# If the calculated tentative_g_score is lower than the previously recorded g-score for that neighbor (or if it doesn’t exist), it updates:     
            if tentative_g_score < g_cost.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g_score
                f_score[neighbor] = g_cost[neighbor] + heuristic(neighbor, deliveries)
                
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    path = [start]      # Initialize the path with the starting point 
    remaining_deliveries = deliveries[:]        # Create a copy of the deliveries list to keep track of remaining deliveries
    current = start     # Set the current location to the starting point
    
    while remaining_deliveries:     # Loop until all deliveries are made
        nearest_delivery = min(remaining_deliveries, key=lambda x: get_cost(current, x, traffic_info))
        path.append(nearest_delivery)
        current = nearest_delivery       # Update the current location to the nearest delivery point
        remaining_deliveries.remove(nearest_delivery)       # Remove the nearest delivery point from the list of remaining deliveries
    
    return path     # Path found


# Example of the delivery route

start = (7, 7)
deliveries = [(1, 2), (2, 3), (3, 1), (8, 8), (4, 4), (6, 6), (7, 7), (9, 9), (0, 0), (9, 10)]
all_locations = [(0, 0), (1, 2), (2, 3), (3, 1), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14)]

traffic_info = {
    ((0, 0), (1, 1)): 1,
    ((1, 1), (2, 2)): 1,
    ((2, 2), (3, 3)): 1,
    ((3, 3), (4, 4)): 1,
    ((4, 4), (5, 5)): 1,
    ((5, 5), (6, 6)): 1,
    ((6, 6), (7, 7)): 1,
    ((7, 7), (8, 8)): 1,
    ((8, 8), (9, 9)): 1,
    ((0, 0), (2, 2)): 2,
    ((0, 0), (3, 3)): 3,
    ((0, 0), (4, 4)): 4,
    ((0, 0), (5, 5)): 5,
    ((1, 1), (3, 3)): 2,
    ((1, 1), (4, 4)): 3,
    ((1, 1), (5, 5)): 4,
    ((2, 2), (4, 4)): 2,
    ((2, 2), (5, 5)): 3,
    ((3, 3), (5, 5)): 2,
}

# Call the A* algorithm to find the optimal delivery route
route = A_algorithm(start, deliveries, traffic_info)
print("Optimal delivery route:", route)
