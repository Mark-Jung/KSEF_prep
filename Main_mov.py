# Main.py
# -*- coding: utf-8 -*-

import cv2
#import numpy as np
import os
#from PIL import Image
#from pytesseract import*
import downloadList
import carPos
import uploadFiles
import getGps   #for raspberry pi

import DetectChars
import DetectPlates
#import PossiblePlate

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################
def main():

    suspectList = downloadList.getList()
    print(suspectList)
    reportedList = []
    gpsString = getGps.get()
    gpsdata=gpsString.split(',')
    print('size of gps data:{}').format(len(gpsdata))
    print('GPS:{}').format(gpsString)
    
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training

    if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
        print "\nerror: KNN traning was not successful\n"               # show error message
        return                                                          # and exit program
    # end if




    nCount = 0
    cap = cv2.VideoCapture('TESTB4.avi')
    while (cap.isOpened()):
        #if ((cap.get(cv2.CAP_PROP_POS_FRAMES) + 1) < cap.get(cv2.CV_CAP_PROP_FRAME_COUNT)) :       # if there is at least one more frame
        if ((cap.get(1) + 1) < cap.get(7)-90) :       # if there is at least one more frame
            ret, imgOriginalScene = cap.read()                           # read it
            
        else: 
            print('end of avi')
            break
       
        #ret, imgOriginalScene = cap.read()
        nCount = nCount + 1
        if nCount > 1:
            nCount = 0
                
#            if imgOriginalScene is None:                            # if image was not read successfully
#                print "\nerror: image not read from file \n\n"      # print error message to std out
#                os.system("pause")                                  # pause so user can see error message
#                return                                              # and exit program
#            #end if

            listOfPossiblePlates = DetectPlates.detectPlatesInScene2(imgOriginalScene)           # detect plates
            listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

        
            if len(listOfPossiblePlates) == 0:                          # if no plates were found
##                print "\nno license plates were detected\n"             # inform user no plates were found
                cv2.imshow("imgOriginalScene", imgOriginalScene)            # show scene image
            else:                                                       # else
                        # if we get in here list of possible plates has at leat one plate
        
                        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
                listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
        
                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
                licPlate = listOfPossiblePlates[0]
                
                if len(licPlate.strChars) < 9:
                    continue
        
                #cv2.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate
                #cv2.imshow("imgThresh", licPlate.imgThresh)
        
#                if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
#                    print "\nno characters were detected\n\n"       # show message
#                    return                                          # and exit program
                # end if
        
                drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             # draw red rectangle around plate
                print "----------------------------------------"
                print "license plate = " + licPlate.strChars       # write license plate text to std out
                print "----------------------------------------"
                
        
                cv2.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image
                
        
                
        ###번호판 대조#############################################################
                strIndex = suspectList.find(licPlate.strChars.decode('utf-8'))
        ##########################################################################  
        
                #print('strIndex:{}').format(strIndex)
                     
                if strIndex > -1 and licPlate.strChars not in reportedList:
                    reportedList.append(licPlate.strChars)
                    fName = licPlate.strChars[-4:] + ".IMG.jpg"
                    cv2.imwrite(fName, imgOriginalScene)           # write image out to file

                    if len(gpsdata) ==4:
                        tempString = gpsString
            
                    else:
                        tempString='2017.09.26,07:12:48.012,37.504342,127.036213\n'

                    carPos.write(tempString,licPlate.strChars)
                    uploadFiles.upload(licPlate.strChars[-4:])
                    
                if licPlate.strChars in reportedList:
                    print('reported already\n')
                    
            cv2.waitKey(90) 

    k = cv2.waitKey(0) & 0xff
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
    
        return
       
# end main

###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# end function

###################################################################################################
if __name__ == "__main__":
    main()


















