# DetectPlates.py
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
import Main
import random

import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar

# module level variables ##########################################################################
PLATE_WIDTH_PADDING_FACTOR = 1.1
PLATE_HEIGHT_PADDING_FACTOR = 1.1
PLATE_ASPECT_RATIO_A = 2.0 # 1.97 ~ 2.16
PLATE_ASPECT_RATIO_B = 4.73
PLATE_MIN_WIDTH = 100

ASPECT_RATIO_A = 2.0 #2~2.16 12도 회전시 1.628
ASPECT_RATIO_B = 4.73 #12도 회전시 2.46
PIXEL_THRESHOLD = 200 #경계 카운트
NUM_CUT_IN_PLATE = 4 #plate찾을때 HIGH되는 횟수
OVERLAPPING_CUT_CENTER_DISTANCE = 5 #중복 rect 제거시 중심거리
###################################################################################################
def detectPlatesInScene2(imgOriginalScene):
    listOfPossiblePlates = []                   # this will be the return value

    height, width, numChannels = imgOriginalScene.shape

    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)         # preprocess to get grayscale and threshold images

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)
    # end if # show steps #########################################################################
    imgThreshCopy = imgThreshScene.copy()

    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)   # find all contours
    
    possibleCnts = []

    for cnt in contours:
        rect = cv2.boundingRect(cnt)
        [x,y,w,h] = rect
        aspectRatio = float(w/h)
        if w > PLATE_MIN_WIDTH:
            if aspectRatio > ASPECT_RATIO_A *0.8 and aspectRatio < ASPECT_RATIO_A * 1.2:
                possibleCnts.append(cnt)
            elif aspectRatio > ASPECT_RATIO_B *0.53 and aspectRatio < ASPECT_RATIO_B * 1.2:
                possibleCnts.append(cnt)
                
    if Main.showSteps == True: # show steps #######################################################
        imgOriginalCopy0 = imgOriginalScene.copy() 
        for cnt in possibleCnts:
            [x,y,w,h] = cv2.boundingRect(cnt)             
            cv2.rectangle(imgOriginalCopy0,(x,y),(x+w,y+h),(255,0,255),2)
        cv2.imshow('possible plate',imgOriginalCopy0)
    ##############################################################################################
                
    possibleCnts = checkOvelappingCnts(possibleCnts)                 
    possibleCnts = checkPossibleChars(imgOriginalScene, imgThreshScene, possibleCnts) 
    
    if Main.showSteps == True: # show steps #######################################################
        imgOriginalCopy = imgOriginalScene.copy()        
        for cnt in possibleCnts:
            [x,y,w,h] = cv2.boundingRect(cnt)
            cv2.rectangle(imgOriginalCopy,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow("removed Plates", imgOriginalCopy) 
    ############################################################################################
            
    if len(possibleCnts) > 0:
        for cnt in possibleCnts:
            rectBox2D = cv2.minAreaRect(cnt)
            possiblePlate = extractPlate2(imgOriginalScene, rectBox2D)         # attempt to extract plate
            listOfPossiblePlates.append(possiblePlate) 

    return listOfPossiblePlates
# end function
###############################################################################################
def checkPossibleChars(imgOriginalScene, imgThreshScene, possibleCnts):
    
    height, width = imgThreshScene.shape
    
    checkedCnt = []
    pxIsHighOld = False
    
    imgOriginalCopy = imgOriginalScene.copy() #그리기용
    
    for cnt in possibleCnts:
        intEdgeCount = 0
        [x,y,w,h] = cv2.boundingRect(cnt)
        midX = x + w/2
        midY = y + h/2  
        pvMax = 0
        for i in range(0,w):
            pv = imgThreshScene[midY,x+i]
            
            if pv > pvMax: pvMax = pv
            if pv > PIXEL_THRESHOLD: pxIsHigh = True
            else: pxIsHigh = False
            if pxIsHigh != pxIsHighOld :
                if pxIsHighOld == False:
                    intEdgeCount = intEdgeCount+1
                    cv2.line(imgOriginalCopy,(x+i,midY),(x+i+3,midY),(0,0,255),2)
                
                pxIsHighOld = pxIsHigh
        #print('[checkPossibleChars] pvMax:{}, edges:{}').format(pvMax, intEdgeCount)
        
        if intEdgeCount >= NUM_CUT_IN_PLATE and midX > width/5 and midX < width*4/5:    #글자 갯수, 화면상 위치 판단
            checkedCnt.append(cnt)
            
    if Main.showSteps == True: # show steps ####################################################   
        cv2.imshow('checkPossibleChars_risingEdge',imgOriginalCopy)
    ############################################################################################    
    return checkedCnt
###########################################################################################################
def checkOvelappingCnts(possibleCnts):
    removedCnts = possibleCnts
    itoRm = []
    
    for i in range(0, len(removedCnts)):
        rectA = cv2.boundingRect(removedCnts[i])
        [xA,yA,wA,hA] = rectA
        for j in range(0, len(removedCnts)):
            if i == j:
                continue
            rectB = cv2.boundingRect(removedCnts[j])
            [xB,yB,wB,hB] = rectB
            if wA < wB:
                if xA > xB and yA > yB and xA+xA < xB+wB and yA+hA < yB+hB:
                    itoRm.append(j)
            elif wA > wB:
                if xA < xB and yA < yB and xA+xA > xB+wB and yA+hA > yB+hB:
                    itoRm.append(i)
                    
    itoRm = list(set(itoRm)) #contours는 set으로 중복제거가 안 되는 듯
    
    if len(itoRm) > 0:
        count = 0
        for k in itoRm:
            del removedCnts[k-count]
            count = count + 1
            
    return removedCnts
    
#######################################################################################################
def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []                   # this will be the return value

    height, width, numChannels = imgOriginalScene.shape

    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("0", imgOriginalScene)
    # end if # show steps #########################################################################

    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)         # preprocess to get grayscale and threshold images

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)
    # end if # show steps #########################################################################

            # find all possible chars in the scene,
            # this function first finds all contours, then only includes contours that could be chars (without comparison to other chars yet)
    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene, 1) #scene일때1, plate일때2

    if Main.showSteps == True: # show steps #######################################################
        print "step 2 - len(listOfPossibleCharsInScene) = " + str(len(listOfPossibleCharsInScene))         # 131 with MCLRNF1 image

        imgContours = np.zeros((height, width, 3), np.uint8)

        contours = []

        for possibleChar in listOfPossibleCharsInScene:
            contours.append(possibleChar.contour)
        # end for

        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)          #글자로 추정되는 contour만 그린다.
        cv2.imshow("2b", imgContours) 
    # end if # show steps #########################################################################

            # given a list of all possible chars, find groups of matching chars
            # in the next steps each group of matching chars will attempt to be recognized as a plate
