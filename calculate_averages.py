import pandas as pd


def getAverages():
    fname = "WoolworthsDemands.csv"

    demandData = pd.read_csv(fname, index_col="Store").transpose()
    demandData.index = pd.to_datetime(demandData.index)  
    weekdays = demandData.loc[(demandData.index.weekday!=5) & (demandData.index.weekday!=6)]
    saturdays = demandData.loc[demandData.index.weekday==5]

    weekdaysMean = weekdays.mean(axis=0).to_frame().rename(columns={0:"Weekdays"})
    saturdaysMean = saturdays.mean(axis=0).to_frame().rename(columns={0:"Saturdays"})

    return pd.merge(weekdaysMean, saturdaysMean, on="Store")


if __name__ == "__main__":
    outname = "AverageDemands.csv"

    getAverages().to_csv(outname)