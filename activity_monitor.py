"""
The `activity_monitor.py` script is part of the StreamMatey OBS Plugin software. It provides an `ActivityMonitor` class for tracking chat activity and a `Bot` class for interacting with Twitch chat.

The `ActivityMonitor` class is responsible for monitoring the rate of chat messages. It uses a deque to store the timestamps of the most recent messages within a specified window size.

The `ActivityMonitor` class has two methods:

- `add_message(message)`: Adds the timestamp of a new message to the deque.
- `get_activity_level()`: Calculates and returns the current activity level, defined as the number of messages per second.

The `Bot` class is a subclass of `commands.Bot` from the `twitchio.ext` module. It extends the base class with an `activity_monitor` attribute and overrides the `event_message` method to add each incoming message to the activity monitor.

The `Bot` class also includes a command for checking the current activity level. The `activity_command` method responds to the "!activity" command by printing the current activity level.

In the main part of the script, an `ActivityMonitor` instance and a `Bot` instance are created. The `ActivityMonitor` instance is set to monitor a 1-minute window of activity. The `Bot` instance is initialized with the necessary Twitch credentials and the `ActivityMonitor` instance, and is set to join two channels.

Finally, the bot is run with the `run` method. This starts the bot and begins monitoring chat activity.
"""
