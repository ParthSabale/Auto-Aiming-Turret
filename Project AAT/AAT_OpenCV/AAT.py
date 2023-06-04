import cv2
import numpy as np
import serial
import time

ser = serial.Serial('COM3', 9600, timeout=1)


def send_command(command):
    ser.write(command.encode())
    data = ser.readline().decode('ascii')
    return data


def shoot():
    return send_command('1')


def HR():
    return send_command('2')


def HL():
    return send_command('3')


def VD():
    return send_command('4')


def VU():
    return send_command('5')


capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower1 = np.array([0, 100, 100])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([160, 100, 100])
    upper2 = np.array([179, 255, 255])

    vbh1 = cv2.inRange(hsv, lower1, upper1)
    vbh2 = cv2.inRange(hsv, lower2, upper2)
    vaibhav = cv2.bitwise_or(vbh1, vbh2)

    contours, hierarchy = cv2.findContours(vaibhav, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 100), 3)

    a = 0
    b = 0
    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        m = cv2.moments(cnt)
        if m['m00'] != 0:
            a = int(m['m10'] / m['m00'])
            b = int(m['m01'] / m['m00'])

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 100)
    if circles is not None:
        for i in circles:
            x = int(i[0][0])
            y = int(i[0][1])
            z = int(i[0][2])
            r1 = int(z / 2)
            cv2.rectangle(frame, (x - r1, y - r1), (x + r1, y + r1), (0, 0, 255))

            if (a > (x - r1)) & (a < (x + r1)) & (b > (y - r1)) & (b < (y + r1)):
                print("Target detected")
                print("Shoot")
                print(shoot())
                time.sleep(5)
            elif a < (x - r1):
                print(HR())
            elif a > (x + r1):
                print(HL())
            elif b < (y - r1):
                print(VU())
            elif b > (y - r1):
                print(VD())

    cv2.imshow("Detecting Program", frame)

    # Termination of program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
