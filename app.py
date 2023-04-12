from flask import Flask, render_template


from flask import Flask, Response, render_template, request, redirect, session, url_for, make_response, jsonify, flash
import ssl
import cv2
import time
import requests
import json
import os
import datetime
from threading import Thread
from queue import Queue
from flask import stream_with_context

cv2.setNumThreads(2)

if cv2.ocl.haveOpenCL() :
   cv2.ocl.setUseOpenCL(True)

app = Flask(__name__)
#app = Flask(__name__, template_folder='template')
#app.secret_key = '$aiware_web_key$'

# Replace the IP address and port number with your RTSP server's address and port number
rtsp_url = 'rtsp://admin:admin@192.168.0.30:554/stream2'

#'0030BAFF3161'
userData =[]
temp = {'mac':'000000000001','event':'timelapse','url':'rtsp://admin:admin@192.168.0.30:554/stream2'}
userData.append(temp)
temp = {'mac':'000000000002','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv001.stream'}
userData.append(temp)
'''
temp = {'mac':'000000000003','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv002.stream'}
userData.append(temp)
temp = {'mac':'000000000004','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv003.stream'}
userData.append(temp)
temp = {'mac':'000000000005','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv004.stream'}
userData.append(temp)
temp = {'mac':'000000000006','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv005.stream'}
userData.append(temp)
temp = {'mac':'000000000007','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv006.stream'}
userData.append(temp)
temp = {'mac':'000000000008','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv007.stream'}
userData.append(temp)
temp = {'mac':'000000000009','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv008.stream'}
userData.append(temp)
temp = {'mac':'000000000010','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv009.stream'}
userData.append(temp)
temp = {'mac':'000000000011','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv010.stream'}
userData.append(temp)
temp = {'mac':'000000000012','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv011.stream'}
userData.append(temp)
temp = {'mac':'000000000013','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv012.stream'}
userData.append(temp)
temp = {'mac':'000000000014','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv013.stream'}
userData.append(temp)
temp = {'mac':'000000000015','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv014.stream'}
userData.append(temp)
temp = {'mac':'000000000016','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv015.stream'}
userData.append(temp)
temp = {'mac':'000000000017','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv016.stream'}
userData.append(temp)
temp = {'mac':'000000000018','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv017.stream'}
userData.append(temp)
temp = {'mac':'000000000019','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv018.stream'}
userData.append(temp)
temp = {'mac':'000000000020','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv019.stream'}
userData.append(temp)
temp = {'mac':'000000000021','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv020.stream'}
userData.append(temp)
temp = {'mac':'000000000022','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv021.stream'}
userData.append(temp)
temp = {'mac':'000000000023','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv022.stream'}
userData.append(temp)
temp = {'mac':'000000000024','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv023.stream'}
userData.append(temp)
temp = {'mac':'000000000025','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv024.stream'}
userData.append(temp)
temp = {'mac':'000000000026','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv025.stream'}
userData.append(temp)
temp = {'mac':'000000000027','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv026.stream'}
userData.append(temp)
temp = {'mac':'000000000028','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv027.stream'}
userData.append(temp)
temp = {'mac':'000000000029','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv028.stream'}
userData.append(temp)
temp = {'mac':'000000000030','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv029.stream'}
userData.append(temp)
'''
#rtsp://210.99.70.120:1935/live/cctv002.stream
#rtsp://210.99.70.120:1935/live/cctv003.stream
#rtsp://210.99.70.120:1935/live/cctv004.stream
#rtsp://210.99.70.120:1935/live/cctv005.stream
#rtsp://210.99.70.120:1935/live/cctv006.stream

videos = []
for data in userData:
    print('CCTV Connected ---------------', data["url"])
    video = cv2.VideoCapture(data["url"])
    videos.append(video)


def gen_frames(CamNum):
    
    rtsp_url = userData[CamNum]['url']
    mac = userData[CamNum]['mac']
    event = userData[CamNum]['event']
    #cap = cv2.VideoCapture(rtsp_url)
    print('Viewer Connected ---------------', rtsp_url, " : ", mac)
    
    
    cap = videos[CamNum]
    
    # 원본 동영상 크기 정보
    capw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    caph = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("         원본 동영상 너비(가로) : {}, 높이(세로) : {}".format(capw, caph),"   ", cap.get(cv2.CAP_PROP_FPS))

    # 동영상 크기 변환
    wRatio = 640
    hRatio = 480
    hRatio = 640 / capw * caph
    print("        ",hRatio)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, wRatio) # 가로
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(hRatio)) # 세로
    r1 = cap.set(cv2.CAP_PROP_FRAME_WIDTH, wRatio) # 가로
    r2 = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(hRatio)) # 세로
    print("        ",r1,"    ",r2)

    # 변환된 동영상 크기 정보
    capw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    caph = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("         변환된 동영상 너비(가로) : {}, 높이(세로) : {}".format(capw, caph))

    
    sendTime = time.time()
    frameTime = time.time()
    
    while True:
        success, frame = cap.read()
        time.sleep(0.1)
        if not success:
            print("---- break ", CamNum)
            # Check if the camera is opened successfully
            time.sleep(3)
            cap = cv2.VideoCapture(rtsp_url)
            #break
        else:
            
            
            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            framebyte = buffer.tobytes()
            
            # Use yield instead of return to send the frame to the web page
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + framebyte + b'\r\n')
           
            #fps 값 입력
            sec = time.time() - frameTime
            frameTime = time.time()
            fps = 1/(sec)
            str = "FPS : %0.1f" % fps
            cv2.putText(frame, str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
            '''
            if (time.time() - sendTime) > 10.0:
                d_now = datetime.datetime.now()
                save_file = "d:/" + mac + "_" + d_now.strftime('%Y%m%d%H%M%S%f') + ".jpg"
                cv2.imwrite(save_file, frame)
                
                
                if (event == 'evt'):
                    datas = {
                        "event" : "evt",
                        "mac" : mac
                    }
                    ## Send to Cam Docker 
                    with open(save_file,'rb') as f:
                        r = requests.post('https://zenai-cloud.com:5443/event', data=datas, files={"files":f}) #{"files":open(save_file,'rb')}
                        print("Send Data (to CAM Docker) : " , datas , " / " , save_file, " result : ", r )
                else:
                    datas = {
                        "mac" : mac,
                        "date-time" : d_now.strftime('%Y%m%d%H%M%S')
                    }
                    ## Send to Cam Docker 
                    with open(save_file,'rb') as f:
                        r = requests.post('https://zenai-cloud.com:5443/timelapse', data=datas, files={"files":f}) #{"files":open(save_file,'rb')}
                        print("Send Data (to CAM Docker) : " , datas , " / " , save_file, " result : ", r )
                
                
                
                sendTime = time.time() # timer reset
                os.remove(save_file)
                
                #print("Send Image : ", save_file)
            '''
            
            
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    
    
@app.route('/')
def index():
    return render_template('cctv_rtsp.html')

@app.route('/video_feed', methods=['GET','POST'])
def video_feed():
    # Use Response to create a streaming response with MIME type multipart/x-mixed-replace
    camNum = request.args.get('camNum', default = '0', type = int)
    #print("----------------------------------- CMD : ", camNum)
    
    #thread = Thread(target=gen_frames, args=(camNum))
    #thread.daemon = False
    #thread.start()

    return Response(stream_with_context(gen_frames(camNum)), mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route("/")
def index():
    return render_template('./index.html')
