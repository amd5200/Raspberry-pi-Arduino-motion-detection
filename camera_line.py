# coding: utf -8                   #加上這行才能key中文 要import urllib2
import urllib2
import cv2.cv as cv
import time

cv.NamedWindow("camera", 1)

#capture = cv.CaptureFromCAM(0)
capture = cv.CaptureFromCAM(1)
#capture = cv.CaptureFromCAM(2)


#width = 160 #leave None for auto-detection
#height = 120 #leave None for auto-detection
width = 640 #leave None for auto-detection
height = 480 #leave None for auto-detection
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)

while True:
    
    img = cv.QueryFrame(capture)
######   若解析度有改變，下面劃線座標亦隨之改變##############
    cv.Line(img, (width/2,0),(width/2,height), (0,10,255),3) 
    cv.Line(img, ((width/2-20),(height/2-10)),((width/2-20),(height/2+10)), (0,10,255),2)
    cv.Line(img, ((width/2+20),(height/2-10)),((width/2+20),(height/2+10)), (0,10,255),2) 
    cv.Line(img, (0,height/2),(width,height/2), (0,10,255),3) 
    cv.Line(img, ((width/2-10),(height/2-20)),((width/2+10),(height/2-20)), (0,10,255),2)
    cv.Line(img, ((width/2-10),(height/2+20)),((width/2+10),(height/2+20)), (0,10,255),2)
    cv.ShowImage("camera", img)
     
    if cv.WaitKey(10) == 27:
        break
