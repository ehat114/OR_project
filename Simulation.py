import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pickle


def getCost(path, adj, demands):
    path = ["Distribution Centre Auckland"] + path + ["Distribution Centre Auckland"]
    travelTimes = getTravelTime(adj, path)
    randomDemands = getRandomDemands(demands, path)

    totalTime = 0
    totalPallets = 0
    freight = 0

    maxPallets = 26
    maxTime = 4 * (60 ** 2)
    overtimeCost = 275 / (60 ** 2)
    costCoeff = 225. / (60 ** 2)

    for i in range(len(path) - 1):
        pallets = randomDemands[i + 1]
        nextTime = totalTime + travelTimes[i] + 450 * pallets
        nextPallets = totalPallets + pallets

        if nextPallets > maxPallets:
            # do the rest of the path
            totalTime += np.random.normal(adj.loc[path[i], "Distribution Centre Auckland"], 2)
            
            freight = 1
            break
        else:
            totalTime = nextTime
            totalPallets = nextPallets

    if totalTime > maxTime:
        return (totalTime - maxTime) * overtimeCost + maxTime * costCoeff + 2000 * freight
    else:
        return totalTime * costCoeff + 2000 * freight


def getRandomDemands(demands, path):
    return [np.random.choice(demands.loc[store].tolist()) if store != "Distribution Centre Auckland" else 0 for store in path]


def getTravelTime(adj, path):
    return [np.random.normal([adj.loc[path[i]][path[i + 1]] for i in range(len(path) - 1)], 2)]


if __name__ == "__main__":
    a = 0

    if a:
        # demands table
        demandData = pd.read_csv("Data/WoolworthsDemands.csv", index_col="Store").transpose()
        demandData.index = pd.to_datetime(demandData.index)  
        weekdays = demandData.loc[(demandData.index.weekday!=5) & (demandData.index.weekday!=6)].transpose()
        saturdays = demandData.loc[demandData.index.weekday==5].transpose()

        # adjacency matrix
        adj = pd.read_csv("Data/WoolworthsTravelDurations.csv", index_col=0)
        # routes
        satRoutes = pd.read_csv("GeneratedFiles/SaturdaysSolution2.csv")["Path"]
        weekRoutes = pd.read_csv("GeneratedFiles/WeekdaysSolution2.csv")["Path"]

        satRoutes = [satRoutes[i][2:-2].split("', '") for i in range(len(satRoutes))]
        weekRoutes = [weekRoutes[i][2:-2].split("', '") for i in range(len(weekRoutes))]

        iterations = 1000
        weekCosts = [0]*iterations
        satCosts = [0]*iterations

        for i in range(iterations):
            for path in weekRoutes:
                weekCosts[i] += getCost(path, adj, weekdays)
            
            for path in satRoutes:
                satCosts[i] += getCost(path, adj, saturdays)

        with open("GeneratedFiles/SimCosts.pickle", "wb") as fp:
            pickle.dump([weekCosts, satCosts], fp)
        
    else:
        with open("GeneratedFiles/SimCosts.pickle", "rb") as fp:
            weekCosts, satCosts = pickle.load(fp)
    
    satExp = pd.read_csv("GeneratedFiles/SaturdaysSolution2.csv")["Total Cost"].tolist()[0]
    weekExp = pd.read_csv("GeneratedFiles/WeekdaysSolution2.csv")["Total Cost"].tolist()[0]

    satLabel = "p-value = {:.2e}".format(stats.ttest_1samp(satCosts, satExp)[1])
    weekLabel = "p-value = {:.2e}".format(stats.ttest_1samp(weekCosts, weekExp)[1])

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.hist(satCosts, density=True, histtype="stepfilled", alpha=0.2, bins=12)
    ax1.plot([], color="white", label=satLabel)
    ax1.axvline(satExp, color='r', linestyle='dashed', linewidth=1)
    ax1.axvline(np.mean(satCosts), color='b', linestyle='dashed', linewidth=1)
    ax1.set_title('Saturdays')
    ax1.set_xlabel("Cost per Saturdays [$]")
    ax1.legend(frameon=False)

    ax2.hist(weekCosts, density=True, histtype="stepfilled", alpha=0.2, bins=12)
    ax2.plot([], color="white", label=weekLabel)
    ax2.axvline(weekExp, color='r', linestyle='dashed', linewidth=1)
    ax2.axvline(np.mean(weekCosts), color='b', linestyle='dashed', linewidth=1)
    ax2.set_title("Weekdays")
    ax2.set_xlabel("Cost per Weekday [$]")
    ax2.legend(frameon=False)

    fig.tight_layout()

    plt.show()