###########################################################################################################            
    listOfPossibleCharsInScene = DetectChars.removeInnerOverlappingChars(listOfPossibleCharsInScene)  #느리면 제거???
####################################################################################################################    
    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene,1) #문자열로 추정되는 contours를 그룹으로 만들고 그룹의 리스트작성

    if Main.showSteps == True: # show steps #######################################################
        print "step 3 - listOfListsOfMatchingCharsInScene.Count = " + str(len(listOfListsOfMatchingCharsInScene))    # 13 with MCLRNF1 image

        imgContours = np.zeros((height, width, 3), np.uint8)
        #문자열 그룹별로 다른 색으로 contours를 그려준다.
        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue = random.randint(0, 255)
            intRandomGreen = random.randint(0, 255)
            intRandomRed = random.randint(0, 255)

            contours = []

            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
            # end for

            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
        # end for

        cv2.imshow("3", imgContours)
    # end if # show steps #########################################################################

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:                   # for each group of matching chars
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)         # attempt to extract plate

        if possiblePlate.imgPlate is not None:                          # if plate was found
            listOfPossiblePlates.append(possiblePlate)                  # add to list of possible plates
        # end if
    # end for

    print "\n" + str(len(listOfPossiblePlates)) + " possible plates found"          # 13 with MCLRNF1 image

    if Main.showSteps == True: # show steps #######################################################
        print "\n"
        cv2.imshow("4a", imgContours)

        for i in range(0, len(listOfPossiblePlates)):
            p2fRectPoints = cv2.boxPoints(listOfPossiblePlates[i].rrLocationOfPlateInScene)

            cv2.line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), Main.SCALAR_RED, 2)

            cv2.imshow("4a", imgContours)

            print "possible plate " + str(i) + ", click on any image and press a key to continue . . ."

            cv2.imshow("4b", listOfPossiblePlates[i].imgPlate)
            cv2.waitKey(0)
        # end for

        print "\nplate detection complete, click on any image and press a key to begin char recognition . . .\n"
        cv2.waitKey(0)
    # end if # show steps #########################################################################

    return listOfPossiblePlates
