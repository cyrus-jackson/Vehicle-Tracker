import cv2
import numpy

def dist(x,y):   
    return numpy.sqrt(numpy.sum((x-y)**2))

centroid1 = numpy.array((286.2692307692308,319.53846153846155))
centroid2 = numpy.array((171.52173913043478,199.79710144927537))
centroid3 = numpy.array((80.19396551724137,99.2198275862069))

backsub = cv2.BackgroundSubtractorMOG2(200,0,True)
fp = open("data.txt","w")
capture = cv2.VideoCapture("7.avi")
best_id = 0
carCount = 0
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
                if y >= 300 and y <= 390:
                  a = numpy.array((w,h))
                  dist_a_centroid1 = dist(a,centroid1)
                  dist_a_centroid2 = dist(a,centroid2)
                  dist_a_centroid3 = dist(a,centroid3)
                  darr = numpy.array([dist_a_centroid1, dist_a_centroid2, dist_a_centroid3])
                  print("Category %d" % (darr.argmin() + 1 ))
                 
                
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
                cv2.putText(frame, str(best_id), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 0), 2)
               
        cv2.imshow("Track", frame)
        cv2.imshow("background sub", fgmask)
    
    if cv2.waitKey(33) == ord('a'):
      cv2.destroyAllWindows()
      capture.release()
      fp.close()



  
