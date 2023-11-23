"""
This function will open webcam and start capture front_face's user
"""
import cv2
import os
from addDataToDatabase import Control
import time
from addDataToDatabase import Firebase
from firebase_admin import storage,credentials
import addDataToDatabase

def newPerson():
    # Fname = str(input("Type your first name: "))
    # Lname = str(input("Type your last name: "))
    Name = str(input("Type your name here: "))
    idstudent = str(input("Type your student id: "))
    village = str(input("Type your hometown here: "))
    # Control.addPerson("", Fname, Lname,idstudent,village)
    Control.addPerson("", Name, idstudent, village)
    os.makedirs("./images/" + str(idstudent))
    return "Adding {} to dataset".format(Name), idstudent

def storeUserImage():
    msg, idstudent = newPerson()
    print(msg)
    print("Start create dataset...")
    face_cascade = cv2.CascadeClassifier(
        "./cascades/data/haarcascade_frontalface_alt.xml"
    )
    video = cv2.VideoCapture(0)
    count = 0
    count_shot = 10
    while True:
        check, data = video.read()
        faces = face_cascade.detectMultiScale(data, scaleFactor=1.5, minNeighbors=5)
        for x, y, w, h in faces:
            cv2.rectangle(data, (x, y), (x + w, y + h), (0, 255, 0), 3)
            if count_shot == 0:
                cv2.imwrite("./images/" + idstudent + "/" + str(count) + ".jpg", data)
                count += 1
                count_shot = 10
            count_shot = count_shot - 1
        cv2.waitKey(3)
        cv2.imshow("Face Detect", data)
        key = cv2.waitKey(1)

        # Press 'q' to exit
        if key == ord("q") or count == 30:
            break
    print("added!")
    # add first image for data
    # path to user_capture
    folder_path = f"images/{idstudent}"
    # Lấy danh sách các tệp tin trong thư mục
    file_list = os.listdir(folder_path)
    if file_list:
        first_image_path = os.path.join(folder_path, file_list[0])

        # Upload ảnh lên Firebase Storage
        bucket = storage.bucket()
        image_blob = bucket.blob(f"images/{idstudent}/{file_list[0]}")
        image_blob.upload_from_filename(first_image_path)
        # Lấy URL của ảnh sau khi upload
        download_url = image_blob.public_url

        print("First image uploaded. File available at", download_url)
    else:
        print("No images found in the specified folder.")
    #####################
    # Release memory
    video.release()


storeUserImage()
cv2.destroyAllWindows()