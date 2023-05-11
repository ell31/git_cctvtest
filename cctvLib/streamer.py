# -*- encoding: utf-8 -*-
#-------------------------------------------------#
# Date created          : 2020. 8. 18.
# Date last modified    : 2020. 8. 19.
# Author                : ell31@naver.com
# Site                  : 
# License               : 
# Version               : 0.1.0
# Python Version        : 3.6+
#-------------------------------------------------#

import time
import cv2
import imutils
import platform
import numpy as np
from threading import Thread
from queue import Queue
import datetime
import requests
import os

class Streamer :
    
    def __init__(self ):
        
        if cv2.ocl.haveOpenCL() :
            cv2.ocl.setUseOpenCL(True)
        #print('[Streamer] ', 'OpenCL : ', cv2.ocl.haveOpenCL())
            
        self.capture = None
        self.thread = None
        self.width = 640
        self.height = 360
        self.stat = False
        self.current_time = time.time()
        self.preview_time = time.time()
        self.sec = 0
        self.Q = Queue(maxsize=16)
        self.started = False
        self.exit = False
        self.isinference = False
        self.inferenceTime = 10.0
        self.inferenceCount = 0
        self.fpsValue = 0
        
    def run(self, src = 0, mac = 0, event = "" ) :
        #self.stop()
        self.mac = mac
        self.url = src
        self.event = event
        print('[CMD RUN] ', 'MAC : ', self.mac)
        self.started = False
        self.exit = False
        
        self.capture = cv2.VideoCapture( self.url )
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.started = True
        print('[Streamer Start] ', 'MAC : ', self.mac)
        
        if self.thread is None :
            
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon = False
            self.thread.start()
        
        
    def stop(self):
        print('[CMD Stop] ', 'MAC : ', self.mac)
        self.started = False
        self.exit = True
        
        #time.sleep(0.5)
        
    
            
    def update(self):
        #try :
        sendTime = time.time()
        frameTime = time.time()
        while True:
            
            if self.started :
                
                (grabbed, frame) = self.capture.read()
                if grabbed : 
                    #print('[-------------- : ', self.Q.qsize())
                    #self.Q.queue.clear()
                    if (self.Q.qsize() > 2) :
                        trash = self.Q.get()
                    self.Q.put(frame)
                    #time.sleep(0.5)
                    #print('[Recv Frame] ', 'URL : ', self.url)

                    if (self.isinference) and ((time.time() - sendTime) > self.inferenceTime):
                        d_now = datetime.datetime.now()
                        save_file = "d:/" + self.mac + "_" + d_now.strftime('%Y%m%d%H%M%S%f') + ".jpg"
                        cv2.imwrite(save_file, frame)
                        

                        if (self.event == 'evt'):
                            datas = {
                                "event" : "evt",
                                "mac" : self.mac
                            }

                            ## Send to Cam Docker 
                            try:
    
                                with open(save_file,'rb') as f:
                                    r = requests.post('https://zenai-cloud.com:5443/event', data=datas, files={"files":f}) #{"files":open(save_file,'rb')}
                                    #print("Send Data (to CAM Docker) : " , datas , " / " , save_file, " result : ", r )
                            except:
                                print("Data Send fail! (to CAM Docker) : " , datas , " / " , save_file )
                        else:
                            datas = {
                                "mac" : self.mac,
                                "date-time" : d_now.strftime('%Y%m%d%H%M%S')
                            }

                            ## Send to Cam Docker 
                            with open(save_file,'rb') as f:
                                r = requests.post('https://zenai-cloud.com:5443/timelapse', data=datas, files={"files":f}) #{"files":open(save_file,'rb')}
                                #print("Send Data (to CAM Docker) : " , datas , " / " , save_file, " result : ", r )
                        
                        
                        sendTime = time.time() # timer reset
                        os.remove(save_file)
                        
                        self.inferenceCount = self.inferenceCount + 1
                        
                        #print("Send Image : ", save_file)
                else:
                    print("------------------  grabbed failed : ", self.mac)
                    
            else:
                if self.capture is not None :
                    #self.capture.release()
                    #self.clear()
                    print('[Streamer Stop] ', 'MAC : ', self.mac)
                    
                
                
            if self.exit:
                if self.capture is not None :
                    self.capture.release()
                    self.clear()
                    #print('[Streamer Stop] ', 'URL : ', self.url)
                    print('[Thread Exit] ', 'MAC : ', self.mac)
                else:
                    print('[Thread Exit----] ', 'MAC : ', self.mac)
                    
                break
        print('[Thread END] ', 'MAC : ', self.mac)
                
        #except GeneratorExit :
            #print('[Thread GeneratorExit] ', 'MAC : ', self.mac)

            
                
    def clear(self):
        
        with self.Q.mutex:
            self.Q.queue.clear()
            
    def read(self):

        return self.Q.get()

    def blank(self):
        
        return np.ones(shape=[self.height, self.width, 3], dtype=np.uint8)
    
    def bytescode(self):
        
        if not self.capture.isOpened():
            
            frame = self.blank()

        else :
            
            frame = imutils.resize(self.read(), width=int(self.width) )
            fps = 'FPS : ' + str(self.fps())
            
            if self.stat :  
                cv2.rectangle( frame, (0,0), (120,30), (0,0,0), -1)
                cv2.putText  ( frame, fps, (10,20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, cv2.LINE_AA)
            
            
        return cv2.imencode('.jpg', frame )[1].tobytes()
    
    def fps(self):
        
        self.current_time = time.time()
        self.sec = self.current_time - self.preview_time
        self.preview_time = self.current_time
        
        if self.sec > 0 :
            fps = round(1/(self.sec),1)
            
            
        else :
            fps = 1
            
        self.fpsValue = round(((self.fpsValue * 9) + fps) / 10,1)
        return fps
    
    def getfps(self):
        return self.fpsValue;
    
    def isOpened(self):
        return self.capture.isOpened()
    
    def isStarted(self):
        return self.started
    
    def setEvent(self, evt):
        self.event = evt
        
    def setInference(self, time):
        if (time == 0.0):
            self.isinference = False
            self.inferenceTime = 0
        else:
            self.isinference = True
            self.inferenceTime = float(time)
            
            
    def getInference(self):
        return self.inferenceTime
    
    def getInferenceCount(self):
        return self.inferenceCount
                   
    def __exit__(self) :
        print( '* streamer class exit')
        self.capture.release()