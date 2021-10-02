from CalculateAverages import getAverages
from SortRegions import sort_regions_manual
from GenerateRoutes import Routes
from SolveLP import solveRoutesLP
from os import path

if __name__ == "__main__":
    overWriteAverages = False
    overWriteRegions = False
    overWriteRoutes = False
    overWriteSolutions = True

    # Calculate average demand
    averagesFile = "GeneratedFiles/AverageDemands.csv"
    if overWriteAverages or not path.exists(averagesFile):
        getAverages(outName=averagesFile)

    print("Averages passed")

    # Sort stores to into regions
    regionsFile = "GeneratedFiles/WoolworthsRegions.csv"
    if overWriteRegions or not path.exists(regionsFile):
        sort_regions_manual(outName=regionsFile)
    
    print("Regions passed")

    # For both weekdays and saturdays
    for dayType in ["Weekdays", "Saturdays"]:
            
        # Generate valid routes
        routesFile = f"GeneratedFiles/{dayType}Routes.csv"
        if overWriteRoutes or not path.exists(routesFile):
            maxStops = 3

            routes = Routes(dayType)

            for i in range(1, maxStops + 1):
                routes.getRoutes(dayType, i, [routes.origin])
                print(f"{dayType} {i}-stop(s) routes passed")
            
            routes.saveas(routesFile, overwrite=True)

        # Solve LP
        solFile = f"GeneratedFiles/{dayType}Solution.csv"
        if overWriteSolutions or not path.exists(solFile):
            solveRoutesLP(dayType=dayType)
            print(f"{dayType} solutions passed")