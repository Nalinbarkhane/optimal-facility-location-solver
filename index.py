from pulp import *

# --- 1. DEFINE DATA (MODEL PARAMETERS) ---

# A list of potential facility sites
facilities = ["DC1", "DC2", "DC3"]

# A list of customer regions
customers = ["Cust1", "Cust2", "Cust3", "Cust4"]

# Fixed cost to build/operate a facility at each site
fixed_costs = {"DC1": 10000, 
               "DC2": 12000, 
               "DC3": 9000}

# Maximum capacity of each potential facility
capacities = {"DC1": 500, 
              "DC2": 500, 
              "DC3": 500}

# Annual demand from each customer
demands = {"Cust1": 200, 
           "Cust2": 150, 
           "Cust3": 300,
           "Cust4": 100}

# Variable transportation cost (per unit) from facility i to customer j
# Using a nested dictionary: transport_costs[i][j]
transport_costs = {
    "DC1": {"Cust1": 4, "Cust2": 6, "Cust3": 9, "Cust4": 5},
    "DC2": {"Cust1": 6, "Cust2": 4, "Cust3": 7, "Cust4": 8},
    "DC3": {"Cust1": 8, "Cust2": 3, "Cust3": 5, "Cust4": 4},
}

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
