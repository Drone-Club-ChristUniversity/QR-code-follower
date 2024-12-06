from flask_video.app import app, capture_video
import threading
import cv2
from pypluto import pluto
from time import sleep
from getQrCoordinates import get_coordinates

X_LEN = 640
Y_LEN = 480

Drone = pluto()

Drone.cam()
sleep(1)

Drone.connect()
sleep(2)

Drone.arm()
sleep(2)

# Start video capture thread
video_thread = threading.Thread(target=capture_video)
video_thread.daemon = True
video_thread.start()

# Start Flask app
app.run(host='0.0.0.0', port=5000)

# Get video Feed

cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")
cap.set(3,X_LEN)
cap.set(4,Y_LEN)

while True:

    success, img = cap.read()

    # GET QR CODE POSITION
    data_points = get_coordinates(img)

    # MANUPULATE DRONE POSITION

    # ROLL
    if data_points["middle"][0] > X_LEN/2:
        Drone.rcRoll += 50
    elif data_points["middle"][0] < X_LEN/2:
        Drone.rcRoll -= 50

    # THROTTLE
    if data_points["middle"][1] > Y_LEN/2:
        Drone.rcThrottle += 50
    elif data_points["middle"][1] < Y_LEN/2:
        Drone.rcThrottle -= 50

    # PITCH
    if data_points["diagonal"] > 10:
        Drone.rcPitch -= 50
    elif data_points["diagonal"] < 10:
        Drone.rcPitch += 50
    
    # OUTPUT 
    cv2.imshow('Result',img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

Drone.disconnect()
