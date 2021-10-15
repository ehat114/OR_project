import pandas as pd
import numpy as np


def getAverages(outName=None, removeStores=False):
    fname = "Data/WoolworthsDemands.csv"

    demandData = pd.read_csv(fname, index_col="Store").transpose()
    demandData.index = pd.to_datetime(demandData.index)  
    weekdays = demandData.loc[(demandData.index.weekday!=5) & (demandData.index.weekday!=6)]
    saturdays = demandData.loc[demandData.index.weekday==5]

    weekdaysMean = weekdays.mean(axis=0).apply(np.ceil).to_frame().rename(columns={0:"Weekdays"})
    saturdaysMean = saturdays.mean(axis=0).apply(np.ceil).to_frame().rename(columns={0:"Saturdays"})

    if removeStores:
        weekdaysMean.loc["Countdown Aviemore Drive"] += weekdaysMean.loc["Countdown Highland Park"]
        weekdaysMean.loc["Countdown Westgate"] += weekdaysMean.loc["Countdown Northwest"]
        weekdaysMean = weekdaysMean.loc[~weekdaysMean.index.str.contains("Countdown Highland Park") * ~weekdaysMean.index.str.contains("Countdown Northwest")]

        saturdaysMean.loc["Countdown Aviemore Drive"] += saturdaysMean.loc["Countdown Highland Park"]
        saturdaysMean.loc["Countdown Westgate"] += saturdaysMean.loc["Countdown Northwest"]
        saturdaysMean = saturdaysMean.loc[~saturdaysMean.index.str.contains("Countdown Highland Park") * ~saturdaysMean.index.str.contains("Countdown Northwest")]

    averages = pd.merge(weekdaysMean, saturdaysMean, on="Store")

    averages.to_csv(outName)


if __name__ == "__main__":
    outName = "GeneratedFiles/AverageDemands.csv"

    getAverages(outName, removeStores=False)