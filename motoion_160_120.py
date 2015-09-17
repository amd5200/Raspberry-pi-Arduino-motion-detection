#!/usr/bin/env python
# coding: utf -8                   #加上這行才能key中文 要import urllib2
import urllib2

import cv
#import cv2.cv as cv
import sys
import serial
import time

arduino=serial.Serial('/dev/ttyUSB1',9600)     #set arduino serial port
#width = 160 #leave None for auto-detection
#height = 120 #leave None for auto-detection
width = 320 #leave None for auto-detection
height = 240 #leave None for auto-detection

class Target:

    def __init__(self):
        
        
        self.capture = cv.CaptureFromCAM(2)
        cv.NamedWindow("Target", 1)

###########################################################################

#        width = 160 #leave None for auto-detection
#        height = 120 #leave None for auto-detection
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH,width) 
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 
        """
        if width is None:
             width = int(cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH))
        else:
    	     cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

        if height is None:
             height = int(cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
        else:
	     cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 
        """
############################################################################################


    def run(self):
        # Capture first frame to get size
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)
        color_image = cv.CreateImage(cv.GetSize(frame), 8, 3)
        grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
        moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)

        first = True





        while True:
            closest_to_left = cv.GetSize(frame)[0]
            closest_to_right = cv.GetSize(frame)[1]

            color_image = cv.QueryFrame(self.capture)

            # Smooth to get rid of false positives
            cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)
            
            if first:
                difference = cv.CloneImage(color_image)
                temp = cv.CloneImage(color_image)
                cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
                first = False
            else:
                cv.RunningAvg(color_image, moving_average, 0.020, None)
            
            # Convert the scale of the moving average.
            cv.ConvertScale(moving_average, temp, 1.0, 0.0)

            # Minus the current frame from the moving average.
            cv.AbsDiff(color_image, temp, difference)

            # Convert the image to grayscale.
            cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)

            # Convert the image to black and white.
            cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

            # Dilate and erode to get people blobs
            cv.Dilate(grey_image, grey_image, None, 18)
            cv.Erode(grey_image, grey_image, None, 10)

            storage = cv.CreateMemStorage(0)
            contour = cv.FindContours(grey_image, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            points = []

            while contour:
                bound_rect = cv.BoundingRect(list(contour))
                contour = contour.h_next()

                pt1 = (bound_rect[0], bound_rect[1])
                pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                points.append(pt1)
                points.append(pt2)
                cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 3)

            if len(points):
                center_point = reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
                #cv.Circle(color_image, center_point, 40, cv.CV_RGB(255, 255, 255), 1)
                #cv.Circle(color_image, center_point, 30, cv.CV_RGB(255, 100, 0), 1)
                #cv.Circle(color_image, center_point, 20, cv.CV_RGB(255, 255, 255), 1)
                cv.Circle(color_image, center_point, 10, cv.CV_RGB(255, 100, 0), 8)
                print center_point     

########################################  contour center  ####################################################################
                
                cx = ((bound_rect[2])/2)+bound_rect[0]              #(0,0)################
                cy = ((bound_rect[3])/2)+bound_rect[1]              ######################   
                print cx, cy                                        ######################<--160x120 pix
                                                                    ######################
                                                                    ############(160,120)#
######################################### servo motor ######################################################


                if cx < width*5/ 10 :                  
                     arduino.write('e')                
                     print 'e'
                if cx < width*4/ 10 :                  
                     arduino.write('d')                
                     print 'd'
                if cx < width*3/ 10 :                  
                     arduino.write('c')                
                     print 'c'                        
		if cx < width*2/ 10 :
                     arduino.write('b')
                     print 'b'
		if cx < width/ 10 :
                     arduino.write('a')
                     print 'a'

                if cx > width*6 / 10 :
                     arduino.write('f')
                     print 'f'
                if cx > width*7/ 10 :
                     arduino.write('g')
                     print 'g'
                if cx > width*8/ 10 :
                     arduino.write('h')
                     print 'h'
                if cx > width*9/ 10 :
                     arduino.write('i')
                     print 'i'

                if cy < height*5/ 10:
                     arduino.write('n')
                     print 'n'
                if cy < height*4/ 10:
                     arduino.write('m')
                     print 'm'
                if cy < height*3/ 10:
                     arduino.write('l')
                     print 'l'
                if cy < height*2/ 10:
                     arduino.write('k')
                     print 'k'
                if cy < height/ 10:
                     arduino.write('j')
                     print 'j'


                if cy > height*6 / 10:
                     arduino.write('o')
                     print 'o'
                if cy > height*7 / 10:
                     arduino.write('p')
                     print 'p'
                if cy > height*8 / 10:
                     arduino.write('q')
                     print 'q'     
                if cy > height*9 / 10:
                     arduino.write('r')
                     print 'r'



####################################################################################################################### 


            cv.ShowImage("Target", color_image)

            # Listen for ESC key
            c = cv.WaitKey(7) % 0x100
            if c == 27:
                break

if __name__=="__main__":
    t = Target()
    t.run()
