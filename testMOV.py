# -*- coding: utf-8 -*-
import cv2

cap = cv2.VideoCapture('TESTA.avi')
while (cap.isOpened()):
    #if ((cap.get(cv2.CAP_PROP_POS_FRAMES) + 1) < cap.get(cv2.CV_CAP_PROP_FRAME_COUNT)) :       # if there is at least one more frame
    if (cap.get(1) < cap.get(7)) :       # if there is at least one more frame
        ret, imgOriginalScene = cap.read()                           # read it
        print(cap.get(1))
                   
        
    else: 
        print('end of avi')
        break
    cv2.imshow("imgOriginalScene", imgOriginalScene)
    cv2.waitKey(67)
    
    
k = cv2.waitKey(0) & 0xff
if k == 27:
    cap.release()
    cv2.destroyAllWindows()
