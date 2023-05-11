   
    
    
# -*- encoding: utf-8 -*-
#-------------------------------------------------#
# Date created          : 2020. 8. 18.
# Date last modified    : 2020. 8. 19.
# Author                : ell31@naver.com
# Site                  : 
# License               : 
# Version               : 0.1.0
# Python Version        : 3.11.0
#       쓰레드를 사용하여 RTSP 통신
#       25개까지 연결 테스트에는 문제 없으나, 이상 연결할 경우 문제 발생함 (30개까지는 영상은 정상 수신 되는것처럼 보임)

#-------------------------------------------------#

from flask import Flask
from flask import request
from flask import Response
from flask import stream_with_context
from flask import render_template, redirect, session, url_for, make_response, jsonify, flash
import cv2
import ssl
import time
import json

from cctvLib.streamer import Streamer

version = '0.1.0'

if cv2.ocl.haveOpenCL() :
       cv2.ocl.setUseOpenCL(True)

app = Flask( __name__ , template_folder='templates')
app.secret_key = '$aiware_web_key$'
#streamer = Streamer()


userData = {}
#temp = {'mac':'000000000001','event':'evt','url':'rtsp://admin:admin@192.168.0.30:554/stream2'}
#userData['000000000001'] = temp
temp = {'mac':'000000000002','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv001.stream'}
userData['000000000002'] = temp
temp = {'mac':'000000000003','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv002.stream'}
userData['000000000003'] = temp
temp = {'mac':'000000000004','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv003.stream'}
userData['000000000004'] = temp
temp = {'mac':'000000000005','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv004.stream'}
userData['000000000005'] = temp
temp = {'mac':'000000000006','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv005.stream'}
userData['000000000006'] = temp
temp = {'mac':'000000000007','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv006.stream'}
userData['000000000007'] = temp
temp = {'mac':'000000000008','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv007.stream'}
userData['000000000008'] = temp
temp = {'mac':'000000000009','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv008.stream'}
userData['000000000009'] = temp

temp = {'mac':'000000000010','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv009.stream'}
userData['000000000010'] = temp
temp = {'mac':'000000000011','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv010.stream'}
userData['000000000011'] = temp
temp = {'mac':'000000000012','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv011.stream'}
userData['000000000012'] = temp
temp = {'mac':'000000000013','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv012.stream'}
userData['000000000013'] = temp
temp = {'mac':'000000000014','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv013.stream'}
userData['000000000014'] = temp
temp = {'mac':'000000000015','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv014.stream'}
userData['000000000015'] = temp
temp = {'mac':'000000000016','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv015.stream'}
userData['000000000016'] = temp
temp = {'mac':'000000000017','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv016.stream'}
userData['000000000017'] = temp
temp = {'mac':'000000000018','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv017.stream'}
userData['000000000018'] = temp
temp = {'mac':'000000000019','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv018.stream'}
userData['000000000019'] = temp
temp = {'mac':'000000000020','event':'timelapse','url':'rtsp://210.99.70.120:1935/live/cctv019.stream'}
userData['000000000020'] = temp

temp = {'mac':'000000000021','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv020.stream'}
userData['000000000021'] = temp
temp = {'mac':'000000000022','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv021.stream'}
userData['000000000022'] = temp
temp = {'mac':'000000000023','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv022.stream'}
userData['000000000023'] = temp
temp = {'mac':'000000000024','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv023.stream'}
userData['000000000024'] = temp
temp = {'mac':'000000000025','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv024.stream'}
userData['000000000025'] = temp
temp = {'mac':'000000000026','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv025.stream'}
userData['000000000026'] = temp
temp = {'mac':'000000000027','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv026.stream'}
userData['000000000027'] = temp
temp = {'mac':'000000000028','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv027.stream'}
userData['000000000028'] = temp
temp = {'mac':'000000000029','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv028.stream'}
userData['000000000029'] = temp
temp = {'mac':'000000000030','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv029.stream'}
userData['000000000030'] = temp




thread_exit = False
camList = dict()



@app.route('/view', methods=['GET','POST'])
def viewer():
    macadd = request.args.get('mac', default = '0', type = str)
    #print("----------------------------------- Viewer mac: ", macadd)
    return render_template('rtsp.html', mac=macadd)

@app.route('/start', methods=['GET','POST'])
def start():
    cctv_Start()
    return "All Camera is started!"


@app.route('/stop', methods=['GET','POST'])
def stop():
    cctv_Stop()
    return "All Camera is stoped!"

@app.route('/AddCam', methods=['GET','POST'])
def AddCam():
    mac = request.form.get('mac', False)
    address = request.form.get('address', False)
    evt = request.form.get('evt', False)

    if mac == "": return "Add fail!"
    if address == "": return "Add fail!"
    
    if mac in userData:
        return "Add fail!" # 맥이 이미 있음
    else:
        temp = {'mac':mac,'event':evt,'url':address}
        userData[mac] = temp
        return "Add Success!"
    #return rtsp_CamListView()
@app.route('/DelCam', methods=['GET','POST'])
def DelCam(): 
    mac = request.form['mac']
    if mac in camList:
        return "First you need to stop the camera !"
    
    if mac in userData:
        del userData[mac]
        return "Delete Success !"
    else:
        return "Delete fail [not MAC] !" #일치하는 맥이 없음

@app.route('/rtsp_CamListView', methods=['GET','POST'])
def rtsp_CamListView():
    #print(userData);
    return render_template('rtsp_CamListView.html', userData=userData)


