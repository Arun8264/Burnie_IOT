# Burnie_IOT
Burnie Robot who guides people to find some destination
<br>
Team Members:
<br>
Arun Saini (A00290088)
<br>
Aqib Ameen (A00289644)
<br>
Aayush Saini (A00270748)
<br>
Bryan Guzman (A00287695)
<br>
Harold Reyes (A00281588)

# Room-Tracking Robot  

## 🛠 Project Overview  
This project aims to build a robot that can:  
1. Identify different colors assignede with their respective locations.  
2. Interact with users using 7 inch raspberrypi screen with  a user friendly interface .  
3. Navigate to the specified location by navigating through different color .  

---

## 🚀 Current Goals  
- Design the basic layout of the testing field.  
- Set up the robot chassis and hardware.  
- Begin programming the robot for basic movement.  
- Integrate  7 inch respberrypi screen functionality.  

---

## 🖥️ Technologies and Tools  
- **Hardware**:  
  - Microcontroller (e.g., Raspberry Pi or Arduino)  
  - Motors  
  - Ultrasonic/IR sensors  
  - Robot chassis  
  - PiCar-X
  - Camera and SD Card
  - Battries 
- **Software**:  
  - Python  
  -   
  - Basic pathfinding logic



Explanation of file burnie_logic.py Code:
GPIO Setup: We set up GPIO pins to control the motors. You'll need to connect your motors to the Raspberry Pi GPIO pins, and ensure that the motor driver (like L298N or similar) is wired correctly.

Motor Control Functions: The move_forward, move_backward, turn_left, and turn_right functions are used to control the robot's movement.

Camera Setup: The camera is set up using OpenCV. The Raspberry Pi camera module or a USB webcam can be used for capturing frames.

Color Detection: We use the HSV color space to filter out the color of the path the robot should follow. The process_frame function detects the contours of the line and finds the center of the line to make movement decisions.

Line Following Logic: The robot will follow the line by adjusting its direction based on the center of the detected line. If the line is off-center (too far left or right), the robot will turn until it's centered again.

Stopping Condition: If no line is detected, the robot will stop.

Adjustments:
Colors: If your path uses different colors, you’ll need to adjust the LOWER_COLOR and UPPER_COLOR values for the specific color you’re following (e.g., red, blue, green).

Frame Size and Center: The line detection assumes a center of the frame around which the robot will adjust its movement.



This code serves as a basic line-following logic that you can later integrate with your front-end user interface, where the user can control which color path the robot follows.