import RPi.GPIO as GPIO
import cv2
import numpy as np

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Pins (make sure to use the correct GPIO pins for your Picar-X)
LEFT_MOTOR_FORWARD = 17
LEFT_MOTOR_BACKWARD = 18
RIGHT_MOTOR_FORWARD = 22
RIGHT_MOTOR_BACKWARD = 23

# Set up motor pins
GPIO.setup(LEFT_MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_MOTOR_BACKWARD, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_BACKWARD, GPIO.OUT)

# Motor control functions
def move_forward():
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.LOW)

def move_backward():
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.HIGH)

def turn_left():
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.LOW)

def turn_right():
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.HIGH)

def stop():
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.LOW)

# Camera Setup
cap = cv2.VideoCapture(0)  # Change if you use a different camera

# Color ranges for line detection (change these depending on the path color)
LOWER_COLOR = np.array([0, 0, 0], dtype=np.uint8)  # Black path (example)
UPPER_COLOR = np.array([180, 255, 80], dtype=np.uint8)

def process_frame(frame):
    """Process the frame to detect the color line"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)
    
    # Find contours to detect the line
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def follow_line():
    """Logic to follow the line based on color detection"""
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        contours = process_frame(frame)
        
        if contours:
            # Assume the largest contour is the line
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            # Find the center of the contour
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Visualize the center of the line (optional)
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                
                # If the line is to the left or right, turn accordingly
                if cx < 200:  # Turn Left
                    turn_left()
                elif cx > 440:  # Turn Right
                    turn_right()
                else:  # Move Forward
                    move_forward()
            else:
                stop()  # If no contour found, stop
        else:
            stop()  # Stop if no path is detected
        
        # Show the frame (for debugging)
        cv2.imshow("Line Following", frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()

if __name__ == "__main__":
    follow_line()
