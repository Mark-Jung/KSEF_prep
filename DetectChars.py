# DetectChars.py
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
import random

import Main
import Preprocess
import PossibleChar

# module level variables ##########################################################################

kNearest = cv2.ml.KNearest_create()

        # constants for checkIfPossibleChar, this checks one possible char only (does not compare to another char)
MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8
MIN_PIXEL_AREA = 80

MIN_ASPECT_RATIO = 0.1
MAX_ASPECT_RATIO = 1.3
################################################
MIN_PIXEL_WIDTH_B = 2
MIN_PIXEL_HEIGHT_B = 6
MIN_PIXEL_AREA_B = 50
MIN_ASPECT_RATIO_B = 0.1
MAX_ASPECT_RATIO_B = 2.5
GAP_THRESHOLD = 6
DISTANCE_THRESHOLD = 6
MAX_CHANGE_IN_AREA_B = 0.8 #원래0.5
MAX_CHANGE_IN_WIDTH_B = 0.8 #원래0.8
MAX_CHANGE_IN_HEIGHT_B = 0.8 #원래0.2
SMALL_CHAR_RATIO = 0.8
ROW_CUT_RATIO = 1.5
RESIZE_LONG_WIDTH = 300  #520:335
RESIZE_SHORT_WIDTH = 193
##################################################
        # constants for comparing two chars
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5 #원래0.5

MAX_CHANGE_IN_WIDTH = 0.8 #원래0.8
MAX_CHANGE_IN_HEIGHT = 0.2 #원래0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

        # other constants
MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100

###################################################################################################
def loadKNNDataAndTrainKNN():
    allContoursWithData = []                # declare empty lists,
    validContoursWithData = []              # we will fill these shortly

    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)                  # read in training classifications
    except:                                                                                 # if file could not be opened
        print "error, unable to open classifications.txt, exiting program\n"                # show error message
        os.system("pause")
        return False                                                                        # and return False
    # end try

    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                 # read in training images
    except:                                                                                 # if file could not be opened
        print "error, unable to open flattened_images.txt, exiting program\n"               # show error message
        os.system("pause")
        return False                                                                        # and return False
    # end try

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train

    kNearest.setDefaultK(1)                                                             # set default K to 1

    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)           # train KNN object

    return True                             # if we got here training was successful so return true
# end function

###################################################################################################
def detectCharsInPlates(listOfPossiblePlates):
    intPlateCounter = 0
    imgContours = None
    contours = []

    if len(listOfPossiblePlates) == 0:          # if list of possible plates is empty
        return listOfPossiblePlates             # return
    # end if

            # at this point we can be sure the list of possible plates has at least one plate

    for possiblePlate in listOfPossiblePlates:          # for each possible plate, this is a big for loop that takes up most of the function

        possiblePlate.imgGrayscale, possiblePlate.imgThresh = Preprocess.preprocess(possiblePlate.imgPlate)     # preprocess to get grayscale and threshold images

        if Main.showSteps == True: # show steps ###################################################
            cv2.imshow("5a", possiblePlate.imgPlate)
            cv2.imshow("5b", possiblePlate.imgGrayscale)
            cv2.imshow("5c", possiblePlate.imgThresh)
        # end if # show steps #####################################################################


        ######[리사이즈 비율계산]###########################################################################    
        resizeFactor = findResizeFactor(possiblePlate)
        #print('[detectCharsInPlates] resizeFactor:{}').format(resizeFactor)
        
        #####[확대_..] increase size of plate image for easier viewing and char detection
        possiblePlate.imgThresh = cv2.resize(possiblePlate.imgThresh, (0, 0), fx = resizeFactor, fy = resizeFactor)

        #####[다시 이진화.그레이제거 목적인 듯.0보다크면 무조건255] threshold again to eliminate any gray areas
        thresholdValue, possiblePlate.imgThresh = cv2.threshold(possiblePlate.imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        if Main.showSteps == True: # show steps ###################################################
            cv2.imshow("5d", possiblePlate.imgThresh)
        # end if # show steps #####################################################################

                # find all possible chars in the plate,
        #####[PossibleChar리스트를 다시 생성]        # this function first finds all contours, then only includes contours that could be chars (without comparison to other chars yet)
        listOfPossibleCharsInPlate = findPossibleCharsInPlate(possiblePlate.imgGrayscale, possiblePlate.imgThresh, 2) #imgGrayscale은 안쓰는듯

        if Main.showSteps == True: # show steps ###################################################
            height2, width2, numChannels = possiblePlate.imgPlate.shape
            height, width  = int(height2*resizeFactor), int(width2*resizeFactor)
            imgContours = np.zeros((height, width, 3), np.uint8)
            del contours[:]                                         # clear the contours list

            for possibleChar in listOfPossibleCharsInPlate:
                contours.append(possibleChar.contour)
            # end for

            cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)

            cv2.imshow("6", imgContours)
        # end if # show steps #####################################################################
        
        
