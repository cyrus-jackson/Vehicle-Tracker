import cv2

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

    init_clusters = data_pts[:]         
    #shuffle(init_clusters)          
    init_clusters = init_clusters[0:k]  

    old_clusters, new_clusters = {}, {} 
    for item in init_clusters:
        old_clusters[item] = [] 

    while 1: 
        tmp = {}
        for k in old_clusters: 
            tmp[k] = []

        """ Associate each point with the closest cluster center. """
        for point in data_pts: 
            min_clust = None
            min_dist = 1000000000 
            for pc in tmp: 
                pc_dist = distance(point, pc)
                if pc_dist < min_dist: 
                    min_dist = pc_dist
                    min_clust = pc
            tmp[min_clust].append(point) 

        """ Recompute the new cluster centers. """
        for k in tmp:
            associated = tmp[k]
            xs = [pt[0] for pt in associated] 
            ys = [pt[1] for pt in associated] 
            x = average(xs) 
            y = average(ys) 
            new_clusters[(x,y)] = associated 

        if lists_are_same(old_clusters.keys(), new_clusters.keys()): 
            return old_clusters.keys()
        else: 
            old_clusters = new_clusters
            new_clusters = {}








backsub = cv2.BackgroundSubtractorMOG2(200,0,True)
fp = open("data.txt","w")
capture = cv2.VideoCapture("7.avi")
best_id = 0
carCount = 0
t = ()
data = []
i = 0
if capture:
  while True:
   # print(carCount)

    ret, frame = capture.read()
    if ret:
        fgmask = backsub.apply(frame, None, 0.01)
        contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        try: hierarchy = hierarchy[0]
        except: hierarchy = []
        cv2.line(frame,(0,70),(650,100),(0,255,0))
        for contour, hier in zip(contours, hierarchy):
            (x,y,w,h) = cv2.boundingRect(contour)
            x1=w/2     
            y1=h/2
            cx=x+x1
            cy=y+y1
            centroid=(cx,cy)
            
            if w > 80 and h > 70:
                #print("%d %d" % (y,x))
                cv2.circle(frame,(int(cx),int(cy)),4,(0,255,0),-1)
                # figure out id
             #   print(cv2.boundingRect(contour))
                if y >= 300 and y <= 370:
                  carCount = carCount + 1
                  print("%d,%d\n" % (w,h))
                  t = (w,h)
                  data.append(t)
                  fp.write("%d,%d\n" % (w,h))
                
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
                cv2.putText(frame, str(best_id), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 0), 2)
               
        cv2.imshow("Track", frame)
        cv2.imshow("background sub", fgmask)
    
    if cv2.waitKey(33) == ord('a'):
      cv2.destroyAllWindows()
      capture.release()
      fp.close()
      k = k_means(data, 3)
      print("The Centroids Are " ,k)



  
