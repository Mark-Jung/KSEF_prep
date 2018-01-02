# -*- coding: utf-8 -*-
import carPos
import uploadFiles
import downloadList

suspectList = downloadList.getList()


car_data = '89자6012'
carD =  car_data.decode('utf-8')
print(suspectList.find(carD))

if suspectList.find(carD) > -1:
    print('in the list')
    tempString='2017.09.26,07:12:48.012,37.504342,127.036213'
    tempString = tempString + '\n'
    carPos.write(tempString,car_data)
    uploadFiles.upload(car_data[-4:])