###########################################################################################################            
        listOfPossibleCharsInPlate = removeInnerOverlappingChars(listOfPossibleCharsInPlate)  #느리면 제거..하면 안됨
####################################################################################################################         
#        for possibleChar in listOfPossibleCharsInPlate:
#            print('w:{},h:{},area:{}').format(possibleChar.intBoundingRectWidth,possibleChar.intBoundingRectHeight,possibleChar.intBoundingRectArea)
####################################################################################################################
        '''listOfPossibleCharsInPlate = mergeCloseChar(listOfPossibleCharsInPlate)
        
        if Main.showSteps == True: # show steps ###################################################
            height, width, numChannels = possiblePlate.imgPlate.shape
            #height, width, numChannels = possiblePlate.imgThresh.shape #확대한 크기로 안 나와서 수정함...오류나네? 확대를 안함
            imgContours = np.zeros((height, width, 3), np.uint8)
            del contours[:]                                         # clear the contours list

            for possibleChar in listOfPossibleCharsInPlate:
                contours.append(possibleChar.contour)
                #print('w:{},h:{},area:{}').format(possibleChar.intBoundingRectWidth,possibleChar.intBoundingRectHeight,possibleChar.intBoundingRectArea)
            # end for

            cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)

            cv2.imshow("7b_merged", imgContours)'''
        # end if # show steps #####################################################################


