from numpy.lib.function_base import trim_zeros
from CalculateAverages import getAverages
from SortRegions import sort_regions_manual
from GenerateRoutes import Routes
from SolveLP import solveRoutesLP
from os import path


if __name__ == "__main__":
    overWriteAverages = False
    overWriteRegions = False
    overWriteRoutes = {"Weekdays": False, "Saturdays": True}
    overWriteSolutions = {"Weekdays": True, "Saturdays": True}
    removeStores = True

    # Calculate average demand
    averagesFile = "GeneratedFiles/AverageDemands.csv"
    if overWriteAverages or not path.exists(averagesFile):
        getAverages(outName=averagesFile, removeStores=removeStores)

    print("Averages passed")

    # Sort stores to into regions
    regionsFile = "GeneratedFiles/WoolworthsRegions.csv"
    if overWriteRegions or not path.exists(regionsFile):
        sort_regions_manual(outName=regionsFile)
    
    print("Regions passed")

    # For both weekdays and saturdays
    for dayType in ["Weekdays", "Saturdays"]:
            
        # Generate valid routes
        routesFile = f"GeneratedFiles/{dayType}Routes.csv" if not removeStores else f"GeneratedFiles/{dayType}Routes2.csv"
        if overWriteRoutes[dayType] or not path.exists(routesFile):
            maxStops = 3 if dayType == "Weekdays" else 3

            routes = Routes(dayType, removeStores=removeStores)

            routes.getRoutes(dayType, maxStops)
            
            routes.saveas(routesFile, overwrite=True)
        
        print(f"{dayType} routes passed")

        # Solve LP
        solFile = f"GeneratedFiles/{dayType}Solution.csv" if not removeStores else f"GeneratedFiles/{dayType}Solution2.csv"
        if overWriteSolutions[dayType] or not path.exists(solFile):
            solveRoutesLP(outname=solFile, dayType=dayType, removeStores=True)
                
        print(f"{dayType} solutions passed")