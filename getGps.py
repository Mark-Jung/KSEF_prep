# -*- coding: utf-8 -*-
#import os
import serial
import time

def get():      
    ser = serial.Serial('/dev/ttyAMA0',115200,timeout=5)
##    print ser.portstr
    cnt=1
    while cnt:
    
        read_ser = ser.readline()
        return read_ser
        #print(read_ser)
        #gpsdata=read_ser.split(',')
        #time.sleep(2)
        #print(gpsdata)
            
##        if len(gpsdata)==4 :
##            #print( "\n"+"lat: "+str(gpsdata[-2])+", lng: "+str(gpsdata[-1])+"\n")
##            #cnt = 0
##            return read_ser