#######################################################################################################################        
 
        #####[글자 그룹의 리스트를 다시작성]        # given a list of all possible chars, find groups of matching chars within the plate
        #listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars2(listOfPossibleCharsInPlate,2)
        listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars2(listOfPossibleCharsInPlate)
        #print('[detectCharsInPlates] No. of char groups in plate:{}').format(len(listOfListsOfMatchingCharsInPlate))

        if Main.showSteps == True: # show steps ###################################################
            imgContours = np.zeros((height, width, 3), np.uint8)
            del contours[:]

            for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
                intRandomBlue = random.randint(0, 255)
                intRandomGreen = random.randint(0, 255)
                intRandomRed = random.randint(0, 255)

                for matchingChar in listOfMatchingChars:
                    contours.append(matchingChar.contour)
                # end for
                cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            # end for
            cv2.imshow("7", imgContours)
        # end if # show steps #####################################################################
        ###### 인식된 글자 그룹이 없을 때 처리
        if (len(listOfListsOfMatchingCharsInPlate) == 0):			# if no groups of matching chars were found in the plate

            if Main.showSteps == True: # show steps ###############################################
                print "chars found in plate number " + str(intPlateCounter) + " = (none), click on any image and press a key to continue . . ."
                intPlateCounter = intPlateCounter + 1
                cv2.destroyWindow("8_merge")
                cv2.destroyWindow("9_rm_circle")
                cv2.destroyWindow("10")
                cv2.waitKey(0)
            # end if # show steps #################################################################

            possiblePlate.strChars = ""
            continue						# go back to top of for loop
        # end if
   
        ####[인접글자 합치기 ]#################################################################################
        listOfListsOfMatchingCharsInPlate = mergeCloseChar2(listOfListsOfMatchingCharsInPlate)
        ###################################################################################################
        
        if Main.showSteps == True: # show steps ###################################################
            imgContours = np.zeros((height, width, 3), np.uint8)

            for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
                intRandomBlue = random.randint(0, 255)
                intRandomGreen = random.randint(0, 255)
                intRandomRed = random.randint(0, 255)

                del contours[:]

                for matchingChar in listOfMatchingChars:
                    contours.append(matchingChar.contour)
                # end for

                cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            # end for
            cv2.imshow("8_merge", imgContours)
        # end if # show steps #####################################################################
        
       
        
        #####[각 글자그룹을 x기준으로 정렬 & 겹치는 테두리는 제거]
        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):                              # within each list of matching chars
            listOfListsOfMatchingCharsInPlate[i].sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right
            #listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i]) #안쪽에 있는 테두리 없앤다. 앞에서 함            # and remove inner overlapping chars
        # end for
        
        ####[원 및 작은 테두리 제거]############################################################################################
        listOfListsOfMatchingCharsInPlate = removeSmallCnt(listOfListsOfMatchingCharsInPlate, possiblePlate)
      
        ##########################################################################################################

        #####[글자 그룹의 길이 중 최대값과 인덱스를 찾는다.]        # within each possible plate, suppose the longest list of potential matching chars is the actual list of chars
        '''intLenOfLongestListOfChars = 0
        intIndexOfLongestListOfChars = 0

                # loop through all the vectors of matching chars, get the index of the one with the most chars
        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
            if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
                intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
                intIndexOfLongestListOfChars = i
            # end if
        # end for'''

        #####[길이가 젤 긴 글자그룹만 선택]        # suppose that the longest list of matching chars within the plate is the actual list of chars
        #longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]
        
        #####[길이가 짧은 순으로 정렬]##############################################################
        listOfListsOfMatchingCharsInPlate.sort(key = lambda listofLists: len(listofLists))

        if Main.showSteps == True: # show steps ###################################################
            imgContours = np.zeros((height, width, 3), np.uint8)
            del contours[:]
            
            for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
    
                for matchingChar in listOfListsOfMatchingCharsInPlate[i]:
                    contours.append(matchingChar.contour)
                # end for
    
                cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)

            cv2.imshow("9_rm_circle", imgContours)
        # end if # show steps #####################################################################
        
        #####[길이가 젤 긴 글자그룹으로 문자인식 후 저장]
        #possiblePlate.strChars = recognizeCharsInPlate(possiblePlate.imgThresh, longestListOfMatchingCharsInPlate)
        
        
        ####[글자인식]###########################################################
        possiblePlate.strChars=''
        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
            possiblePlate.strChars = possiblePlate.strChars + recognizeCharsInPlate(possiblePlate.imgThresh, listOfListsOfMatchingCharsInPlate[i])
        
        if Main.showSteps == True: # show steps ###################################################
            print "chars found in plate number " + str(intPlateCounter) + " = " + possiblePlate.strChars + ", click on any image and press a key to continue . . ."
            #print "chars found in plate number = , click on any image and press a key to continue . . ." 
            intPlateCounter = intPlateCounter + 1
            cv2.waitKey(0)
        # end if # show steps #####################################################################

    # end of big for loop that takes up most of the function
    #####여기까지 for문. 각 후보 플레이트에 대해 글자인식을 반복수행한다.
    
    if Main.showSteps == True:
        print "\nchar detection complete, click on any image and press a key to continue . . .\n"
        cv2.waitKey(0)
    # end if

    return listOfPossiblePlates
# end function
#################################################################################################
def findResizeFactor(possiblePlate):
    height, width = possiblePlate.imgThresh.shape
    aspectRatio = width/height
    if aspectRatio > 2.5:               #긴거 폭233
        fx = RESIZE_LONG_WIDTH/float(width)
        #print('[findResizeFactor] resizeFactor:{}').format(fx)
    else:                               #짧은거 150
        fx = RESIZE_SHORT_WIDTH/float(width)
        
    return fx
        
