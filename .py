import os
import time
import speech_recognition as sr
from flask import Flask, render_template, request
from picarx import PicarX  # Using SunFounder PiCar-X package

px = PicarX()

app = Flask(__name__)

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

@app.route('/move')
def move():
    direction = request.args.get('dir')
    move_car(direction)
    return f"Car moved {direction}"

def listen_to_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized: {command}")
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
        print("Could not understand audio")
    except sr.RequestError:
        print("Speech recognition service error")

def obstacle_avoidance():
    while True:
        distance = px.get_distance()
        if distance < 20:
            print("Obstacle detected! Stopping.")
            px.stop()
            time.sleep(0.1)

if __name__ == '__main__':
    os.system('flask run --host=0.0.0.0 --port=5000 &')
    while True:
        listen_to_voice()
        obstacle_avoidance()
