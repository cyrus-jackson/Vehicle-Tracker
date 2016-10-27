from math import sqrt

def k_means(data_pts, k=None):
    """ Return k (x,y) pairs where:
            k = number of clusters
        and each
            (x,y) pair = centroid of cluster

        data_pts should be a list of (x,y) tuples, e.g.,
            data_pts=[ (0,0), (0,5), (1,3) ]
    """

    """ Helper functions """

    
    def lists_are_same(la, lb): 
        out = False
        for item in la:
            if item not in lb:
                out = False
                break
            else:
                out = True
        return out  
    def distance(a, b): 
        return sqrt(abs(a[0]-b[0])**2 + abs(a[1]-b[1])**2)
    def average(a): 
        return sum(a)/float(len(a))

    """ Set up some initial values """
    if k is None: 
        n = len(data_pts)
        k = int(sqrt(n/2))  
                        
    if k < 1: 
        k = 1



    """ Randomly generate k clusters and determine the cluster centers,
        or directly generate k random points as cluster centers. """

    init_clusters = data_pts[:]         # put all of the data points into clusters
    #shuffle(init_clusters)          # put the data points in random order
    init_clusters = init_clusters[0:k]  # only keep the first k random clusters

    old_clusters, new_clusters = {}, {} 
    for item in init_clusters:
        old_clusters[item] = [] # every cluster has a list of points associated with it. Initially, it's 0

    while 1: # just keep going forever, until our break condition is met
        tmp = {}
        for k in old_clusters: # create an editable version of the old_clusters dictionary
            tmp[k] = []

        """ Associate each point with the closest cluster center. """
        for point in data_pts: # for each (x,y) data point
            min_clust = None
            min_dist = 1000000000 # absurdly large, should be larger than the maximum distance for most data sets
            for pc in tmp: # for every possible closest cluster
                pc_dist = distance(point, pc)
                if pc_dist < min_dist: # if this cluster is the closest, have it be the closest (duh)
                    min_dist = pc_dist
                    min_clust = pc
            tmp[min_clust].append(point) # add each point to its closest cluster's list of associated points

        """ Recompute the new cluster centers. """
        for k in tmp:
            associated = tmp[k]
            xs = [pt[0] for pt in associated] # build up a list of x's
            ys = [pt[1] for pt in associated] # build up a list of y's
            x = average(xs) # x coordinate of new cluster
            y = average(ys) # y coordinate of new cluster
            new_clusters[(x,y)] = associated # these are the points the center was built off of, they're *probably* still associated

        if lists_are_same(old_clusters.keys(), new_clusters.keys()): # if we've reached equilibrium, return the points
            return old_clusters.keys()
        else: # otherwise, we'll go another round. let old_clusters = new_clusters, and clear new_clusters.
            old_clusters = new_clusters
            new_clusters = {}


k = k_means([ (3,2), (0,5), (1,3), (2,5), (3,8) ], 3)
print(k)
