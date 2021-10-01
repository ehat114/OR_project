from numpy.lib import index_tricks
from GenerateRoutes import Routes
import pandas as pd
from pulp import *


if __name__ == "__main__":
    fname = "GeneratedFiles/WeekdaysRoutes"
    # fname = "SaturdaysRoutes"

    routes = pd.read_csv(f"{fname}.csv", index_col=0)

    prob = LpProblem("Distribution Route Problem", LpMinimize)

    vars = LpVariable.dicts("Route", routes.index, 0, None, LpBinary)

    prob += lpSum([routes["Cost"][r] * vars[r] for r in routes.index]), "Total Cost"

    for store in [s for s in routes.columns.tolist() if s not in ["Path", "Pallets", "Cost"]]:
        prob += lpSum([routes[store][r] * vars[r] for r in routes.index]) == 1
    
    prob += lpSum([vars[r] for r in routes.index]) <= 60
    
    prob.writeLP('GeneratedFiles/Routes.lp')

    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with its resolved optimum value
    for v in prob.variables():
        if v.varValue == 1:
            print(v.name, "=", v.varValue)

    # The optimised objective function valof Ingredients pue is printed to the screen    
    print("Total Cost = ", value(prob.objective))

