class AnalogMeter {
    constructor(needleElement) {
        this.needleElement = needleElement;
        this.lastUpdate = Date.now();
    }

    update(sentimentScore) {
        // Limit the update rate to 60 FPS
        if (Date.now() - this.lastUpdate < 1000 / 60) {
            return;
        }
        this.lastUpdate = Date.now();

        // Convert the sentiment score to a rotation angle
        const angle = sentimentScore * 90;  // Adjust the multiplier as needed

        // Update the needle rotation
        this.needleElement.style.transform = `rotate(${angle}deg)`;
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
let lightBarMeter = new LightBarMeter(Array.from(document.querySelectorAll('.light-bar-meter .light')));

// Connect to the server
var socket = io.connect('http://localhost:5000');  // Replace with your server URL

// Listen for sentiment updates
socket.on('sentiment', function(data) {
    try {
        // Update the sentiment meters
        analogMeter.update(data.sentiment);
        lightBarMeter.update(data.sentiment);
    } catch (error) {
        console.error('Failed to update sentiment meters:', error);
    }
});