##################################################################################################
def mergeCloseChar(listOfListsOfMatchingCharsInPlate):
    mergedListOfListsOfMatchingCharsInPlate = []
    for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
        maxArea = 0
        for matchingChar in listOfMatchingChars:
            if matchingChar.intBoundingRectArea > maxArea:
                maxArea = matchingChar.intBoundingRectArea
        
        listofAll = listOfMatchingChars
        
        for matchingCharA in listOfMatchingChars:
            if matchingCharA.intBoundingRectArea > maxArea*SMALL_CHAR_RATIO: #큰 글자 무시
                continue
            [xA,yA,widthA,heightA] = matchingCharA.boundingRect
            for matchingCharB in listOfMatchingChars:
                if matchingCharB.intBoundingRectArea > maxArea*SMALL_CHAR_RATIO: #큰 글자 무시
                    continue
                if matchingCharA == matchingCharB:
                    continue
                [xB,yB,widthB,heightB] = matchingCharB.boundingRect
                if abs((xA+widthA/2) - (xB+widthB/2)) > abs((yA+heightA/2) - (yB+heightB/2)): #중점 거리비교
                    dist = abs((xA+widthA/2) - (xB+widthB/2)) - widthA/2 - widthB/2 #간격계산:중점거리에서 반경제거
                else:
                    dist = abs((yA+heightA/2) - (yB+heightB/2)) - heightA/2 - heightB/2
                #print(dist)
                if dist < GAP_THRESHOLD:
                    cont = np.vstack([matchingCharA.contour,matchingCharB.contour])
                    listofAll.append(PossibleChar.PossibleChar(cont)) 
                    if matchingCharA in listofAll: listofAll.remove(matchingCharA)
                    if matchingCharB in listofAll: listofAll.remove(matchingCharB)
        
        print('[mergeCloseChar]length of list:{}').format(len(listofAll))
        listofAll = list(set(listofAll))
        print('[mergeCloseChar]length of list:{}').format(len(listofAll))
        mergedListOfListsOfMatchingCharsInPlate.append(listofAll)
                    
    return mergedListOfListsOfMatchingCharsInPlate
# end fuction
#################################################################################################################
def mergeCloseChar2(listOfListsOfMatchingCharsInPlate):
    #print('[mergeCloseChar2]length of list:{}').format(len(listOfListsOfMatchingCharsInPlate))
    mergedListOfListsOfMatchingCharsInPlate = []
    for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
        maxArea = 0
        for matchingChar in listOfMatchingChars:
            if matchingChar.intBoundingRectArea > maxArea:
                maxArea = matchingChar.intBoundingRectArea
        
        listofMergedResult = []
        listofSmallChars = []
        listToRemove = []
        listToCheck = []
        for matchingCharA in listOfMatchingChars:  #대입형태로 카피해서 쓰더라도 멤버를 제거하면 실시간 반영되는 듯.. 제거에 주의
            if matchingCharA.intBoundingRectArea > maxArea*SMALL_CHAR_RATIO: #큰 글자 무시
                continue
            [xA,yA,widthA,heightA] = matchingCharA.boundingRect
            for matchingCharB in listOfMatchingChars:
                if matchingCharB.intBoundingRectArea > maxArea*SMALL_CHAR_RATIO: #큰 글자 무시
                    continue
                if matchingCharA == matchingCharB:
                    continue
                [xB,yB,widthB,heightB] = matchingCharB.boundingRect
                distX = abs((xA+widthA/2) - (xB+widthB/2)) - widthA/2 - widthB/2
                if abs((yA+heightA/2) - (yB+heightB/2)) < DISTANCE_THRESHOLD and distX < GAP_THRESHOLD: #x방향 합치기
                    cont = np.vstack([matchingCharA.contour, matchingCharB.contour])
                    tempChar = PossibleChar.PossibleChar(cont)
                    tempRect = tempChar.boundingRect
                    if tempRect not in listToCheck: #중복방지
                        listofMergedResult.append(tempChar)
                        listToCheck.append(tempRect)
                        listToRemove.append(matchingCharA)
                        listToRemove.append(matchingCharB)
            listofSmallChars.append(matchingCharA) #작은 크기의 모든 글자
        #end for
        listOfMatchingChars = list(set(listOfMatchingChars)-set(listofSmallChars)) #큰 글자 집합
        listofSmallChars = list(set(listofSmallChars)-set(listToRemove)) #작은 글자 중 합쳐진 글자 제거
        listofSmallChars = listofSmallChars + listofMergedResult         #조각들의 모임
        
        #end for
        #2nd merge process, y축 방향, 다층일 수 있다.
        secondMgdChars = []
        listToRm = []
        listToch = []
        for matchingCharA in listofSmallChars:
            [xA,yA,widthA,heightA] = matchingCharA.boundingRect
            listofCntClosetoA = []
            for matchingCharB in listofSmallChars:
                if matchingCharA == matchingCharB:
                    continue
                [xB,yB,widthB,heightB] = matchingCharB.boundingRect
                if abs((xA+widthA/2) - (xB+widthB/2)) < DISTANCE_THRESHOLD: #y축 방향
                    listofCntClosetoA.append(matchingCharB.contour)
                    listToRm.append(matchingCharB)
            #end for        
            if len(listofCntClosetoA) > 0: #근접 글자가 있는 경우
                listofCntClosetoA.append(matchingCharA.contour) #자기 자신 추가
                cont = np.vstack(listofCntClosetoA[i] for i in range(0,len(listofCntClosetoA)))
                tempChar = PossibleChar.PossibleChar(cont)
                tempRect = tempChar.boundingRect
                if tempRect not in listToch: #중복방지
                    secondMgdChars.append(tempChar)
                    listToch.append(tempRect)
                    listToRm.append(matchingCharA)
        #end for
        listofSmallChars = list(set(listofSmallChars)-set(listToRm)) #작은 조각 모임에서 합쳐진 요소 제거
        listofSmallChars = listofSmallChars + list(set(secondMgdChars))         #합쳐진 요소 추가'''
        
        mergedListOfListsOfMatchingCharsInPlate.append(listOfMatchingChars+listofSmallChars)
                    
    return mergedListOfListsOfMatchingCharsInPlate
