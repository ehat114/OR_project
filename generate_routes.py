import numpy as np
import pandas as pd
import pickle
from calculate_averages import getAverages


class Route():
    def __init__(self, path, time, pallets) -> None:
        self.path = path
        self.time = time
        self.pallets = pallets


class Routes():
    def __init__(self, adj, demands, type, origin, maxStops, maxTime, maxPallets, allStores) -> None:
        self.routes = []
        self.getRoutes(adj, demands, type, origin, maxStops, maxTime, maxPallets, [origin], [s for s in allStores if s != origin])

    def getRoutes(self, adj, demands, type, origin, maxStops, maxTime, maxPallets, currentPath, allStores, time=0, pallets=0, stops=0):
        if stops == maxStops:
            nextTime = time + adj.loc[currentPath[-1], origin]

            if nextTime <= maxTime:
                self.routes.append(Route(currentPath, nextTime, pallets))
        else:
            for store in allStores:
                if store not in currentPath:
                    demand = demands.loc[store, type]
                    nextTime = time + adj.loc[currentPath[-1], store] + 450 * demand
                    nextPallets = pallets + demand

                    if nextTime <= maxTime and nextPallets <= maxPallets:
                        self.getRoutes(adj, demands, type, origin, maxStops, maxTime, maxPallets, currentPath + [store], allStores, nextTime, nextPallets, stops+1)


def getAdjacencyMatrix():
    fname = "WoolworthsTravelDurations.csv"
    return pd.read_csv(fname, index_col=0)


if __name__ == "__main__":
    save = 1
    read = 0

    # Number of stops
    maxStops = 1

    if read:
        with open(f"{maxStops}StopsWeekdayRoutes.pickle", "rb") as fp:
            weekdayRoutes = pickle.load(fp)

        print(f"{len(weekdayRoutes.routes)} routes found")
        print(weekdayRoutes.routes[0].path)
    
    else:
        # Constraints
        maxPallets = 26
        maxTime = 4 * (60 ** 2)
        origin = "Distribution Centre Auckland"

        # Get average demands
        demands = getAverages()

        # Get adjacency matrix
        adj = getAdjacencyMatrix()

        # Get the name of every store + distribution center
        allStores = adj.index.values.tolist()

        # Calculate all possible routes with certain number of stops
        weekdayRoutes = Routes(adj, demands, "Weekdays", origin, maxStops, maxTime, maxPallets, allStores)
        print(f"{len(weekdayRoutes.routes)} routes found")

        if save:
            with open(f"{maxStops}StopsWeekdayRoutes.pickle", "wb") as fp:
                pickle.dump(weekdayRoutes, fp)
    