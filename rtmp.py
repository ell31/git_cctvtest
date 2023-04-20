from flask import Flask, Response, render_template
import cv2
import numpy as np
import pycurl
from io import BytesIO
import threading

app = Flask(__name__)

# RTMP 주소와 RTMP 포트를 설정
rtmp_addr = "rtmp://example.com/live"
rtmp_port = 1935

# 각 CCTV 카메라의 ID와 RTMP URL
cams = [
    {
        "id": 1,
        "url": f"rtmp://210.99.70.120/live/cctv045.stream",
    },
    {
        "id": 2,
        "url": f"rtmp://210.99.70.120/live/cctv046.stream",
    },
    {
        "id": 3,
        "url": f"rtmp://210.99.70.120/live/cctv047.stream",
    },
]

# 카메라별로 영상을 받아오는 함수
def get_stream(cam):
    # RTMP 주소와 카메라 ID를 결합하여 RTMP URL 생성
    cam_addr = f"{cam['url']}"
    while True:
        # PyCURL 객체를 생성하여 RTMP 스트림을 받아옴
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, cam_addr)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        # 받아온 데이터를 바이트 스트림으로 변환
        data = buffer.getvalue()

        # 바이트 스트림을 NumPy 배열로 변환
        nparr = np.frombuffer(data, np.uint8)

        # NumPy 배열을 OpenCV의 이미지 형식으로 변환
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 영상을 출력
        cam['frame'] = frame

# 각 카메라에 대한 스레드 생성
threads = []
for cam in cams:
    thread = threading.Thread(target=get_stream, args=(cam,))
    threads.append(thread)
    thread.start()

# Flask 웹 애플리케이션 라우트
@app.route('/')
def index():
    return render_template('rtmp.html', cams=cams)

# 영상 프레임을 웹으로 출력하는 함수
def gen_frame(cam):
    while True:
        frame = cam['frame']
        cv2.imshow("1111", frame)
        # OpenCV 이미지를 바이트 스트림으로 변환
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# 웹 애플리케이션 라우트
@app.route('/video_feed/<int:cam_id>')
def video_feed(cam_id):
    cam = [cam for cam in cams if cam['id'] == cam_id][0]
    return Response(gen_frame(cam), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)