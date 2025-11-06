import requests
from flask import Flask, request, jsonify, render_template_string
import speech_recognition as sr
import pyttsx3
import threading
import time
import signal
import sys
from dataclasses import dataclass
from typing import Optional

# Flask Configuration
app = Flask(__name__)

# Weather API Configuration
API_KEY = ""  # Replace with your key
CITY = "Lyon"  # Default city


# Data structure for weather information
@dataclass
class WeatherInfo:
    city: str
    temperature: float  # in Celsius
    humidity: int  # in percentage
    wind_speed: float  # in km/h
    description: str
    pressure: Optional[int] = None  # in hPa
    precipitation: Optional[float] = None  # in mm

    def __str__(self):
        return (
            f"Weather in {self.city}: {self.description}\n"
            f"Temperature: {self.temperature}°C\n"
            f"Humidity: {self.humidity}%\n"
            f"Wind: {self.wind_speed} km/h\n"
            f"Pressure: {self.pressure} hPa\n"
            f"Precipitation: {self.precipitation} mm"
        )


# Global variables
current_weather = None
listening_active = False
voice_response = ""


# Function to get weather data from API
def get_weather_data(city=CITY):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=en"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            print(f"API Error: {data['error']['message']}")
            return None

        # Extract relevant data
        current = data["current"]
        weather_info = WeatherInfo(
            city=city,
            temperature=current["temp_c"],
            humidity=current["humidity"],
            wind_speed=current["wind_kph"],
            description=current["condition"]["text"],
            pressure=current["pressure_mb"],
            precipitation=current["precip_mm"],
        )

        return weather_info
    except Exception as e:
        print(f"Error while retrieving weather data: {e}")
        return None


# Functions for audio input and output
def speak_text(text: str):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # Use first voice (usually English)

    engine.say(text)
    engine.runAndWait()


def record_audio():
    global voice_response

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\n Listening... Speak now!")
            speak_text("I'm listening. What would you like to know about the weather?")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)

        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print(f'🔊 You said: "{text}"')

            # Process the text and generate response
            response = generate_weather_response(text)
            print(f" Response: {response}")
            speak_text(response)

            # Update the global variable with the response
            voice_response = f'You asked: "{text}"\nResponse: {response}'
            return text

        except sr.UnknownValueError:
            voice_response = "I couldn't understand what you said. Please try again."
            print("❓ I didn't understand that.")
            speak_text("I didn't catch that. Please try again.")
            return None

        except sr.RequestError:
            voice_response = "There was an error with the speech recognition service."
            print(" Error with the speech recognition service.")
            speak_text("There was an error with the speech recognition service.")
            return None

    except Exception as e:
        voice_response = f"Error: {str(e)}"
        print(f"Error during voice recognition: {e}")
        return None


# Periodic weather data updates
def update_weather_periodically():
    global current_weather
    while True:
        current_weather = get_weather_data()
        print(" Weather data updated!")
        time.sleep(600)  # Update every 10 minutes


# Function to generate a simple response based on weather data
def generate_weather_response(query):
    global current_weather

    if not current_weather:
        return "Sorry, I couldn't get the current weather data."

    # Simple query analysis
    query = query.lower()

    if "temperature" in query or "hot" in query or "cold" in query:
        return f"The temperature in {current_weather.city} is {current_weather.temperature}°C."

    elif "humid" in query:
        return f"The humidity level is currently {current_weather.humidity}%."

    elif "wind" in query:
        return f"The wind speed is {current_weather.wind_speed} kilometers per hour."

    elif "rain" in query or "precipitation" in query:
        if current_weather.precipitation > 0:
            return f"There is currently {current_weather.precipitation} mm of precipitation."
        else:
            return "There is no precipitation at the moment."

    elif "wear" in query or "clothes" in query or "dress" in query:
        response = "For today, "

        if current_weather.temperature < 5:
            response += "it's very cold. I recommend wearing a thick coat, scarf, gloves, and a hat."
        elif current_weather.temperature < 12:
            response += (
                "it's cool. I recommend wearing a light coat or jacket and a sweater."
            )
        elif current_weather.temperature < 20:
            response += "the temperature is pleasant. A sweater or light jacket should be enough."
        elif current_weather.temperature < 25:
            response += (
                "it's nice. A t-shirt and possibly a light layer for the evening."
            )
        else:
            response += "it's hot. Light clothing is recommended, and don't forget sun protection!"

        if current_weather.precipitation > 0:
            response += " Don't forget your umbrella, there's precipitation!"

        return response

    else:
        # Default response with weather summary
        return f"In {current_weather.city}, it's currently {current_weather.temperature}°C with {current_weather.description}. The humidity is {current_weather.humidity}% and the wind is blowing at {current_weather.wind_speed} km/h."


# Voice assistant function that will be triggered from the web
def start_voice_recognition():
    global listening_active, voice_response

    if listening_active:
        return "Voice assistant is already listening. Please wait."

    listening_active = True
    try:
        record_audio()
    finally:
        listening_active = False

    return voice_response


