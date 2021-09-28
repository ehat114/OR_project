# required imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()

def sort_regions_kmeans(plotRegions=False):
    ''' Partitions the Woolworths stores into regions based on their location using a k-means algorithm.
    
        Parameters
        ----------
        plotRegions : bool
            If true, plots the store locations coloured with their region on a scatterplot.

        Returns
        -------
        None

        Notes
        -----
        The list of stores and their respective regions are written in the file 'WoolworthsRegions.csv'.
    '''

    # read location data from file
    data = pd.read_csv('WoolworthsLocations.csv')
    # seperate out required columns
    locs = data.loc[:,['Store','Lat','Long']]

    # compute k-means clustering of data
    kmeans = KMeans(n_clusters=6,init='k-means++')      # we had 5 clusters - seems to work better with 6
    kmeans.fit(locs[locs.columns[1:3]])

    # predicts region clusters of data 
    locs['Region'] = kmeans.fit_predict(locs[locs.columns[1:3]])
    #locs['Region'] = locs['Region'] + 1     # changes region labels from {0,1,...,n-1} to {1,2,...,n}
    labels = kmeans.predict(locs[locs.columns[1:3]])

    # write new data frame to csv file
    locs.to_csv('WoolworthsRegions.csv')

    if plotRegions:
        # visualise k-means with scatterplot
        locs.plot.scatter(x = 'Long', y = 'Lat', c=labels, s=50,cmap='inferno',title='Auckland Woolworths stores filtered by region')
        plt.show()


def sort_regions_manual(plotRegions=False):
    # read location data from file
    data = pd.read_csv('WoolworthsLocations.csv')
    # seperate out required columns
    locs = data.loc[:,['Store','Lat','Long']]
    locs.set_index('Store')

    # create new column of regions
    locs['Region'] = [-1]*66    # initialize regions at -1 so we can spot future errors

    # loop over each store
    for st in locs.index:
        # find coordinates of store
        x = locs['Long'][st]
        y = locs['Lat'][st]

        # check if store within bounds of region 4
        if x >= 174.8289359 and y >= -36.9297263:
            locs['Region'][st] = 4
        # check if store within bounds of region 5
        if y <= -36.9425083:
            locs['Region'][st] = 5
        # check if store within bounds of region 2
        if x <= 174.7239957:
            locs['Region'][st] = 2
        # check if store within bounds of region 1
        if y >= -36.81111802 and locs['Region'][st] != 2:
            locs['Region'][st] = 1
        # remaining stores are in region 3
        if locs['Region'][st] == -1:
            locs['Region'][st] = 3
        
    # change one final store region - Countdown Glenfield to region 1
    locs['Region'][7] = 1

    # write to csv file
    locs.to_csv('WoolworthsRegions.csv')

    if plotRegions:
        # visualise regions with scatterplot
        locs.plot.scatter(x = 'Long', y = 'Lat', c ='Region', s=50,cmap='inferno',title='Auckland Woolworths stores filtered by region')
        plt.show()

def main():
    #sort_regions_kmeans(True)
    sort_regions_manual(True)

if __name__ == "__main__":
    main()