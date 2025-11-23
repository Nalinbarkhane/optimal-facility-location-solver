import pandas as pd
from pulp import *
import matplotlib.pyplot as plt
import os
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

print("Loading data from CSVs...")
try:
    # Load data from CSVs
    fac_df = pd.read_csv('data/facilities.csv')
    cust_df = pd.read_csv('data/customers.csv')
except FileNotFoundError:
    print("Error: Make sure 'facilities.csv' and 'customers.csv' are in the same directory.")
    exit()
    
# Set the facility/customer IDs as the index for easy lookup
fac_df = fac_df.set_index('facility_id')
cust_df = cust_df.set_index('customer_id')

print(fac_df.head())
print(cust_df.head())
# Get lists of facilities and customers
facilities = fac_df.index.tolist()
customers = cust_df.index.tolist()

print(facilities)
print(customers)

# Convert data to dictionaries (which PuLP expects)
fixed_costs = fac_df['fixed_cost'].to_dict()
capacities = fac_df['capacity'].to_dict()
demands = cust_df['demand'].to_dict()

print(fixed_costs)
print(capacities)
print(demands)

# --- 2. CALCULATE TRANSPORT COSTS ---

# Get (x, y) coordinates into numpy arrays
fac_coords = fac_df[['x', 'y']].values
cust_coords = cust_df[['x', 'y']].values

print(fac_coords)
print(cust_coords)

# Calculate Euclidean distance matrix
dist_matrix = euclidean_distances(fac_coords, cust_coords)
print(dist_matrix)

# Define a cost per unit of distance
# You can change this factor to see how it impacts the solution
COST_PER_DISTANCE_UNIT = 1.2

# Create the transport_costs dictionary
transport_costs = {}
for i_idx, i in enumerate(facilities):
    transport_costs[i] = {}
    for j_idx, j in enumerate(customers):
        transport_costs[i][j] = dist_matrix[i_idx, j_idx] * COST_PER_DISTANCE_UNIT

print("Data loaded and transport costs calculated.")

# --- 2. INITIALIZE THE MODEL ---
model = LpProblem(name="FacilityLocationProblem", sense=LpMinimize)

# --- 3. DEFINE DECISION VARIABLES ---

# y_i: A binary variable: 1 if we build at facility i, 0 otherwise
use_facility = LpVariable.dicts("UseFacility", facilities, cat=LpBinary)

# x_ij: A continuous variable: Quantity shipped from facility i to customer j
# lowBound=0 ensures non-negativity
ship_quantity = LpVariable.dicts("ShipQuantity", (facilities, customers), lowBound=0, cat=LpContinuous)

# --- 4. DEFINE THE OBJECTIVE FUNCTION ---

# 4a. Add the total fixed cost
fixed_cost_component = lpSum(fixed_costs[i] * use_facility[i] for i in facilities)

# 4b. Add the total variable transportation cost
variable_cost_component = lpSum(transport_costs[i][j] * ship_quantity[i][j] 
                                for i in facilities 
                                for j in customers)

# Add the combined objective function to the model
model += fixed_cost_component + variable_cost_component, "Total_Cost"

# --- 5. DEFINE THE CONSTRAINTS ---

# Constraint 1: Demand Satisfaction
# For each customer j, the sum of shipments from all facilities i must equal the demand of j
for j in customers:
    model += lpSum(ship_quantity[i][j] for i in facilities) == demands[j], f"Demand_Satisfaction_{j}"

# Constraint 2: Capacity Constraint
# For each facility i, the total shipped to all customers j must be <= capacity[i] * use_facility[i]
for i in facilities:
    model += lpSum(ship_quantity[i][j] for j in customers) <= capacities[i] * use_facility[i], f"Capacity_Constraint_{i}"

# --- 6. SOLVE THE MODEL ---
print("Solving the model...")
model.solve()

# --- 7. PRINT THE RESULTS ---
print(f"Status: {LpStatus[model.status]}")
print(f"Total Optimal Cost: ${value(model.objective):,.2f}")
print("\n--- Optimal Solution ---")

print("Facilities to Open:")
for i in facilities:
    if use_facility[i].varValue == 1:
        print(f"  - {i}")

print("\nShipping Plan:")
for i in facilities:
    for j in customers:
        # Only print shipments that are actually happening (quantity > 0)
        if ship_quantity[i][j].varValue > 0:
            print(f"  - Ship {ship_quantity[i][j].varValue:,.0f} units from {i} to {j}")
            
print("\nGenerating visualization...")
plt.figure(figsize=(12, 8))

# Plot customers
plt.scatter(cust_df['x'], cust_df['y'], c='blue', marker='o', label='Customers')
for j in customers:
    plt.text(cust_df.loc[j, 'x'] + 1, cust_df.loc[j, 'y'], j)

# Plot potential facility sites
plt.scatter(fac_df['x'], fac_df['y'], c='red', marker='x', s=100, label='Potential Sites')

# Plot opened facilities and shipping routes
for i in facilities:
    if use_facility[i].varValue == 1:
        # Plot the opened facility with a green star
        plt.scatter(fac_df.loc[i, 'x'], fac_df.loc[i, 'y'], c='green', marker='*', s=200, 
                    label=f'Opened Site: {i}')
        plt.text(fac_df.loc[i, 'x'] + 1, fac_df.loc[i, 'y'], i)
        
        # Plot shipping routes
        for j in customers:
            if ship_quantity[i][j].varValue > 0:
                # Get coordinates for the line
                x1, y1 = fac_df.loc[i, 'x'], fac_df.loc[i, 'y']
                x2, y2 = cust_df.loc[j, 'x'], cust_df.loc[j, 'y']
                plt.plot([x1, x2], [y1, y2], c='gray', linestyle='--', alpha=0.7)

plt.title('Optimal Facility Location and Shipping Routes')
plt.xlabel('X-Coordinate')
plt.ylabel('Y-Coordinate')
plt.legend(loc='upper left')
plt.grid(True)
OUTPUT_IMAGE_PATH = os.path.join('docs', 'images', 'solution.png')
os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
plt.savefig(OUTPUT_IMAGE_PATH, bbox_inches="tight", dpi=300)
plt.show()