# Setup signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("\n You pressed Ctrl+C! Exiting gracefully...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# HTML Template for web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Application</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f8ff;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #4682b4;
            text-align: center;
        }
        .weather-info {
            margin-top: 20px;
        }
        .info-item {
            margin: 10px 0;
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 5px;
        }
        .main-info {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .temperature {
            font-size: 36px;
            font-weight: bold;
        }
        .description {
            font-size: 18px;
            color: #4682b4;
        }
        .button-container {
            text-align: center;
            margin: 30px 0;
        }
        .voice-btn {
            background-color: #4682b4;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            display: inline-flex;
            align-items: center;
            transition: all 0.3s;
        }
        .voice-btn:hover {
            background-color: #36648b;
            transform: scale(1.05);
        }
        .voice-btn:active {
            transform: scale(0.95);
        }
        .voice-btn .mic-icon {
            margin-right: 10px;
            font-size: 20px;
        }
        .refresh-btn {
            background-color: #4682b4;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .refresh-btn:hover {
            background-color: #36648b;
        }
        .response-area {
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 5px;
            border: 1px solid #ddd;
            min-height: 100px;
            white-space: pre-line;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 10px 0;
        }
        .loading-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            background-color: #4682b4;
            border-radius: 50%;
            margin: 0 5px;
            animation: pulse 1.5s infinite ease-in-out;
        }
        .loading-dot:nth-child(2) {
            animation-delay: 0.3s;
        }
        .loading-dot:nth-child(3) {
            animation-delay: 0.6s;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.2); opacity: 1; }
        }
        .assistant-info {
            margin-top: 30px;
            padding: 15px;
            background-color: #fffaf0;
            border-radius: 5px;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background-color: #28a745;
            border-radius: 50%;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Real-time Weather</h1>
        
        <!-- Weather Information Section -->
        <div class="weather-info">
            <div class="main-info">
                <div>
                    <div class="temperature">{{ weather.temperature }}°C</div>
                    <div class="description">{{ weather.description }}</div>
                </div>
                <button class="refresh-btn" onclick="location.reload()">Refresh</button>
            </div>
            
            <div class="info-item">
                <strong>City:</strong> {{ weather.city }}
            </div>
            <div class="info-item">
                <strong>Humidity:</strong> {{ weather.humidity }}%
            </div>
            <div class="info-item">
                <strong>Wind speed:</strong> {{ weather.wind_speed }} km/h
            </div>
            <div class="info-item">
                <strong>Pressure:</strong> {{ weather.pressure }} hPa
            </div>
            <div class="info-item">
                <strong>Precipitation:</strong> {{ weather.precipitation }} mm
            </div>
        </div>
        
        <!-- Voice Assistant Section -->
        <div class="button-container">
            <button id="voiceButton" class="voice-btn" onclick="startVoiceRecognition()">
                <span class="mic-icon">🎤</span> Ask about weather
            </button>
        </div>
        
        <div id="loading" class="loading">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
        
        <div class="response-area" id="responseArea">
            Your voice assistant responses will appear here...
        </div>
        
        <div class="assistant-info">
            <h3><span class="status-indicator"></span> Voice Assistant</h3>
            <p>Click the "Ask about weather" button above to activate the voice assistant. You can ask questions like:</p>
            <ul>
                <li>What's the temperature today?</li>
                <li>Is it going to rain?</li>
                <li>How's the humidity?</li>
                <li>What should I wear today?</li>
                <li>How strong is the wind?</li>
            </ul>
        </div>
    </div>
    
    <script>
        // Auto refresh every 10 minutes
        setTimeout(function() {
            location.reload();
        }, 600000);
        
        // Voice recognition function
        function startVoiceRecognition() {
            const button = document.getElementById('voiceButton');
            const loading = document.getElementById('loading');
            const responseArea = document.getElementById('responseArea');
            
            // Disable button and show loading
            button.disabled = true;
            button.innerHTML = '<span class="mic-icon">🎤</span> Listening...';
            button.style.backgroundColor = '#8B0000';
            loading.style.display = 'block';
            responseArea.innerText = "Listening... Please speak now.";
            
            // Call the API endpoint to start recognition
            fetch('/api/voice-recognition')
                .then(response => response.text())
                .then(data => {
                    responseArea.innerText = data;
                })
                .catch(error => {
                    responseArea.innerText = "Error: " + error;
                })
                .finally(() => {
                    // Re-enable button and hide loading
                    button.disabled = false;
                    button.innerHTML = '<span class="mic-icon">🎤</span> Ask about weather';
                    button.style.backgroundColor = '#4682b4';
                    loading.style.display = 'none';
                });
        }
    </script>
</body>
</html>
"""


# Routes for web application
@app.route("/")
def home():
    global current_weather
    if not current_weather:
        current_weather = get_weather_data()

    return render_template_string(HTML_TEMPLATE, weather=current_weather)


@app.route("/api/weather", methods=["GET"])
def api_weather():
    global current_weather
    if not current_weather:
        current_weather = get_weather_data()

    return jsonify(
        {
            "city": current_weather.city,
            "temperature": current_weather.temperature,
            "humidity": current_weather.humidity,
            "wind_speed": current_weather.wind_speed,
            "description": current_weather.description,
            "pressure": current_weather.pressure,
            "precipitation": current_weather.precipitation,
        }
    )


@app.route("/api/voice-recognition", methods=["GET"])
def api_voice_recognition():
    return start_voice_recognition()


# Main entry point
if __name__ == "__main__":
    # Print welcome banner
    print("\n" + "=" * 50)
    print("🌤️  WEATHER CLEAR")
    print("=" * 50)

    # Initialize weather data
    print("\n🔄 Initializing weather data...")
    current_weather = get_weather_data()

    if current_weather:
        print(f" Current weather loaded for {current_weather.city}")
    else:
        print("  Could not load initial weather data. Will retry later.")

    # Start periodic weather updates in a separate thread
    weather_thread = threading.Thread(target=update_weather_periodically, daemon=True)
    weather_thread.start()

    # Start web application
    print("\n🌐 Web server started at http://localhost:5000")
    print("🔊 Voice assistant is ready")
    print("📝 Use the web interface to interact with the voice assistant")
    print("⛔ Press Ctrl+C to exit the application")
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
