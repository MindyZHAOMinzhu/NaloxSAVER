from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import secrets
from camera import generate_frames

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(24)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/narcan_video')
def narcan_video():
    return render_template('preloaded_video.html')

@socketio.on('connect', namespace='/')
def test_connect():
    print('Client connected')

@socketio.on('test_client_to_server')
def handle_test_event(data):
    print('Client says:', data['message'])
    socketio.emit('test_server_to_client', {'message': 'Hello from server'})
    
def get_socketio():
    return socketio

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
