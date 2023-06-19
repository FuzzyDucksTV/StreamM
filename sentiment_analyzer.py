import logging
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from database import Database

# Download the vader_lexicon
nltk.download('vader_lexicon', quiet=True)

class SentimentAnalyzer:
    def __init__(self, database: Database):
        """
        Initialize the SentimentAnalyzer with a database instance.
        
        :param database: An instance of the Database class.
        """
        self._database = database
        self._sid = SentimentIntensityAnalyzer()
        self._logger = logging.getLogger(__name__)

    def analyze_sentiment(self, chat_message: str, message_user: str, message_timestamp: str) -> float:
        """
        Analyze the sentiment of a chat message and store it in the database.
        
        :param chat_message: The chat message to analyze.
        :param message_user: The user who sent the message.
        :param message_timestamp: The timestamp of the message.
        :return: The sentiment score of the message.
        """
        try:
            # Handle edge case of empty message
            if not chat_message.strip():
                return 0.0
            
            # Check if the message already exists in the database
            existing_message = self._database.get_comment(chat_message)
            if existing_message is not None:
                return existing_message[2]  # Return the existing sentiment score
            
            # Calculate sentiment score
            sentiment_score = self._sid.polarity_scores(chat_message)['compound']
            
            # Store in database only if the sentiment score is not equal to 0.0
            if sentiment_score != 0.0:
                self._database.insert_comment(chat_message, sentiment_score, message_user, message_timestamp)
            
            return sentiment_score
        except Exception as e:
            # Log error and return neutral sentiment score
            self._logger.error(f"An error occurred while analyzing sentiment: {e}")
            return 0.0
