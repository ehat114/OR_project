import pandas as pd
from pulp import *

def solveRoutesLP(dayType=None, saveLP=False):
    fname = "GeneratedFiles/WeekdaysRoutes.csv" if dayType == "Weekdays" else "GeneratedFiles/SaturdaysRoutes.csv" if dayType == "Saturdays" else None

    if fname is not None:
        routes = pd.read_csv(fname, index_col=0)
        prob = LpProblem("Distribution Route Problem", LpMinimize)
        vars = LpVariable.dicts("Route", routes.index, 0, None, LpBinary)

        prob += lpSum([routes["Cost"][r] * vars[r] for r in routes.index]), "Total Cost"

        prob += lpSum([vars[r] for r in routes.index]) <= 60

        for store in [s for s in routes.columns.tolist() if s not in ["Path", "Pallets", "Cost"]]:
            prob += lpSum([routes[store][r] * vars[r] for r in routes.index]) == 1
        
        if saveLP:
            prob.writeLP(f'GeneratedFiles/{dayType}Routes.lp')

        prob.solve()
        
        routes = routes.iloc[[v.name[6:] for v in prob.variables() if v.varValue == 1]]
        routes["Total Cost"] = [value(prob.objective)] + [0]*(routes.shape[0] - 1)
        routes[["Path", "Pallets", "Cost", "Total Cost"]].to_csv(f"GeneratedFiles/{dayType}Solution.csv")

if __name__ == "__main__":
    solveRoutesLP(dayType="Weekdays")