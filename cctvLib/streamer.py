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
        self.Q = Queue(maxsize=128)
        self.started = False
        self.exit = False
        
    def run(self, src = 0, mac = 0 ) :
        #self.stop()
        self.mac = mac
        self.url = src
        print('[CMD RUN] ', 'MAC : ', self.mac)
        self.started = False
        self.exit = False
        if self.thread is None :
            
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon = False
            self.thread.start()
        
        
    def stop(self):
        print('[CMD Stop] ', 'MAC : ', self.mac)
        self.exit = True
        #self.started = False
        #time.sleep(0.5)
        
    def status_started(self):
        return self.started
            
    def update(self):
        #try :
            while True:
                print('[while] ', 'MAC : ', self.mac, self.started, self.exit)
                if self.started :
                    
                    (grabbed, frame) = self.capture.read()
                    if grabbed : 
                        self.Q.put(frame)
                        #time.sleep(0.5)
                        #print('[Recv Frame] ', 'URL : ', self.url)
                        
                else:
                    if self.capture is not None :
                        self.capture.release()
                        self.clear()
                        print('[Streamer Stop] ', 'MAC : ', self.mac)
                        
                    self.capture = cv2.VideoCapture( self.url )
                    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    self.started = True
                    print('[Streamer Start] ', 'MAC : ', self.mac)
                    
                if self.exit:
                    if self.capture is not None :
                        self.capture.release()
                        self.clear()
                        #print('[Streamer Stop] ', 'URL : ', self.url)
                        print('[Thread Exit] ', 'MAC : ', self.mac)
                    else:
                        print('[Thread Exit----] ', 'MAC : ', self.mac)
                        
                    break
                
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
        
            if self.stat :  
                cv2.rectangle( frame, (0,0), (120,30), (0,0,0), -1)
                fps = 'FPS : ' + str(self.fps())
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
            
        return fps
                   
    def __exit__(self) :
        print( '* streamer class exit')
        self.capture.release()