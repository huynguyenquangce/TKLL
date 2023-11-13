import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred,{
#     'databaseURL':"https://faceattendancerealtime-8bc2f-default-rtdb.firebaseio.com/"
# })
# firebase_admin.initialize_app(cred,{
#     'databaseURL':"https://datkll-781f0-default-rtdb.firebaseio.com/"
# })
firebase_admin.initialize_app(cred,{
     'databaseURL':"https://fir-c20cd-default-rtdb.asia-southeast1.firebasedatabase.app/"
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
    # def addPerson(self,Fname,Lname,idstudent,village):
    #     persons = db.reference('person')
    #     # Lấy danh sách người từ Firebase
    #     persons_data = persons.get()
    #     # num_persons = len(persons_data) if persons_data else 0
    #
    #     # Tạo một bản ghi mới
    #     newPerson = {
    #         # "id": num_persons,
    #         "Fname": Fname,
    #         "Lname": Lname,
    #         "MSSV": idstudent,
    #         "Quequan": village,
    #         "createAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     }
    #     persons.child(str(idstudent)).set(newPerson)
    #
    def addPerson(self,Name,idstudent,village):
        persons = db.reference('person')
        # Lấy danh sách người từ Firebase
        persons_data = persons.get()
        # num_persons = len(persons_data) if persons_data else 0

        # Tạo một bản ghi mới
        newPerson = {
            # "id": num_persons,
            "Name": Name,
            "Quequan": village,
            "createAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_attendance":0,
            "attendance_processed": False
        }
        persons.child(idstudent).set(newPerson)

    # def addHistory(self,imgUrl,Personid,__v,Status=True,Response=False):
    #         history = db.reference('history')
    #         timeEvent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #         # Tạo một lượt mới
    #         newTurn = {
    #             "urlimg": imgUrl,
    #             "Status": Status,
    #             "Personid": Personid,
    #             "updateAt": timeEvent,
    #             "__v": __v,
    #             "Response": Response
    #         }
    #         # Thêm lượt mới vào Firebase với Personid là tên của node con
    #         history.child(str(Personid)).set(newTurn)
    # def getIdStudentByFnameLame(self,idstudent):


    def addCheckin(self,Name,idstudent):
        checkin = db.reference('checkin')
        timeEvent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         # Tạo một lượt mới
        newTurn = {
                # "urlimg": imgUrl,
            "Name": Name,
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
            "checkoutTime": timeEvent,
        }
            # Thêm lượt mới vào Firebase với Personid là tên của node con
        checkout.child(str(idstudent)).set(newTurn)

    # def getIdbyName(self, name):
    #     persons = db.reference('person')
    #     persons_data = persons.get()
    #
    #     for idstudent, person_data in persons_data.items():
    #         if person_data.get("Name") == name:
    #             return idstudent
    #
    #     # Trường hợp không tìm thấy
    #     return None

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
    # def getTotalAttendance(self,id):
    #     persons = db.reference("person")
    #     person_data=persons.get()
    #     for person_id, person_data in person_data.items():
    #         # Kiểm tra nếu ID của người bằng với ID đã cho
    #         if person_id == id:
    #             # Trả về tên của người đó
    #             person_data.get("total_attendance")+=1

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
        if hours == 0 and minutes == 0 and seconds >= 15 and not temp.get('attendance_processed', False):
            temp['total_attendance'] += 1
            temp['attendance_processed'] = True  # Đặt biến flag thành True để đánh dấu là đã xử lý
            # Cập nhật giá trị trong cơ sở dữ liệu
            temp_ref.update({'total_attendance': temp['total_attendance'], 'attendance_processed': True})

    def resetCheck(self,id):
        temp_ref = db.reference(f'person/{id}')
        temp = temp_ref.get()
        temp['attendance_processed'] = False
        temp_ref.update({'attendance_processed': temp['attendance_processed']})














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