@app.route('/GetStatus', methods=['GET','POST'])
def GetStatus():

    #mac = request.args.get('mac', default = '0', type = str)
    
    data = {}
    for key, value in userData.items():
        if key in camList:
            dic = {
                'Created': 'Created',
                'isOpened': camList[key].isOpened(),
                'Started': camList[key].isStarted(),
                'inferenctTime': camList[key].getInference(),
                'inferenctCount': camList[key].getInferenceCount()
            }
        else:
            dic = {
                'Created': 'N/A',
                'isOpened': 'N/A',
                'Started': 'N/A',
                'inferenctTime': '0',
                'inferenctCount': '0'
            }
        data[key] = dic
    #print(data);
    return jsonify(data)

@app.route('/StartOne', methods=['GET','POST'])
def StartOne(): 
    mac = request.form['mac']
    cctv_StartOne(mac)  
    return mac + " : Camera is started!"

@app.route('/StopOne', methods=['GET','POST'])
def StopOne(): 
    mac = request.form['mac']
    cctv_StopOne(mac)  
    return mac + " : Camera is stoped!"

@app.route('/setEvent', methods=['GET','POST'])
def setEvent(): 
    #mac = request.args.get('mac', default = '0', type = str)
    mac = request.form['mac']
    event = request.form['event']
    
    userData[mac]['event'] = event
    if mac in camList:
        camList[mac].setEvent(event)
        
    return mac + " : set completed!"

@app.route('/setInferenceTime', methods=['GET','POST'])
def setInferenceTime(): 
    #mac = request.args.get('mac', default = '0', type = str)
    mac = request.form['mac']
    timeValue = request.form['timeValue']
    if (is_float(timeValue)):
        
        if mac in camList:
            camList[mac].setInference(timeValue)
        else:
            return mac + " : First you need to start the camera !"
            
        return mac + " : set completed!"
    else :
        return mac + " : not number!"
    
    
    
@app.route('/getfps', methods=['GET','POST'])
def getfps():
    mac = request.args.get('mac', default = '0', type = str)
    try :
        return Response(whilefps(mac), mimetype='text/event-stream')
    except Exception as e :
        print('[CCTV] ', 'getfps error : ',str(e))
def whilefps(mac):
    
    while True:
        if mac in camList:
            fps = camList[mac].getfps()
            data = {"fps": fps}
            #yield "data: {}\n\n".format(fps) #json.dumps(data)
            yield "data: " + str(camList[mac].getfps()) + "\n\n"
            time.sleep(1)
        

@app.route('/video_feed', methods=['GET','POST'])
def video_feed():
    mac = request.args.get('mac', default = '0', type = str)
    try :
        
        return Response(
            stream_with_context( stream_gen( mac ) ), #stream_with_context-지속적으로 데이타를 전송시킴
            mimetype='multipart/x-mixed-replace; boundary=frame' )
        
    except Exception as e :
        print('[CCTV] ', 'stream error : ',str(e))
        

def cctv_Start():   
    global thread_exit
    thread_exit = False;
    for key, value in userData.items():
        rtsp_url = value['url']
        mac = value['mac']
        event = value['event']
        if mac in camList:
            continue;
        else:
            streamer = Streamer()
            streamer.run( rtsp_url, mac, event )
            camList[mac] = streamer

def cctv_StartOne(mac):
    global thread_exit
    thread_exit = False;

    if mac in userData:
        rtsp_url = userData[mac]['url']
        mac = userData[mac]['mac']
        event = userData[mac]['event']
        if mac in camList:
            return;
        else:
            streamer = Streamer()
            streamer.run( rtsp_url, mac, event )
            camList[mac] = streamer
            
def cctv_StopOne(mac):
    if mac in camList:
        camList[mac].stop()
        del(camList[mac])
        #print("[STOP CAM]  mac : ", mac)
        
def cctv_ViewOne(mac):
    if mac in camList:
        camList[mac].stop()
        del(camList[mac])
        #print("[STOP CAM]  mac : ", mac)
    
                  
def cctv_Stop(): 
    global thread_exit
    thread_exit = True;
    for key, value in userData.items():
        mac = value['mac']
        
        if mac in camList:
            camList[mac].stop()
            del(camList[mac])
            
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
           

def stream_gen( mac ):   

    try : 
        global thread_exit
        '''
        rtsp_url = userData[camNum]['url']
        mac = userData[camNum]['mac']
        
        streamer = Streamer()
        streamer.run( rtsp_url )
        camList[mac] = streamer
        '''
        print("[View Start]  mac : ", mac)
        while True :
            if mac in camList:
                
                #if (camList[mac].status_started() == False):
                #    print("[View Exit]  mac : ", mac)
                #    break;
                if thread_exit:
                    print("[View Exit]  mac : ", mac)
                    break;
                
                frame = camList[mac].bytescode()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break;
            
            
            #if cv2.waitKey(10) & 0xFF == ord('q'):
            #    break
            
    except GeneratorExit :
        #camList[mac].stop()
        #del(camList[mac])
        print("[Streamer Except - View Exit]  mac : ", mac)
        
if __name__ == '__main__' :
    
    print('------------------------------------------------')
    print('CCTV - version ' + version )
    print('------------------------------------------------')
    
    #app.run( host='0.0.0.0', port=5000 )

    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #ssl_context.load_cert_chain(certfile='D:/1.AIWare/3.Project/U.Japen_Docker/1.Program/aiware-docker-web_20230322/zenai-cloud.com/fullchain2.pem',keyfile='D:/1.AIWare/3.Project/U.Japen_Docker/1.Program/aiware-docker-web_20230322/zenai-cloud.com/privkey2.pem')
    app.run(host='0.0.0.0',port=5202,debug=False)# ,ssl_context=ssl_context