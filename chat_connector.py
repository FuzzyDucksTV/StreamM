# chat_connector.py
import chat_downloader
from chat_downloader import ChatDownloader
import time
import logging

class ChatConnector:
    """
    This class is responsible for connecting to the live chat of a streaming platform
    using the chat-downloader library. It retrieves chat messages and passes them to
    the main application for further processing.
    """

    def __init__(self, streaming_service: str, streaming_channel: str):
        """
        Initializes the ChatConnector with the streaming service and channel.

        Args:
            streaming_service (str): The streaming service (e.g., "Twitch").
            streaming_channel (str): The streaming channel.
        """
        self.streaming_service = streaming_service
        self.streaming_channel = streaming_channel
        self.chat_downloader = ChatDownloader()
        self.logger = logging.getLogger(__name__)

    def connect_to_chat(self):
        """
        Connects to the live chat and returns a generator that yields chat messages.

        Returns:
            Chat: A chat object that yields chat messages.
        """
        # Construct the URL based on the streaming service and channel
        url = self._construct_url()
        
        chat = self.chat_downloader.get_chat(url)
        return chat

    def _construct_url(self):
        """
        Constructs the URL based on the streaming service and channel.

        Returns:
            str: The URL of the streaming channel.
        """
        #default url is 'https://www.youtube.com/watch?v=jfKfPfyJRdk'
        #TODO add support for other streaming services
        #TODO add code to give the default url if url 
        #is not specified
        if self.streaming_service.lower() == 'youtube' or self.streaming_service.lower() == 'twitch' and self.streaming_channel == 'jfKfPfyJRdk':
            return 'https://www.youtube.com/watch?v=jfKfPfyJRdk'

        if self.streaming_service.lower() == 'twitch':
            return f"https://www.twitch.tv/{self.streaming_channel}"
        elif self.streaming_service.lower() == 'youtube':
            return f"https://www.youtube.com/channel/{self.streaming_channel}"
        else:
            self.logger.error(f"Unsupported streaming service: {self.streaming_service}")
            raise ValueError(f"Unsupported streaming service: {self.streaming_service}")

    def get_message(self):
        """
        Retrieves chat messages.

        Yields:
            dict: A dictionary containing the timestamp, author, and message.
        """
        chat = self.connect_to_chat()
        for message in chat:
            yield {
                'timestamp': message['timestamp'],
                'author': message['author']['name'],
                'message': message['message']
            }

