import cv2
import numpy as np
import RPi.GPIO as GPIO
import time 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


motor1A = 33
motor1B = 32
motor2A = 31
motor2B = 29
Ena=7

GPIO.setup(Ena,GPIO.OUT)
GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)

pwm=GPIO.PWM(Ena,100)
pwm.start(0)


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
#cap.set(10,150)

_,frame = cap.read()
rows, cols, _ =frame.shape
x_medium = int(cols/2)
y_medium = int(cols/2)


while True:
    success, img = cap.read() #her frame degerini okuyor ve bunu img kaydediyor
    frame = cv2.flip(img, 1)
    imgContour = img.copy()

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([45, 100,50])
    upper = np.array([75, 255,255])
    mask = cv2.inRange(imgHSV, lower, upper)
    green = cv2.bitwise_and(img, img, mask = mask)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse = True)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        x_medium = int((x + x + w) / 2)
        y_medium = int((y + y + h) / 2)
        frame_center_x = frame.shape[1] // 2
        x_diff = x_medium - frame_center_x
        
        break
    frame_center_x = frame.shape[1] // 2
    frame_center_y = frame.shape[0] // 2
    x_diff = x_medium - frame_center_x
    y_diff = y_medium - frame_center_y

    cv2.line(img, (x_medium ,0), (x_medium, 480), (0, 255, 0), 2)
    cv2.line(img, (0 ,y_medium), (640, y_medium), (0, 255, 0), 2)
    
    if abs(x_diff) > 20:
            if x_diff > 0:
                
                GPIO.output(motor1A, GPIO.LOW)
                GPIO.output(motor1B, GPIO.LOW)
                GPIO.output(motor2A, GPIO.HIGH)
                GPIO.output(motor2B, GPIO.LOW)
            else:
                 
                GPIO.output(motor1A, GPIO.HIGH)
                GPIO.output(motor1B, GPIO.LOW)
                GPIO.output(motor2A, GPIO.LOW)
                GPIO.output(motor2B, GPIO.LOW)
    else:
            
                GPIO.output(motor1A, GPIO.LOW)
                GPIO.output(motor1B, GPIO.LOW)
                GPIO.output(motor2A, GPIO.LOW)
                GPIO.output(motor2B, GPIO.LOW)
    
    
    
    if abs(y_diff) > 30:
            if y_diff > 0:
                
                GPIO.output(motor1A, GPIO.LOW)
                GPIO.output(motor1B, GPIO.HIGH)
                GPIO.output(motor2A, GPIO.LOW)
                GPIO.output(motor2B, GPIO.HIGH)
            
    else:
            
                GPIO.output(motor1A, GPIO.LOW)
                GPIO.output(motor1B, GPIO.LOW)
                GPIO.output(motor2A, GPIO.LOW)
                GPIO.output(motor2B, GPIO.LOW)
              
    
    cv2.imshow("video", img)
    #cv2.imshow("img", mask)
    #cv2.imshow("green", green)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break