# end function

###################################################################################################
def findPossibleCharsInScene(imgThresh, intCheck):
    listOfPossibleChars = []                # this will be the return value

    intCountOfPossibleChars = 0

    imgThreshCopy = imgThresh.copy()

    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)   # find all contours
    
    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    for i in range(0, len(contours)):                       # for each contour

        if Main.showSteps == True: # show steps ###################################################
            cv2.drawContours(imgContours, contours, i, Main.SCALAR_WHITE)
        # end if # show steps #####################################################################

        possibleChar = PossibleChar.PossibleChar(contours[i])

        if DetectChars.checkIfPossibleChar(possibleChar, intCheck):                   # 면적, 종횡비 등으로 거름. if contour is a possible char, note this does not compare to other chars (yet) . . .
            intCountOfPossibleChars = intCountOfPossibleChars + 1           # increment count of possible chars
            listOfPossibleChars.append(possibleChar)                        # and add to list of possible chars
        # end if
    # end for

    if Main.showSteps == True: # show steps #######################################################
        print "\nstep 2 - len(contours) = " + str(len(contours))                       # 2362 with MCLRNF1 image
        print "step 2 - intCountOfPossibleChars = " + str(intCountOfPossibleChars)       # 131 with MCLRNF1 image
        cv2.imshow("2a", imgContours)                                       #찾아진 contour다 그림                        
    # end if # show steps #########################################################################

    return listOfPossibleChars
# end function


###################################################################################################
def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()           # this will be the return value

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # 람다는 한줄로 정의하는 함수다. sort chars from left to right based on x position

    ##### [plate 중심좌표계산] calculate the center point of the plate
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0 #처음거랑 마지막거 센터평균
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

    ###### [plate높이와 폭계산] calculate plate width and height
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    # end for

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)
    ##### end [plate높이와 폭계산] 

    ######[각도 계산. y차와 거리 이용] calculate correction angle of plate region
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

    #####[위치기록.Box2D형식인듯] pack plate region center point, width and height, and correction angle into rotated rect member variable of plate
    possiblePlate.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

            # final steps are to perform the actual rotation

    #####[회전 및 crop]        # get the rotation matrix for our calculated correction angle
    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)

    height, width, numChannels = imgOriginal.shape      # unpack original image width and height

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))       # rotate the entire image

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

    possiblePlate.imgPlate = imgCropped         # copy the cropped plate image into the applicable member variable of the possible plate

    return possiblePlate
# end function

#################################################################################################################################################
def extractPlate2(imgOriginal, rectBox2D):
    possiblePlate = PossiblePlate.PossiblePlate()           # this will be the return value

    (centerB, (widthB, heightB), angleofRotation) = rectBox2D # height와 width위치에 주의

    #print('[extract2] widthB:{}, heightB:{}, angle:{}').format(widthB, heightB, angleofRotation)
    
    if widthB < heightB: #각에 따라 뒤바뀌기도 한다.
        tempWidthB = widthB
        widthB = heightB
        heightB = tempWidthB
    
    if angleofRotation == -90.0 or angleofRotation == -0.0:
        angleofRotation == 0.0
    elif angleofRotation > -90.0 and angleofRotation < -45.0:
        angleofRotation = angleofRotation + 90
    
    possiblePlate.rrLocationOfPlateInScene = ( tuple(centerB), (widthB, heightB), angleofRotation)

    #####[회전 및 crop]        # get the rotation matrix for our calculated correction angle
    rotationMatrix = cv2.getRotationMatrix2D(tuple(centerB), angleofRotation, 1.0)

    height, width, numChannels = imgOriginal.shape      # unpack original image width and height

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))       # rotate the entire image

    imgCropped = cv2.getRectSubPix(imgRotated, (int(widthB), int(heightB)), tuple(centerB))

    possiblePlate.imgPlate = imgCropped         # copy the cropped plate image into the applicable member variable of the possible plate

    return possiblePlate
# end function









