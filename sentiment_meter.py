import logging
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path

class SentimentMeter:
    """
    This class is responsible for displaying a meter that changes as each message is given a sentiment score.
    """
    def __init__(self):
        """
        Initializes the SentimentMeter.
        """
        self.logger = logging.getLogger(__name__)
        self.sentiment_scores = []
        self.decay_factor = 0.9

        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(-180, 0)
        self.ax.set_xlim(-1, 1)
        self.ax.set_axis_off()
        self.ax.set_title("")
        self.create_meter(0.0)

        # Initialize the FuncAnimation object
    

    def update(self, sentiment_score):
        """
        Updates the sentiment meter based on the sentiment score of a message.

        Args:
            sentiment_score (float): The sentiment score of a message.

        Raises:
            TypeError: If sentiment_score is not a float.
            ValueError: If sentiment_score is not between -1 and 1.
        """
        if not isinstance(sentiment_score, float):
            raise TypeError("Sentiment score must be a float.")
        if not -1 <= sentiment_score <= 1:
            raise ValueError("Sentiment score must be between -1 and 1.")

        # Add the new sentiment score to the list
        self.sentiment_scores.append(sentiment_score)

        # Only consider the last 10 sentiment scores
        recent_sentiment_scores = self.sentiment_scores[-10:]

        # Apply the decay factor to the weights
        weights = [self.decay_factor ** i for i in range(len(recent_sentiment_scores))]

        # Calculate the weighted average sentiment score
        weighted_average = sum(x * w for x, w in zip(recent_sentiment_scores, weights)) / sum(weights)

        self.ax.clear()
        artists = self.create_meter(weighted_average)
        plt.draw()
        plt.pause(0.03)
        return artists

    def create_meter(self, sentiment_score):
        """
        Creates a graphical representation of the sentiment meter.

        Args:
        sentiment_score (float): The sentiment score to display on the meter.
        """
        if not isinstance(sentiment_score, float):
            raise TypeError("Sentiment score must be a float.")
        if not -1 <= sentiment_score <= 1:
            raise ValueError("Sentiment score must be between -1 and 1.")

        # Define properties of the meter
        theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
        radii = np.linspace(0, 1, 100)
        artists = []
        for radius in radii:
            x = radius * np.sin(theta)
            y = -radius * np.cos(theta) - 90
            line, = self.ax.plot(x, y, color='black', linewidth=2)
            artists.append(line)
        x = np.linspace(-1, 1, 100)
        y = np.zeros(100)
        line, = self.ax.plot(x, y, color='black', linewidth=2)
        artists.append(line)
        # Calculate the angle based on the sentiment score
        # Map the sentiment score from -1 to 1 to the angle from -90 to 90
        
        angle = ((sentiment_score / 0.25) * 90)
        # Calculate the coordinates of the needle
        x = [0, 0.3 * np.sin(np.radians(angle))]
        y = [0, -90 + 0.3 * np.cos(np.radians(angle))]
        line, = self.ax.plot(x, y, color='red', linewidth=2)
        artists.append(line)
        plt.draw()
        plt.pause(0.13)


        