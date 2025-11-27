from pyscipopt import Model

# This script solves the Next Release Problem (NRP) using pyscipopt.
# The goal is to select a set of requirements that maximizes customer profit
# while respecting a budget and other constraints.

# 1. Define problem data
requirements = [f'r{i}' for i in range(1, 8)]
costs = {
    'r1': 15, 'r2': 10, 'r3': 12, 'r4': 8, 'r5': 20, 'r6': 5, 'r7': 18
}
BUDGET = 50
customers = {
    'c1': {'reqs': ['r1', 'r3'], 'profit': 200},
    'c2': {'reqs': ['r2', 'r4', 'r5'], 'profit': 300},
    'c3': {'reqs': ['r1', 'r5'], 'profit': 150},
    'c4': {'reqs': ['r6'], 'profit': 100}
}

# 2. Create a SCIP model
model = Model("NRP_Solver")

# 3. Create variables
# Binary variables for each requirement (1 if selected, 0 otherwise)
req_vars = {r: model.addVar(vtype="B", name=r) for r in requirements}

# Binary variables for each customer's satisfaction
cust_sat_vars = {c: model.addVar(vtype="B", name=f'sat_{c}') for c in customers}

# 4. Add Constraints

# Constraint 1: Budget constraint
model.addCons(sum(costs[r] * req_vars[r] for r in requirements) <= BUDGET)

# Constraint 2: Feature Dependencies
# If r2 is selected, r1 must also be selected (r2 -> r1  <=>  r2 <= r1)
model.addCons(req_vars['r2'] <= req_vars['r1'])

# Constraint 3: Customer Satisfaction
# A customer is satisfied if all their requested requirements are met.
for name, data in customers.items():
    # This is equivalent to sat_c = AND(reqs), which can be modeled as:
    # sat_c <= req_i for all req_i in data['reqs']
    for req in data['reqs']:
        model.addCons(cust_sat_vars[name] <= req_vars[req])
    # sat_c >= sum(req_i) - (len(reqs) - 1)
    model.addCons(cust_sat_vars[name] >= sum(req_vars[r] for r in data['reqs']) - (len(data['reqs']) - 1))

# 5. Define Objective Function: Maximize total profit
total_profit = sum(data['profit'] * cust_sat_vars[name] for name, data in customers.items())
model.setObjective(total_profit, "maximize")

# 6. Solve the problem
model.optimize()

# 7. Print the solution
if model.getStatus() == "optimal":
    print("Optimal Solution Found:")

    selected_reqs = [r for r in requirements if model.getVal(req_vars[r]) > 0.9]
    final_cost = sum(costs[r] for r in selected_reqs)
    final_profit = model.getObjVal()

    print(f"\nSelected Requirements: {', '.join(sorted(selected_reqs))}")
    print(f"Total Cost: {final_cost} (Budget: {BUDGET})")

    print("\nCustomer Satisfaction:")
    for name, data in customers.items():
        if model.getVal(cust_sat_vars[name]) > 0.9:
            status = "SATISFIED"
        else:
            status = "NOT SATISFIED"
        req_names = sorted(data['reqs'])
        print(f"  - Customer {name} (requests {req_names}): {status}")

    print(f"\nTotal Profit: {final_profit}")

else:
    print("No optimal solution found.")
