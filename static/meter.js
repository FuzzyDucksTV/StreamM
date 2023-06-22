class AnalogMeter {
    constructor(needleElement) {
        this.needleElement = needleElement;
        this.lastUpdate = Date.now();
        this.sentiment_scores = [];  // Initialize sentiment_scores as an empty array
        this.decay_factor = 0.5;
        this.sentimentScoreElement = document.getElementById('sentiment-score');  // New property
        
    }

    update(sentimentScore) {
        // Limit the update rate to 60 FPS
        if (Date.now() - this.lastUpdate < 1000 / 60) {
            return;
        }
        this.lastUpdate = Date.now();

        // Convert the sentiment score to a rotation angle
        // Add the new sentiment score to the list
this.sentiment_scores.push(sentimentScore);

// Only consider the last 10 sentiment scores
let recent_sentiment_scores = this.sentiment_scores.slice(Math.max(this.sentiment_scores.length - 10, 0));

// Apply the decay factor to the weights
let weights = recent_sentiment_scores.map((_, i) => Math.pow(this.decay_factor, i));

// Calculate the weighted average sentiment score
let weighted_average = recent_sentiment_scores.reduce((sum, score, i) => sum + score * weights[i], 0) / weights.reduce((a, b) => a + b, 0);
        const angle = weighted_average * 90;  // Adjust the multiplier as needed

        // Update the needle rotation
        this.needleElement.style.transform = `rotate(${angle}deg)`;
        this.sentimentScoreElement.textContent = `Sentiment Score: ${weighted_average.toFixed(2)}`;  // New line
        
        

    }
}

class LightBarMeter {
    constructor(lightElements) {
        this.lightElements = lightElements;
        this.lastUpdate = Date.now();
    }

    update(sentimentScore) {
        // Limit the update rate to 60 FPS
        if (Date.now() - this.lastUpdate < 1000 / 60) {
            return;
        }
        this.lastUpdate = Date.now();

        // Determine the number of lights to turn on
        const numLights = Math.round(sentimentScore * 5);  // Adjust the multiplier as needed

        // Turn off all lights
        this.lightElements.forEach(light => light.style.background = 'gray');

        // Turn on the appropriate lights
        for (let i = 0; i < numLights; i++) {
            this.lightElements[i].style.background = this.lightElements[i].classList.contains('red') ? 'darkred' : 'darkgreen';
        }
    }
}

// Initialize the sentiment meters
let analogMeter = new AnalogMeter(document.querySelector('.analog-meter .needle'));

// Connect to the server
var socket = io.connect('http://localhost:5000');  // Replace with your server URL

// Listen for sentiment updates
socket.on('sentiment', function(data) {
    try {
        // Update the sentiment meters
        analogMeter.update(data.sentiment);
    } catch (error) {
        console.error('Failed to update sentiment meters:', error);
    }
});

// Function to copy URL
// Function to create URL
// Function to create URL
document.getElementById('create-url-button').addEventListener('click', function() {
    var urlInput = document.getElementById('url-input').value;
    if (urlInput) {
        // Parse the input URL
        var url;
        try {
            url = new URL(urlInput);
        } catch (error) {
            alert('Invalid URL. Please enter a valid YouTube or Twitch URL.');
            return;
        }
        
        var stream, channel;
        
        if (url.hostname === 'www.twitch.tv') {
            stream = 'twitch';
            channel = url.pathname.slice(1);  // Remove the leading '/'
        } else if (url.hostname === 'www.youtube.com') {
            stream = 'youtube';
            channel = url.searchParams.get('v');
            if (!channel) {
                alert('Invalid YouTube URL. The URL should be in the format "https://www.youtube.com/watch?v=<video_id>".');
                return;
            }
        } else {
            alert('Invalid URL. Please enter a valid YouTube or Twitch URL.');
            return;
        }
        
        // Create a new URL based on the parsed data
        var newUrl = 'http://127.0.0.1:5000/meter.html?meter=analogue&channel=' + encodeURIComponent(channel) + '&stream=' + encodeURIComponent(stream);
        document.getElementById('created-url').textContent = newUrl;
        document.getElementById('copy-url-button').style.display = 'block';
    } else {
        alert('Please enter a URL.');
    }
});

// Function to copy URL
document.getElementById('copy-url-button').addEventListener('click', function() {
    var urlText = document.getElementById('created-url').textContent;
    if (urlText) {
        navigator.clipboard.writeText(urlText)
            .then(function() {
                alert('URL copied to clipboard');
            })
            .catch(function(err) {
                alert('Failed to copy URL: ' + err);
            });
    }
});
