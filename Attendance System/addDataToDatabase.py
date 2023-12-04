import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred,{
     'databaseURL':"https://rawda-7ee0e-default-rtdb.firebaseio.com/",
'storageBucket':"rawda-7ee0e.appspot.com"
 })
import os
import glob

# bucket = storage.bucket()
image_directory= "img/"

class Firebase:
    # def updateFlag(self):
    #     flag = db.reference('flags')
    #     flag.update({'Flagcheck': True})

    def clearHistory(self):
        history = db.reference('history')
        history.delete()
        return "delete all turns"

    def clearPerson(self):
        persons = db.reference('persons')
        persons.delete()
        return "Delete all persons"

    # def getNameById(self, id):
    #     persons = db.reference('persons')
    #     # Sử dụng get() để lấy dữ liệu của "persons"
    #     persons_data = persons.get()
    #     Fname, Lname = "", ""
    #     if persons_data is not None:
    #         for person_info in persons_data:
    #             if person_info.get('id') == id:
    #                 Fname = person_info.get('Fname', '')
    #                 Lname = person_info.get('Lname', '')
    #                 break
    #     return Fname, Lname

class Control:
    def addPerson(self,Name,idstudent,village,position):
        persons = db.reference('person')
        # Lấy danh sách người từ Firebase
        persons_data = persons.get()
        # num_persons = len(persons_data) if persons_data else 0

        # Tạo một bản ghi mới
        newPerson = {
            "Name": Name,
            "ID": idstudent,
            "Hometown": village,
            "Position":position,
            "createAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_attendance":0,
            "attendance_processed": False
        }
        persons.child(idstudent).set(newPerson)

    def addCheckin(self,Name,idstudent):
        checkin = db.reference('checkin')
        timeEvent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         # Tạo một lượt mới
        newTurn = {
                # "urlimg": imgUrl,
            "Name": Name,
            "ID": idstudent,
            "checkinTime": timeEvent,
        }
        # Thêm lượt mới vào Firebase với Personid là tên của node con
        checkin.child(str(idstudent)).set(newTurn)

    def addCheckout(self,Name,idstudent):
        checkout = db.reference('checkout')
        timeEvent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Tạo một lượt mới
        newTurn = {
              # "urlimg": imgUrl,
            "Name": Name,
            "ID": idstudent,
            "checkoutTime": timeEvent,
        }
            # Thêm lượt mới vào Firebase với Personid là tên của node con
        checkout.child(str(idstudent)).set(newTurn)

    def getNameById(self, given_id):
        persons_ref = db.reference('person')

        # Lấy dữ liệu của node 'person'
        persons_data = persons_ref.get()

        for person_id, person_data in persons_data.items():
            # Kiểm tra nếu ID của người bằng với ID đã cho
            if person_id == given_id:
                # Trả về tên của người đó
                return person_data.get("Name")

        # Trường hợp không tìm thấy ID
        return None

    def getTimeCheckIn(self,id):
        input = db.reference('checkin')
        checkin_data = input.get()
        for person_id, person_data in checkin_data.items():
            # Kiểm tra nếu ID của người bằng với ID đã cho
            if person_id == id:
                # Trả về tên của người đó
                return person_data.get("checkinTime")

        # Trường hợp không tìm thấy ID
        return None

    def getTimeCheckOut(self,id):
        input = db.reference('checkout')
        checkin_data = input.get()
        for person_id, person_data in checkin_data.items():
            # Kiểm tra nếu ID của người bằng với ID đã cho
            if person_id == id:
                # Trả về tên của người đó
                return person_data.get("checkoutTime")

        # Trường hợp không tìm thấy ID
        return None

    def compareTime(self,time_str1,time_str2,id):

        temp_ref = db.reference(f'person/{id}')
        temp = temp_ref.get()
        time1 = datetime.strptime(time_str1, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.strptime(time_str2, "%Y-%m-%d %H:%M:%S")

        # Thực hiện phép trừ
        time_difference = time1 - time2

        # Lấy tổng số giây chênh lệch
        total_seconds = time_difference.total_seconds()

        # Tách giờ, phút và giây từ tổng số giây chênh lệch
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        print(f"{hours} giờ, {minutes} phút, {seconds} giây")
        # if (hours == 0 and minutes ==0 and seconds >= 30):
        #     temp['total_attendance'] += 1
        #     # Cập nhật giá trị trong cơ sở dữ liệu
        #     temp_ref.update({'total_attendance': temp['total_attendance']})
        if hours == 0 and minutes == 0 and seconds >= 5 and not temp.get('attendance_processed', False):
            temp['total_attendance'] += 1
            temp['attendance_processed'] = True  # Đặt biến flag thành True để đánh dấu là đã xử lý
            # Cập nhật giá trị trong cơ sở dữ liệu
            temp_ref.update({'total_attendance': temp['total_attendance'], 'attendance_processed': True})

    def resetCheck(self,id):
        temp_ref = db.reference(f'person/{id}')
        temp = temp_ref.get()
        temp['attendance_processed'] = False
        temp_ref.update({'attendance_processed': temp['attendance_processed']})

    def addpersonHistory(self,idstudent,name,checkInTime,checkOutTime):
        history = db.reference('history')
        day_ref = db.reference("/history/" + idstudent + "/day")
        current_date = datetime.now()
        day = current_date.day
        month = current_date.month
        year = current_date.year
        formatted_date = str(day) + '-' + str(month) + '-' + str(year)
        newTurn = {
              # "urlimg": imgUrl,
            "Name": name,
            "ID": idstudent,
            "checkInTime": checkInTime,
            "checkOutTime": checkOutTime
        }
        history.child(str(idstudent)).child(formatted_date).set(newTurn)











    # get imgUrl
    # def getImageUrl(self):
    #     files = glob.glob("img/*.png")
    #     imgName = max(files, key=os.path.getctime)
    #     imgUrl = imgName
    #     return str(imgUrl)

    # def addImageToDatabase(self):
    #     for filename in os.listdir(image_directory):
    #         if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
    #             local_image_path = os.path.join(image_directory, filename)
    #             firebase_storage_path = f'images/{filename}'  # Đặt tên tùy ý
    #
    #             # Đọc nội dung của tệp ảnh cục bộ
    #             with open(local_image_path, 'rb') as image_file:
    #                 image_data = image_file.read()
    #
    #             # Tải lên ảnh lên Firebase Storage
    #             blob = bucket.blob(firebase_storage_path)
    #             blob.upload_from_string(image_data)
    #
    #             # Lấy URL của ảnh sau khi đã tải lên
    #             uploaded_image_url = blob.public_url
    #
    #             print(f"Ảnh {filename} đã được tải lên và có URL: {uploaded_image_url}")