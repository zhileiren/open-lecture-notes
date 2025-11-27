from z3 import *

# This script solves the Next Release Problem (NRP) based on the formulation
# where profit is associated with satisfying a customer's complete set of
# requested requirements.

# 1. Define Requirements as Boolean variables
# Each variable represents whether a requirement is selected (True) or not (False)
r1, r2, r3, r4, r5, r6, r7 = Bools('r1 r2 r3 r4 r5 r6 r7')
requirements = [r1, r2, r3, r4, r5, r6, r7]

# 2. Define cost for each requirement
costs = {
    r1: 15, r2: 10, r3: 12, r4: 8, r5: 20, r6: 5, r7: 18
}

# 3. Define the total available budget
BUDGET = 50

# 4. Define customers, their requested requirements, and the profit they provide
customers = {
    'c1': {'reqs': [r1, r3], 'profit': 200},
    'c2': {'reqs': [r2, r4, r5], 'profit': 300},
    'c3': {'reqs': [r1, r5], 'profit': 150},
    'c4': {'reqs': [r6], 'profit': 100}
}

# 5. Create an optimizer instance
opt = Optimize()

# 6. Add Constraints

# Constraint 1: Budget constraint
# The sum of costs of selected requirements must not exceed the BUDGET
total_cost_expression = Sum([If(r, costs[r], 0) for r in requirements])
opt.add(total_cost_expression <= BUDGET)

# Constraint 2: Feature Dependencies (optional)
# Example: If r2 is selected, r1 must also be selected (e.g., r1 is a prerequisite for r2)
opt.add(Implies(r2, r1))


# 7. Define customer satisfaction and profit calculation
customer_profits = []
for name, data in customers.items():
    # A customer is satisfied if ALL their requested requirements are selected
    customer_satisfied = Bool(f'satisfied_{name}')
    opt.add(customer_satisfied == And(data['reqs']))
    customer_profits.append(If(customer_satisfied, data['profit'], 0))

# 8. Define Objective Function: Maximize total profit from satisfied customers
total_profit_expression = Sum(customer_profits)
opt.maximize(total_profit_expression)

# 9. Solve the problem
if opt.check() == sat:
    m = opt.model()
    print("Optimal Solution Found:")

    selected_reqs = [r for r in requirements if is_true(m.eval(r))]
    selected_reqs_names = sorted([str(r) for r in selected_reqs])

    final_cost = sum(costs[r] for r in selected_reqs)

    print(f"\nSelected Requirements: {', '.join(selected_reqs_names)}")
    print(f"Total Cost: {final_cost} (Budget: {BUDGET})")

    print("\nCustomer Satisfaction:")
    final_profit = 0
    for name, data in customers.items():
        satisfied_var = Bool(f'satisfied_{name}')
        if is_true(m.eval(satisfied_var)):
            final_profit += data['profit']
            status = "SATISFIED"
        else:
            status = "NOT SATISFIED"

        req_names = sorted([str(r) for r in data['reqs']])
        print(f"  - Customer {name} (requests {req_names}): {status}")

    print(f"\nTotal Profit: {final_profit}")

else:
    print("No solution found that satisfies all constraints.")