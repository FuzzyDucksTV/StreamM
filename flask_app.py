import random
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, disconnect
import sqlite3
from sentiment_analyzer import SentimentAnalyzer
from sentiment_meter import SentimentMeter
from database import Database
from chat_connector import ChatConnector
import threading
import re

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class InvalidParametersError(Exception):
    """
    Custom exception class for invalid parameters.
    """
    pass

@app.errorhandler(InvalidParametersError)
def handle_invalid_parameters_error(error):
    """
    Error handler for InvalidParametersError.
    """
    response = jsonify({'error': 'Invalid parameters'})
    response.status_code = 400
    return response

@app.route('/')
def home():
    """
    Render the home page.
    """
    return render_template('index.html')

@app.route('/index.html', methods=['POST'])
def generate():
    """
    Generate the URL for the sentiment meter based on the user's input.
    """
    url = request.form.get('url')

    # Validate the URL
    if not re.match(r'https?://(www\.)?(youtube\.com/watch\?v=|twitch\.tv/)[^\s]+', url):
        raise InvalidParametersError

    # Start the chat connector and sentiment analyzer using the classes in the chat_connector.py and sentiment_analyzer.py.
    # Note we will have to change the existing code in sentiment_analyzer.py to make writing to the database optional (especially in development as we have finite resources).

    # Return the generated URL for the meter
    return jsonify({'meter_url': f'{request.base_url}?stream=youtube&channel={url.split("=")[-1]}&meter=analogue'})

@app.route('/index.html', methods=['GET'])
def sentiment_meter():
    """
    Render the sentiment meter page based on the parameters in the URL.
    """
    stream = request.args.get('stream')
    channel = request.args.get('channel')
    meter = request.args.get('meter')

    if meter == None or channel == None or stream == None:
        return render_template('index.html')

    # Validate the parameters
    if (stream not in ['youtube', 'twitch'] or not channel or meter not in ['analogue', 'digital']):
        raise InvalidParametersError

    # Render the meter page
    return render_template('meter.html', stream=stream, channel=channel, meter=meter)
class ChatConnectionError(Exception):
    """
    Custom exception class for chat connection errors.
    """
    pass

@app.errorhandler(ChatConnectionError)
def handle_chat_connection_error(error):
    """
    Error handler for ChatConnectionError.
    """
    response = jsonify({'error': 'Failed to connect to the chat'})
    response.status_code = 500
    return response

@app.route('/index.html', methods=['POST'])
def generate_index():
    """
    Generate the URL for the sentiment meter based on the user's input.
    """
    url = request.form.get('url')

    # Validate the URL
    if not re.match(r'https?://(www\.)?(youtube\.com/watch\?v=|twitch\.tv/)[^\s]+', url):
        raise InvalidParametersError

    # Start the chat connector and sentiment analyzer
    try:
        chat_connector = ChatConnector(url)
        sentiment_analyzer = SentimentAnalyzer()
        threading.Thread(target=start_stream, args=(chat_connector, sentiment_analyzer)).start()
    except Exception as e:
        raise ChatConnectionError from e

    # Return the generated URL for the meter
    return jsonify({'meter_url': f'{request.base_url}?stream=youtube&channel={url.split("=")[-1]}&meter=analogue'})

def start_stream(chat_connector, sentiment_analyzer):
    """
    Connect to the chat and analyze the sentiment of the chat messages.
    """
    try:
        # Connect to the chat
        chat_connector.connect()

        # Continuously analyze the chat sentiment
        while True:
            message = chat_connector.get_message()
            sentiment_score = sentiment_analyzer.analyze_sentiment(message)
            socketio.emit('sentiment_score', {'score': sentiment_score})
    except Exception as e:
        # Log the error and disconnect the socket
        app.logger.error(f"An error occurred: {e}")
        disconnect()

def send_random_sentiment():
    while True:
        socketio.sleep(1)
        sentiment = random.uniform(-1, 1)  # Generate a random sentiment score between -1 and 1
        socketio.emit('sentiment', {'sentiment': sentiment})


if __name__ == '__main__':
    try:
        socketio.run(app)
    except Exception as e:
        # Log the error and exit the application
        app.logger.error(f"An error occurred: {e}")
        exit(1)
