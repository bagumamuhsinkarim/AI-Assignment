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
    while current in came_from:
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
    
    return None  # No path found





# Example of the delivery route

start = (0, 0)  # Example starting point

deliveries = [(1, 2), (2, 3),(3, 1)]  # Example delivery points [(x1, y1), (x2, y2), ...

# Traffic information between delivery points
traffic_info = {
    ((0, 0), (1, 2)): 2,   # Start to (1, 2)
    ((0, 0), (2, 3)): 4,   # Start to (2, 3)
    ((1, 2), (2, 3)): 1,   # (1, 2) to (2, 3)
    ((1, 2), (3, 1)): 3,   # (1, 2) to (3, 1)
    ((2, 3), (3, 1)): 2,   # (2, 3) to (3, 1)
    ((0, 0), (3, 4)): 5,   # Start to (3, 4)
    ((1, 2), (3, 4)): 4,   # (1, 2) to (3, 4)
    ((2, 3), (1, 1)): 3,   # (2, 3) to (1, 1)
    ((3, 1), (1, 1)): 2,   # (3, 1) to (1, 1)
    ((0, 0), (4, 0)): 3,   # Start to (4, 0)
    ((4, 0), (3, 1)): 2,   # (4, 0) to (3, 1)
    ((2, 3), (0, 0)): 6,   # (2, 3) to Start
    ((3, 4), (4, 0)): 5,   # (3, 4) to (4, 0)
    ((4, 0), (3, 4)): 6,   # (4, 0) to (3, 4)
}

# Call the A* algorithm to find the optimal delivery route
route = A_algorithm(start, deliveries, traffic_info)
print("Optimal delivery route:", route)
