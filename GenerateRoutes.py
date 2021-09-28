import pandas as pd
import os
import re
from CalculateAverages import getAverages


class Routes():
    def __init__(self, type) -> None:
        # Constraints
        self.maxPallets = 26
        self.maxTime = 4 * (60 ** 2)
        self.costCoeff = 225. / (60**2)
        
        # Name of origin
        self.origin = "Distribution Centre Auckland"

        # Get average demands
        self.demands = getAverages()

        # Get adjacency matrix
        self.adj = getAdjacencyMatrix()

        # Get regions
        self.regions = getRegions()

        # Get the name of every store
        self.stores = [s for s in self.adj.index.tolist() if s != self.origin]
        
        if type == "Saturdays":
            matchStr = re.compile("Countdown")
            self.stores = [s for s in self.stores if matchStr.match(s)]

        # Initialize dataframe
        self.routes = pd.DataFrame(columns=["Path"] + ["Pallets"] + ["Cost"] + self.stores)

    def getRoutes(self, type, maxStops, currentPath, time=0, pallets=0, stops=0) -> None:
        
        # Stopping condition
        if stops == maxStops:
            nextTime = time + self.adj.loc[currentPath[-1], self.origin]

            if nextTime <= self.maxTime:
                self.addRoute(currentPath, nextTime, pallets)
        else:
            for store in self.stores:
                if store not in currentPath and (self.regions[store] == self.regions[currentPath[-1]] or len(currentPath) == 1):
                # if store not in currentPath:
                    demand = self.demands.loc[store, type]
                    nextTime = time + self.adj.loc[currentPath[-1], store] + 450 * demand
                    nextPallets = pallets + demand

                    if nextTime <= self.maxTime and nextPallets <= self.maxPallets:
                        self.getRoutes(type, maxStops, currentPath + [store], nextTime, nextPallets, stops + 1)


    def addRoute(self, path, time, pallets):
        self.routes = self.routes.append(dict(zip(self.routes.columns.values, [path[1:]] + [pallets] + [round(time * self.costCoeff, 2)] + [1 if store in path else 0 for store in self.stores])), ignore_index=True)

    
    def saveas(self, fname, overwrite=False):
        if os.path.exists(fname) and not overwrite:
            raise Exception(f"\"{fname}\" already exists")
        else:
            self.routes.to_csv(f"{fname}.csv")

    def loadfrom(self, fname):
        self.routes = pd.read_csv(f"{fname}.csv", index_col=0)


def getAdjacencyMatrix():
    fname = "Data/WoolworthsTravelDurations.csv"
    return pd.read_csv(fname, index_col=0)


def getRegions():
    fname = "GeneratedFiles/WoolworthsRegions.csv"
    return pd.read_csv(fname, index_col="Store")["Region"]


if __name__ == "__main__":
    save = 1
    read = 1
    type = "Weekdays"
    # type = "Saturdays"

    if read:
        routes = Routes(type)
        routes.loadfrom(f"GeneratedFiles/{type}Routes")

    else:
        # Calculate all possible routes with certain number of stops
        routes = Routes(type)

        for i in range(1, 3):
            routes.getRoutes(type, i, [routes.origin])
        
        if save:
            routes.saveas(f"GeneratedFiles/{type}Routes", overwrite=True)

    print(f"{len(routes.routes)} routes found")
    print(routes.routes)