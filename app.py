from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return "StreamMatey Server is running..."

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def send_random_sentiment():
    while True:
        socketio.sleep(1)
        sentiment = random.uniform(-1, 1)  # Generate a random sentiment score between -1 and 1
        socketio.emit('sentiment', {'sentiment': sentiment})

if __name__ == '__main__':
    socketio.start_background_task(send_random_sentiment)
    socketio.run(app, debug=True)