# end fuction
##################################################################################################
def removeSmallCnt(listOfListsOfMatchingCharsInPlate, possiblePlate):
    
    height, width = possiblePlate.imgThresh.shape
    aspectRatio = width/height
    
    
    for i in range(0,len(listOfListsOfMatchingCharsInPlate)): 
        itoRm = []
        if len(listOfListsOfMatchingCharsInPlate[i]) < 3:    #3자 미만 삭제
            itoRm.append(i)
    if len(itoRm) > 0 :
        count = 0
        for k in itoRm:
            del listOfListsOfMatchingCharsInPlate[k-count]
            count = count + 1
            
    #x좌표로 정렬된 상태다.
    for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
        if len(listOfMatchingChars) > 2:
            maxHeight = 0
            indextoRemove=[]
            for i in range(0,len(listOfMatchingChars)):
                if listOfMatchingChars[i].intBoundingRectHeight > maxHeight:
                    maxHeight = listOfMatchingChars[i].intBoundingRectHeight
            for i in range(0,len(listOfMatchingChars)):                           #remove small chars
                if listOfMatchingChars[i].intBoundingRectHeight < maxHeight*0.7:
                    indextoRemove.append(i)                                       #중간에 지워버리면 for를 다 돌지 못하고 오류남
            if len(indextoRemove)  > 0:
                count = 0
                for k in indextoRemove:
                    del listOfMatchingChars[k-count]                                #지울때 마다 갯수 줄어듬
                    count = count + 1
                    
        ### 양 끝 삭제 #################################################  
        if len(listOfMatchingChars) > 2 and aspectRatio > 2.5:
            if listOfMatchingChars[-1].intCenterX > width-20:
                del listOfMatchingChars[-1]
            if listOfMatchingChars[0].intCenterX < 20:
                del listOfMatchingChars[0]
                
#        else: 
#            del listOfMatchingChars                                                 #3자 미만 삭제
#            if listOfMatchingChars[0].intBoundingRectHeight < maxHeight*0.7:
#                if listOfMatchingChars[0].intCenterX < 20:
#                    del listOfMatchingChars[0]
#            if listOfMatchingChars[-1].fltAspectRatio < maxHeight*0.7: 
#                if listOfMatchingChars[-1].intCenterX > width-20:
#                    del listOfMatchingChars[-1]
#                    print('[removeSideCircle] aspR:{}').format(listOfMatchingChars[-1].fltAspectRatio)
            

    
    return listOfListsOfMatchingCharsInPlate    
    
