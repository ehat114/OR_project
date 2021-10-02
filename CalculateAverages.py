import pandas as pd


def getAverages(outName=None):
    fname = "Data/WoolworthsDemands.csv"

    demandData = pd.read_csv(fname, index_col="Store").transpose()
    demandData.index = pd.to_datetime(demandData.index)  
    weekdays = demandData.loc[(demandData.index.weekday!=5) & (demandData.index.weekday!=6)]
    saturdays = demandData.loc[demandData.index.weekday==5]

    weekdaysMean = weekdays.mean(axis=0).to_frame().rename(columns={0:"Weekdays"})
    saturdaysMean = saturdays.mean(axis=0).to_frame().rename(columns={0:"Saturdays"})

    averages = pd.merge(weekdaysMean, saturdaysMean, on="Store")

    averages.to_csv(outName)


if __name__ == "__main__":
    outName = "GeneratedFiles/AverageDemands.csv"

    getAverages(outName)