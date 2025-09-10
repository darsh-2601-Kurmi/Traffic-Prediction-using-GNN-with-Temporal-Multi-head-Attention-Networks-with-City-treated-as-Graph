import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import networkx as nx

# Load and process edges data
edges = pd.read_csv('edges_data.csv')
edges['Shape'] = edges['Shape'].fillna('')
edges['ShapePoints'] = edges['Shape'].apply(
    lambda x: [tuple(map(float, point.split(','))) for point in x.split()] if x else []
)

# Keep only valid edges (with shape points)
valid_edges = edges[edges['ShapePoints'].apply(len) > 0]

def get_outgoing_edges(node_id):
    """Get outgoing edges for a given intersection that have valid shape points."""
    return valid_edges[valid_edges['From'] == node_id]

# Speed and acceleration parameters
MAX_SPEED = 33.3  # ~120 km/h
ACCELERATION_LIMIT = 2.5  # ~9 km/h per second

def calculate_direction(current_position, next_position):
    """Calculate direction in degrees between two points."""
    dx, dy = next_position[0] - current_position[0], next_position[1] - current_position[1]
    angle_rad = np.arctan2(dy, dx)
    angle_deg = np.degrees(angle_rad)
    return angle_deg % 360  # Ensure angle is between 0-360

def create_car(car_id, valid_edges):
    """Initialize a car at a random valid edge."""
    selected_edge = valid_edges.sample().iloc[0]
    from_node, to_node = selected_edge['From'], selected_edge['To']
    shapepoints = selected_edge['ShapePoints']
    
    initial_position = shapepoints[0]
    if len(shapepoints) > 1:
        initial_direction = calculate_direction(initial_position, shapepoints[1])
    else:
        initial_direction = 0  # Default direction if only one point

    speed = random.uniform(5, 20)  # Initial speed

    return {
        "ID": car_id,
        "X": initial_position[0],
        "Y": initial_position[1],
        "Edge": (from_node, to_node),
        "CurrentPoint": 0,
        "Shapepoints": shapepoints,
        "Speed": speed,
        "Direction": initial_direction,  # Store direction
        "Download": random.uniform(1, 10),
        "Upload": random.uniform(1, 10),
        "State": "moving"
    }

# Limit the simulation to 75 cars only
cars = [create_car(i, valid_edges) for i in range(300)]
car_data = []
current_time = datetime.now()

# Simulate movement for 300 seconds
for t in range(300):
    for car in cars:
        x, y = car["X"], car["Y"]
        speed = car["Speed"]
        shapepoints = car["Shapepoints"]
        current_point_index = car["CurrentPoint"]
        
        if car["State"] == "moving":
            if random.random() < 0.2:  # Adjust speed with acceleration limits
                acceleration = random.uniform(-ACCELERATION_LIMIT, ACCELERATION_LIMIT)
                car["Speed"] = max(5, min(car["Speed"] + acceleration, MAX_SPEED))
            
            if current_point_index < len(shapepoints) - 1:
                next_point = shapepoints[current_point_index + 1]
                dist_to_next = np.sqrt((next_point[0] - x) ** 2 + (next_point[1] - y) ** 2)
                max_movement = car["Speed"]

                # Calculate new direction
                car["Direction"] = calculate_direction((x, y), next_point)

                if dist_to_next <= max_movement:
                    car["X"], car["Y"] = next_point
                    car["CurrentPoint"] += 1
                else:
                    direction = ((next_point[0] - x) / dist_to_next, (next_point[1] - y) / dist_to_next)
                    car["X"] += direction[0] * max_movement
                    car["Y"] += direction[1] * max_movement
            
            elif current_point_index == len(shapepoints) - 1:
                current_node = car["Edge"][1]
                outgoing_edges = get_outgoing_edges(current_node)
                
                if not outgoing_edges.empty:
                    next_edge = outgoing_edges.sample().iloc[0]
                    if len(next_edge['ShapePoints']) > 0:
                        car["Edge"] = (next_edge['From'], next_edge['To'])
                        car["Shapepoints"] = next_edge['ShapePoints']
                        car["CurrentPoint"] = 0
                        car["X"], car["Y"] = car["Shapepoints"][0]

                        # Update direction for the new segment
                        if len(car["Shapepoints"]) > 1:
                            car["Direction"] = calculate_direction(car["Shapepoints"][0], car["Shapepoints"][1])
                    else:
                        car["State"] = "waiting"
                        car["WaitTime"] = random.randint(1, 3)
                else:
                    car["State"] = "waiting"
                    car["WaitTime"] = random.randint(1, 3)
        
        elif car["State"] == "waiting":
            car["WaitTime"] -= 1
            if car["WaitTime"] <= 0:
                car["State"] = "moving"
        
        car_data.append({
            "ID": car["ID"],
            "Time": current_time + timedelta(seconds=t),
            "X": car["X"],
            "Y": car["Y"],
            "Speed": car["Speed"] if car["State"] == "moving" else 0,
            "Direction": car["Direction"],  # Add direction column
            "State": car["State"],
            "Download": car["Download"],
            "Upload": car["Upload"]
        })

# Save the updated simulation data
car_data_df = pd.DataFrame(car_data)
car_data_df.to_csv("car_data_simulation_300_cars.csv", index=False)
print("Car movement data for 75 cars with direction tracking has been saved to 'car_data_simulation_75_cars.csv'")