###################################################################################################
def findPossibleCharsInPlate(imgGrayscale, imgThresh, intCheck):
    ##### 글자같은 contours를 찾고 PossibleChar형식의 리스트로 만든다.
    listOfPossibleChars = []                        # this will be the return value
    contours = []
    imgThreshCopy = imgThresh.copy()

            # find all contours in plate
    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:                        # for each contour
        possibleChar = PossibleChar.PossibleChar(contour)

        if checkIfPossibleChar(possibleChar, intCheck):              # if contour is a possible char, note this does not compare to other chars (yet) . . .
            listOfPossibleChars.append(possibleChar)       # add to list of possible chars
        # end if
    # end if

    return listOfPossibleChars
# end function

###################################################################################################
def checkIfPossibleChar(possibleChar, intCheck):
    #####면적, 폭, 높이, 종횡비로 가른다.
            # this function is a 'first pass' that does a rough check on a contour to see if it could be a char,
            # note that we are not (yet) comparing the char to other chars to look for a group
    if intCheck == 1:
        if (cv2.contourArea(possibleChar.contour) > MIN_PIXEL_AREA and
            possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
            MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
            return True
        else:
            return False
    elif intCheck == 2:
        #print('[checkIfPossibleChar] width:{}, height:{},aspRatio:{}').format(possibleChar.intBoundingRectWidth ,possibleChar.intBoundingRectHeight ,possibleChar.fltAspectRatio )
        if (cv2.contourArea(possibleChar.contour) > MIN_PIXEL_AREA_B and
            possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH_B and possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT_B and
            MIN_ASPECT_RATIO_B < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_ASPECT_RATIO_B):
            return True
        else:
            return False
    # end if
# end function


###################################################################################################
def findListOfListsOfMatchingChars2(listOfPossibleChars):
    listOfListsOfMatchingChars = []
    rowIndex = []
    listA = listOfPossibleChars  
    listA.sort(key = lambda matchingChar: matchingChar.intCenterY)        
    for i in range(0, len(listA)-1):
        distY = listA[i+1].intCenterY - listA[i].intCenterY
        if distY > listA[i].intBoundingRectHeight*ROW_CUT_RATIO:
            rowIndex.append(i)
    if len(rowIndex) == 0:
        listOfListsOfMatchingChars.append(listA)
    elif len(rowIndex) == 1:
        listOfListsOfMatchingChars.append(listA[0:rowIndex[0]+1])
        listOfListsOfMatchingChars.append(listA[rowIndex[0]+1:])
    else:
        print('[findListOfListsOfMatchingChars2] Too many Groups!')
        listOfListsOfMatchingChars=[]
    return listOfListsOfMatchingChars


###################################################################################################
def findListOfListsOfMatchingChars(listOfPossibleChars, intCheck):
            # with this function, we start off with all the possible chars in one big list
            # the purpose of this function is to re-arrange the one big list of chars into a list of lists of matching chars,
            # note that chars that are not found to be in a group of matches do not need to be considered further
    listOfListsOfMatchingChars = []                  # this will be the return value
    
    
    for possibleChar in listOfPossibleChars:                        # for each possible char in the one big list of chars
        #possibleChar와 가까이에 있고 비슷한 크기의 contour리스트를 만들고 자기도 추가한다.
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars, intCheck)        # find all chars in the big list that match the current char
        listOfMatchingChars.append(possibleChar)                # also add the current char to current possible list of matching chars

        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS:    #3이네..  # if current possible list of matching chars is not long enough to constitute a possible plate
            continue                            # jump back to the top of the for loop and try again with next char, note that it's not necessary
                                                # to save the list in any way since it did not have enough chars to be a possible plate
        # end if

        #if 통과했으면 글자조합 리스트에 추가한다.                     # if we get here, the current list passed test as a "group" or "cluster" of matching chars
        listOfListsOfMatchingChars.append(listOfMatchingChars)      # so add to our list of lists of matching chars

        listOfPossibleCharsWithCurrentMatchesRemoved = []

                                                # remove the current list of matching chars from the big list so we don't use those same chars twice,
        #중복연산을 피하기 위해 새리스트를 만든다.                  # make sure to make a new big list for this since we don't want to change the original big list
        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))
        #세로 만든 리스트로 자기 자신 호출... 리스트의 리스트가 반환된다.
        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved, intCheck)      # recursive call
        #리스트의 리스트가 반환되면 리스트를 하나씩 꺼내서 이 함수의 리스트 오브 리스트에 추가한다.
        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:        # for each list of matching chars found by recursive call
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)             # add to our original list of lists of matching chars
        # end for

        break       # exit for

    # end for

    return listOfListsOfMatchingChars
