from CalculateAverages import getAverages
from SortRegions import sort_regions_manual
from GenerateRoutes import Routes
from SolveLP import solveRoutesLP
from os import path

if __name__ == "__main__":
    overWrite = True

    # Calculate average demand
    averagesFile = "GeneratedFiles/AverageDemands.csv"
    if overWrite or not path.exists(averagesFile):
        getAverages(outName=averagesFile)

    print("Pass 1")

    # Sort stores to into regions
    regionsFile = "GeneratedFiles/WoolworthsRegions.csv"
    if overWrite or not path.exists(regionsFile):
        sort_regions_manual(outName=regionsFile)
    
    print("Pass 2")

    for dayType in ["Weekdays", "Saturdays"]:
            
        # Generate valid routes
        routesFile = f"GeneratedFiles/{dayType}Routes.csv"
        if overWrite or not path.exists(routesFile):
            maxStops = 3

            routes = Routes(dayType)

            for i in range(1, maxStops + 1):
                routes.getRoutes(dayType, i, [routes.origin])
                print(f"{dayType} pass {i}")
            
            routes.saveas(routesFile, overwrite=True)

        # Solve LP
        solFile = f"GeneratedFiles/{dayType}Solution.csv"
        if overWrite or not path.exists(solFile):
            solveRoutesLP(dayType=dayType)
            f"{dayType} pass {maxStops + 1}"