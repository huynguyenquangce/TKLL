# import numpy as np
# import threading
import cv2
import pickle
from addDataToDatabase import Control
import pyttsx3
import numpy as np
face_cascade = cv2.CascadeClassifier("./cascades/data/haarcascade_frontalface_alt2.xml")

#khởi tạo speaker
engine = pyttsx3.init()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

cap = cv2.VideoCapture(0)

# Rescale frameq
def make_720p():
    cap.set(3, 640)
    cap.set(4, 480)

count_stranger = 30
count_relative = 20
temp_id = 0
flag = 0
person_name = ""
check = np.full(shape=100,fill_value=False, dtype=bool)
make_720p()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Cascade face_cascade
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        # print(x, y, w, h)
        roi_gray = gray[y : y + h, x : x + w]  # (y_coordinate_start, y_coordinate_end)
        roi_color = frame[y : y + h, x : x + w]
        # Recognize: Deep learned model predict keras tensorflow pytorch scikit learn
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45 and conf <= 85:
            # count_relative to recognize
            if temp_id != id_:
                count_relative = 20
            temp_id = id_
            person_name = labels[id_]
            count_relative = count_relative - 1

            # # Write person's name
            font = cv2.FONT_HERSHEY_SIMPLEX
            # name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, person_name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            fullname = Control.getNameById("",person_name)
            if not check[temp_id]:
                Control.addCheckin("", fullname,person_name)
                Control.resetCheck("", person_name)
                check[temp_id]=True
            else:
                Control.addCheckout("",fullname,person_name)

            if count_relative == 0:
                print("Successfully")
                count_stranger = 30
                count_relative = 20
                flag = 1
                # getTime checkIn + checkOut and compare
                timeCheckIn = Control.getTimeCheckIn("", person_name)
                timeCheckOut = Control.getTimeCheckOut("", person_name)
                # Control.compareTime("", timeCheckOut, timeCheckIn, person_name)
                Control.addpersonHistory("",person_name,fullname,timeCheckIn,timeCheckOut)
                text = f"Hello{fullname}. Hope you have a good day."
                engine.say(text)
                engine.runAndWait()
                break
        else:
            # Write person's name
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = "Unknown"
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            #speaker
            count_stranger = count_stranger - 1
            if count_stranger == 0:
                print("Who are you??")
                count_stranger = 30
                count_relative = 20
                flag = 2
                text1 = f"Who are you?"
                engine.say(text1)
                engine.runAndWait()
                break
        # # Draw a Rectangle
        color = (255, 0, 0)  # BGR 0 - 255
        stroke = 2
        end_cord_x = x + w  # Width of Rectangle
        end_cord_y = y + h  # Height of Recctangle
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
    cv2.imshow("frame", frame)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()