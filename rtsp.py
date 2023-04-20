   
    
    
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

from flask import Flask
from flask import request
from flask import Response
from flask import stream_with_context
from flask import render_template, redirect, session, url_for, make_response, jsonify, flash
import cv2
import ssl
import time

from cctvLib.streamer import Streamer

version = '0.1.0'

if cv2.ocl.haveOpenCL() :
       cv2.ocl.setUseOpenCL(True)

app = Flask( __name__ , template_folder='templates')
app.secret_key = '$aiware_web_key$'
#streamer = Streamer()


userData =[]
temp = {'mac':'000000000001','event':'evt','url':'rtsp://admin:admin@192.168.0.30:554/stream2'}
userData.append(temp)
temp = {'mac':'000000000002','event':'evt','url':'rtsp://210.99.70.120:1935/live/cctv001.stream'}
userData.append(temp)
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
'''
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


thread_exit = False
camList = dict()

def cctv_Start():   
    global thread_exit
    thread_exit = False;
    for ud in userData:
        rtsp_url = ud['url']
        mac = ud['mac']
        if mac in camList:
            continue;
        else:
            streamer = Streamer()
            streamer.run( rtsp_url, mac )
            camList[mac] = streamer
def cctv_Stop(): 
    global thread_exit
    thread_exit = True;
    for ud in userData:
        rtsp_url = ud['url']
        mac = ud['mac']
        
        if mac in camList:
            camList[mac].stop()
            del(camList[mac])
            print("----------------------------------- cctv Stop: ", mac)

@app.route('/view', methods=['GET','POST'])
def viewer():
    macadd = request.args.get('mac', default = '0', type = str)
    print("----------------------------------- Viewer mac: ", macadd)
    return render_template('TEST_Rtsp3.html', mac=macadd)

@app.route('/start')
def start():

    cctv_Start()
    return "start Complete"

@app.route('/stop')
def stop():

    
    cctv_Stop()
    return "stop Complete"


@app.route('/video_feed', methods=['GET','POST'])
def video_feed():
    
    #src = request.args.get( 'src', default = 0, type = int )
    #src = 'rtsp://admin:admin@192.168.0.30:554/stream2'
    #camNum = request.args.get('camNum', default = '0', type = int)
    mac = request.args.get('mac', default = '0', type = str)
    print("----------------------------------- CMD View Mac: ", mac)

    try :
        
        return Response(
                                stream_with_context( stream_gen( mac ) ), #stream_with_context-지속적으로 데이타를 전송시킴
                                mimetype='multipart/x-mixed-replace; boundary=frame' )
        
    except Exception as e :
        print('[CCTV] ', 'stream error : ',str(e))
        


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
            #if (camList[mac].status_started() == False):
            #    print("[View Exit]  mac : ", mac)
            #    break;
            if thread_exit:
                print("[View Exit]  mac : ", mac)
                break;
            
            frame = camList[mac].bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            
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

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='D:/1.AIWare/3.Project/U.Japen_Docker/1.Program/aiware-docker-web_20230322/zenai-cloud.com/fullchain2.pem',keyfile='D:/1.AIWare/3.Project/U.Japen_Docker/1.Program/aiware-docker-web_20230322/zenai-cloud.com/privkey2.pem')
    app.run(host='0.0.0.0',port=5202,ssl_context=ssl_context)# ,debug=True