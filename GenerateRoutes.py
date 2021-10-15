import pandas as pd
import os
import re


class Routes():
    def __init__(self, dayType, removeStores=False) -> None:
        # Define constraints
        self.maxPallets = 26
        self.maxTime = 4 * (60 ** 2)
        self.costCoeff = 225. / (60**2)
        
        # Name of origin
        self.origin = "Distribution Centre Auckland"

        # Get average demands
        self.demands = getDemands(removeStores=removeStores)

        # Get adjacency matrix
        self.adj = getAdjacencyMatrix()

        # Get regions
        self.regions = getRegions()

        # Get the name of every store
        self.stores = [s for s in self.demands.index.tolist() if s != self.origin]
        
        # check if day is Saturday (stores have different demand)
        if dayType == "Saturdays":
            # find Countdown stores in route path
            matchStr = re.compile("Countdown")
            metroStr = re.compile("Metro")
            self.stores = [s for s in self.stores if matchStr.match(s) and not metroStr.match(s)]

        # Initialize dataframe
        self.routes = pd.DataFrame(columns=["Path"] + ["Pallets"] + ["Cost"] + self.stores)

    def getRoutes(self, dayType, maxStops):
        self.recursive(dayType, maxStops, currentPath=[self.origin])

    def recursive(self, dayType, maxStops, currentPath, time=0, pallets=0, stops=0):
        timeToOrigin = time + self.adj.loc[currentPath[-1], self.origin]

        if timeToOrigin <= self.maxTime:

            if len(currentPath) != 1:
                self.addRoute(currentPath, timeToOrigin, pallets)

            if stops < maxStops:
                for store in self.stores:
                    if store not in currentPath and (self.regions[store] == self.regions[currentPath[-1]] or len(currentPath) == 1): 
                        demand = self.demands.loc[store, dayType]
                        nextTime = time + self.adj.loc[currentPath[-1], store] + 450 * demand
                        nextPallets = pallets + demand

                        if nextTime <= self.maxTime and nextPallets <= self.maxPallets:
                            self.recursive(dayType, maxStops, currentPath + [store], nextTime, nextPallets, stops + 1)


    def addRoute(self, path, time, pallets):
        self.routes = self.routes.append(dict(zip(self.routes.columns.values, [path[1:]] + [pallets] + [round(time * self.costCoeff, 2)] + [1 if store in path else 0 for store in self.stores])), ignore_index=True)

    
    def saveas(self, fname, overwrite=False):
        if os.path.exists(fname) and not overwrite:
            raise Exception(f"\"{fname}\" already exists")
        else:
            self.routes.to_csv(fname)

    def loadfrom(self, fname):
        self.routes = pd.read_csv(fname, index_col=0)

def getDemands(removeStores=False):
    ''' Reads a dataframe of average store demands from file.
    
        Parameters
        ----------
        None

        Returns
        -------
        df : Pandas Dataframe
            Dataframe of average store demands.
    '''
    # define file name
    fname = "GeneratedFiles/AverageDemands.csv" if not removeStores else "GeneratedFiles/AverageDemands2.csv"
    # read average store demands from file
    df = pd.read_csv(fname, index_col="Store")
    # return dataframe of average demands
    return df


def getAdjacencyMatrix():
    ''' Reads the adjacency matrix for our linear programme i.e. a dataframe of travel durations between
        stores.
    
        Parameters
        ----------
        None

        Returns
        -------
        df : Pandas Dataframe
            Adjacency matrix of travel durations.
    '''
    # define file name
    fname = "Data/WoolworthsTravelDurations.csv"
    # read travel durations from file
    df = pd.read_csv(fname, index_col=0)
    # return adjacency matrix
    return df


def getRegions():
    ''' Reads a dataframe of store regions from file.
    
        Parameters
        ----------
        None
        
        Returns
        -------
        df : Pandas Dataframe
            Dataframe of store regions.
        '''
    # define file name 
    fname = "GeneratedFiles/WoolworthsRegions.csv"
    # read store regions from file
    df = pd.read_csv(fname, index_col="Store")["Region"]
    # return dataframe of store regions
    return df


if __name__ == "__main__":
    save = 1
    read = 0
    dayType = "Weekdays"
    # dayType = "Saturdays"

    if read:
        routes = Routes(dayType)
        routes.loadfrom(f"GeneratedFiles/{dayType}Routes.csv")

    else:
        # Calculate all possible routes with certain number of stops
        routes = Routes(dayType)

        routes.getRoutes(dayType, 3)
        
        if save:
            routes.saveas(f"GeneratedFiles/{dayType}Routes.csv", overwrite=True)

    print(f"{len(routes.routes)} routes found")
    print(routes.routes)