# end function

###################################################################################################
def findListOfMatchingChars(possibleChar, listOfChars, intCheck): #possibleChar와 가까이에 있고 비슷한 크기의 contour리스트를 만든다.
            # the purpose of this function is, given a possible char and a big list of possible chars,
            # find all chars in the big list that are a match for the single possible char, and return those matching chars as a list
    listOfMatchingChars = []                # this will be the return value

    for possibleMatchingChar in listOfChars:                # for each char in big list
        if possibleMatchingChar == possibleChar:    # if the char we attempting to find matches for is the exact same char as the char in the big list we are currently checking
                                                    # then we should not include it in the list of matches b/c that would end up double including the current char
            continue                                # so do not add to list of matches and jump back to top of for loop
        # end if
                    # compute stuff to see if chars are a match
        fltDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar)

        fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)
        ##################################################################################################################
        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea-possibleChar.intBoundingRectArea)) / float(max(possibleMatchingChar.intBoundingRectArea,possibleChar.intBoundingRectArea)) #넓이 증가율
        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth-possibleChar.intBoundingRectWidth)) / float(max(possibleMatchingChar.intBoundingRectWidth, possibleChar.intBoundingRectWidth)) #폭 증가율
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight-possibleChar.intBoundingRectHeight)) / float(max(possibleMatchingChar.intBoundingRectHeight, possibleChar.intBoundingRectHeight)) #높이 증가율
        ##################################################################################################################        
        if intCheck == 1 :
                # check if chars match
            if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and  #거리가 대각선 5배보다 가까울 때, 아마 5글자로 생각한 듯
                fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and                                       #각도 12도 차이 미만
                fltChangeInArea < MAX_CHANGE_IN_AREA and                                                   #0.5
                fltChangeInWidth < MAX_CHANGE_IN_WIDTH and                                               #0.8
                fltChangeInHeight < MAX_CHANGE_IN_HEIGHT):                                               #0.2 
    
                listOfMatchingChars.append(possibleMatchingChar)        # if the chars are a match, add the current char to list of matching chars
            # end if
        elif intCheck == 2:
            if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and  #거리가 대각선 5배보다 가까울 때, 아마 5글자로 생각한 듯
                fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and                                       #각도 12도 차이 미만
                fltChangeInArea < MAX_CHANGE_IN_AREA_B and                                                   #0.5
                fltChangeInWidth < MAX_CHANGE_IN_WIDTH_B and                                               #0.8
                fltChangeInHeight < MAX_CHANGE_IN_HEIGHT_B):                                               #0.2 
    
                listOfMatchingChars.append(possibleMatchingChar)
            
    # end for

    return listOfMatchingChars                  # return result
# end function

###################################################################################################
# use Pythagorean theorem to calculate distance between two chars
def distanceBetweenChars(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))
# end function

###################################################################################################
# use basic trigonometry (SOH CAH TOA) to calculate angle between chars
def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:                           # check to make sure we do not divide by zero if the center X positions are equal, float division by zero will cause a crash in Python
        fltAngleInRad = math.atan(fltOpp / fltAdj)      # if adjacent is not zero, calculate angle
    else:
        fltAngleInRad = 1.5708                          # if adjacent is zero, use this as the angle, this is to be consistent with the C++ version of this program
    # end if

    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)       # calculate angle in degrees

    return fltAngleInDeg
# end function

