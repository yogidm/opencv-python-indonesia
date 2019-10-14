import cv2 # Masukkan pustaka OpenCV
import numpy as np

def nothing(x):
    pass
cv2.namedWindow('Nilai HSV')

cv2.createTrackbar('HLo','Nilai HSV',17,180,nothing)
cv2.createTrackbar('HUp','Nilai HSV',33,180,nothing)
cv2.createTrackbar('SLo','Nilai HSV',78,255,nothing)
cv2.createTrackbar('SUp','Nilai HSV',208,255,nothing)
cv2.createTrackbar('VLo','Nilai HSV',88,255,nothing)
cv2.createTrackbar('VUp','Nilai HSV',166,255,nothing)

cap2 = cv2.VideoCapture(1)
while(True): # lakukan pembacaan pada semua frame
    ret2, frame2 = cap2.read()
    hsv = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    hlo = cv2.getTrackbarPos('HLo', 'Nilai HSV')
    hup = cv2.getTrackbarPos('HUp', 'Nilai HSV')
    slo = cv2.getTrackbarPos('SLo', 'Nilai HSV')
    sup = cv2.getTrackbarPos('SUp', 'Nilai HSV')
    vlo = cv2.getTrackbarPos('VLo', 'Nilai HSV')
    vup = cv2.getTrackbarPos('VUp', 'Nilai HSV')

    lower=np.array([hlo,slo,vlo])
    upper = np.array([hup,sup,vup])
    mask = cv2.inRange(hsv,lower,upper)

    #kernel = np.ones((5,5),np.uint8)
    #mask = cv2.erode(mask,kernel,1)
    mask =  cv2.blur(mask,(5,5))
    #====================================================
    cnts,hier= cv2.findContours( mask.copy(), cv2.RETR_LIST,
                                 cv2.CHAIN_APPROX_NONE)
    if cnts:
        cMax = max(cnts, key = cv2.contourArea)
        hull = cv2.convexHull(cMax)
        m = cv2.moments(hull)
        area = m['m00']
        if area == 0:
            area = 1

        centroids = (int (round(m['m10']/area)),int(round(m['m01']/area)) )
        c = centroids
        cv2.circle(frame2,c,30,(128,120,255),5)
        
    #=======================================================    
    
    
   
    cv2.imshow('Frame Awal',frame2)
    cv2.imshow('hsv',mask)
    
    # Tahan frame selama 1ms
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
# Lepas capture dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()


'''
h[(h>43)&(h<46)]=15
    h[(h>46)&(h<77)]=45
    h[(h>77)&(h<108)]=75
    h[(h>108)&(h<128)]=105
    h[(h>128)&(h<145)]=135
    h[(h>125)&(h<43)]=165

    anu=cv2.merge((h,s,v))
    '''
