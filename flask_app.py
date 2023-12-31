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
import logger

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', async_handlers=True,allow_unsafe_requests=True, debug=True)

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

@app.route('/index.html', methods=['GET'])
def sentiment_meter():
    """
    Render the sentiment meter page based on the parameters in the URL.
    """
    stream = request.args.get('stream')
    channel = request.args.get('channel')
    meter = request.args.get('meter')

    if meter == None or channel == None or stream == None:
        try:
            url = "jfKfPfyJRdk"
            chat_connector = ChatConnector("youtube",url)
            sentiment_analyzer = SentimentAnalyzer("none")
            threading.Thread(target=start_stream, args=(chat_connector, sentiment_analyzer)).start()
            return render_template('index.html')
        except Exception as e:
            raise ChatConnectionError from e
    else:
        try:
            chat_connector = ChatConnector(stream, channel)
            sentiment_analyzer = SentimentAnalyzer(meter)
            threading.Thread(target=start_stream, args=(chat_connector, sentiment_analyzer)).start()
            return render_template('meter.html')
        except Exception as e:
            raise ChatConnectionError from e
            

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
    while True:
        try:
            # Get a chat message
            for message in chat_connector.get_message():
                timestamp = message['timestamp']
                author = message['author']
                text = message['message']
                sentiment_score = sentiment_analyzer.analyze_sentiment(text, author, timestamp)
                # Update the sentiment meter with the sentiment score
                #sentiment_meter.update(sentiment_score) #TODO: Update the sentiment meter on the javascript page using the SentimentMeter class. 
                # SentimentMeter Class that will display a javascript driven meter that still needs to be written in the Flask application code.
                socketio.emit('sentiment', {'sentiment': sentiment_score})
  
        except Exception as e:
            logger.log_message(f"An error occurred: {e}")
            continue
        except KeyboardInterrupt:
            logger.log_message("Stopping application...")
            break


if __name__ == '__main__':
    try:
        socketio.run(app)
    except Exception as e:
        # Log the error and exit the application
        app.logger.log_message(f"An error occurred: {e}")
        exit(1)