###################################################################################################
# if we have two chars overlapping or to close to each other to possibly be separate chars, remove the inner (smaller) char,
# this is to prevent including the same char twice if two contours are found for the same char,
# for example for the letter 'O' both the inner ring and the outer ring may be found as contours, but we should only include the char once
#####[한글자 안에서 겹쳐서 따지는 contour를 제거하기 위함]
def removeInnerOverlappingChars(listOfMatchingChars):
    listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)                # this will be the return value
    
    for currentChar in listOfMatchingChars:
        for otherChar in listOfMatchingChars:
            if currentChar != otherChar:        # if current char and other char are not the same char . . .
                ##### 거리가 가까우면 넓이를 비교해서 안쪽걸 지운다.                                                            # if current char and other char have center points at almost the same location . . .
                if distanceBetweenChars(currentChar, otherChar) < (currentChar.fltDiagonalSize * MIN_DIAG_SIZE_MULTIPLE_AWAY):
                                # if we get in here we have found overlapping chars
                                # next we identify which char is smaller, then if that char was not already removed on a previous pass, remove it
                    if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:         # if current char is smaller than other char
                        if currentChar in listOfMatchingCharsWithInnerCharRemoved:              # if current char was not already removed on a previous pass . . .
                            listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)         # then remove current char
                        # end if
                    else:                                                                       # else if other char is smaller than current char
                        if otherChar in listOfMatchingCharsWithInnerCharRemoved:                # if other char was not already removed on a previous pass . . .
                            listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)           # then remove other char
                        # end if
                    # end if
                # end if
            # end if
        # end for
    # end for

    return listOfMatchingCharsWithInnerCharRemoved
# end function

###################################################################################################
# this is where we apply the actual char recognition
def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    strChars = ""               # this will be the return value, the chars in the lic plate

    height, width = imgThresh.shape

    imgThreshColor = np.zeros((height, width, 3), np.uint8)

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)  #이미 되어있을 건데 또함      # sort chars from left to right

    cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR, imgThreshColor)     #contour그릴라고 컬러로                # make color version of threshold image so we can draw contours in color on it
###################################################################################################################################  
    words = {'a':'가', 'l':'서', 'v':'조', 'F':'아', 
            'b':'나', 'm':'어', 'w':'구', 'G':'바', 
            'c':'다', 'n':'저', 'x':'누', 'H':'사', 
            'd':'라', 'o':'고', 'y':'두', 'I':'자', 
            'e':'마', 'p':'노', 'z':'루', 'J':'배', 
            'f':'거', 'q':'도', 'A':'무', 'K':'하', 
            'g':'너', 'r':'로', 'B':'부', 'L':'허', 
            'h':'더', 's':'모', 'C':'수', 'M':'호', 
            'i':'러', 't':'보', 'D':'우', 
            'j':'머', 'u':'소', 'E':'주', 
            'k':'버', 'N':'오', 'O':'경기', 'P':'서울',
            '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', 
            '6':'6', '7':'7', '8':'8', '9':'9'}
################################################################################################################################   
    for currentChar in listOfMatchingChars:                                         # for each char in plate
        #####[합치기 하려면 참고할 것] 
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))

        cv2.rectangle(imgThreshColor, pt1, pt2, Main.SCALAR_GREEN, 2)           # draw green box around the char

        #####[crop.Y가 먼저다.]        # crop char out of threshold image
        imgROI = imgThresh[currentChar.intBoundingRectY : currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
                           currentChar.intBoundingRectX : currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_CHAR_IMAGE_WIDTH, RESIZED_CHAR_IMAGE_HEIGHT))     #20x30      # resize image, this is necessary for char recognition

        npaROIResized = imgROIResized.reshape((1, RESIZED_CHAR_IMAGE_WIDTH * RESIZED_CHAR_IMAGE_HEIGHT)) #1차원 배열로 만든다.        # flatten image into 1d numpy array

        npaROIResized = np.float32(npaROIResized)       #float로 변환        # convert from 1d numpy array of ints to 1d numpy array of floats

        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)              # finally we can call findNearest !!!

        strCurrentChar = str(chr(int(npaResults[0][0])))            # get character from results
        strConveredChar = words[strCurrentChar]
        strChars = strChars + strConveredChar                        # append current char to full string

    # end for

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("10", imgThreshColor)
    # end if # show steps #########################################################################

    return strChars
# end function








