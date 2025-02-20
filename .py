import os
import time
import threading
import speech_recognition as sr
from flask import Flask, request
from picarx import PicarX  # Using SunFounder PiCar-X package

px = PicarX()

app = Flask(__name__)

# Function to control the movement of the car
def move_car(direction):
    if direction == "forward":
        px.forward(30)
    elif direction == "backward":
        px.backward(30)
    elif direction == "left":
        px.set_dir_servo_angle(-30)
        px.forward(30)
    elif direction == "right":
        px.set_dir_servo_angle(30)
        px.forward(30)
    elif direction == "stop":
        px.stop()
    time.sleep(1)
    px.stop()

# Web interface for controlling the car
@app.route('/')
def home():
    return '''
    <h1>PiCar Web Control</h1>
    <button onclick="fetch('/move?dir=forward')">Forward</button>
    <button onclick="fetch('/move?dir=backward')">Backward</button>
    <button onclick="fetch('/move?dir=left')">Left</button>
    <button onclick="fetch('/move?dir=right')">Right</button>
    <button onclick="fetch('/move?dir=stop')">Stop</button>
    '''

# Endpoint for moving the car
@app.route('/move')
def move():
    direction = request.args.get('dir')
    move_car(direction)
    return f"Car moved {direction}"

# Function to listen to voice commands using speech recognition
def listen_to_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Listening for voice commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized command: {command}")
            if "forward" in command:
                move_car("forward")
            elif "backward" in command:
                move_car("backward")
            elif "left" in command:
                move_car("left")
            elif "right" in command:
                move_car("right")
            elif "stop" in command:
                move_car("stop")
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError:
            print("Speech recognition service error")

# Function for obstacle avoidance
def obstacle_avoidance():
    while True:
        distance = px.get_distance()
        if distance < 20:
            print("Obstacle detected! Stopping.")
            px.stop()
        time.sleep(0.1)

# Function to run the Flask app
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    # Create separate threads for Flask, voice recognition, and obstacle avoidance
    flask_thread = threading.Thread(target=run_flask)
    voice_thread = threading.Thread(target=listen_to_voice)
    obstacle_thread = threading.Thread(target=obstacle_avoidance)

    # Start the threads
    flask_thread.start()
    voice_thread.start()
    obstacle_thread.start()

    # Keep the main thread running
    flask_thread.join()
    voice_thread.join()
    obstacle_thread.join()
