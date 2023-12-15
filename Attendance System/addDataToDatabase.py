import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime,time,timedelta
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
     'databaseURL':"https://fir-c20cd-default-rtdb.asia-southeast1.firebasedatabase.app/",
'storageBucket':"fir-c20cd.appspot.com"
 })
import os
import glob

# bucket = storage.bucket()
# xử lí thời gian làm việc của công ty
image_directory= "img/"
checkIn_request = time(2, 16, 0)
checkOut_request = time(2, 17, 5)
time_difference = timedelta(hours=checkOut_request.hour - checkIn_request.hour,
                            minutes=checkOut_request.minute - checkIn_request.minute,
                            seconds=checkOut_request.second - checkIn_request.second)
request_time = time_difference.total_seconds()*1000
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

    # def compareTime(self,time_str1,time_str2,id):
    #     temp_ref = db.reference(f'person/{id}')
    #     temp = temp_ref.get()
    #     time1 = datetime.strptime(time_str1, "%Y-%m-%d %H:%M:%S")
    #     time2 = datetime.strptime(time_str2, "%Y-%m-%d %H:%M:%S")
    #     # test //////////////////////////////////////////////////////////////////////////////////
    #
    #
    #     # Ví dụ: Đối tượng checkOuttime
    #     time_str2 = datetime.now()
    #     # Giờ checkOut quy định
    #     attendance_checkOutTime = time_str2.replace(hour=20, minute=12, second=0, microsecond=0)
    #     time_differenceCO = time1 - attendance_checkOutTime
    #     #test //////////////////////////////////////////////////////////////////////////////////////
    #
    #     # Thực hiện phép trừ
    #     # time_difference = time1 - time2
    #
    #     # Lấy tổng số giây chênh lệch
    #     total_seconds2 = time_differenceCO.total_seconds()
    #
    #     # Tách giờ, phút và giây từ tổng số giây chênh lệch
    #     hours2, remainder = divmod(total_seconds2, 3600)
    #     minutes2, seconds2 = divmod(remainder, 60)

# # CheckOut
#         # print(f"{hours} giờ, {minutes} phút, {seconds} giây")
#         if hours2 >= 0 and minutes2 >= 0 and seconds2 >= 0 and not temp.get('attendance_processed', False):
#             temp['total_attendance'] += 1
#             temp['attendance_processed'] = True  # Đặt biến flag thành True để đánh dấu là đã xử lý
#             # Cập nhật giá trị trong cơ sở dữ liệu
#             temp_ref.update({'total_attendance': temp['total_attendance'], 'attendance_processed': True})



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

        # # Ví dụ: Đối tượng checkIntime
        # time_str1 = datetime.now()
        #
        # # Giờ checkIn quy định
        # attendance_checkInTime = time_str1.replace(hour=10, minute=12, second=0, microsecond=0)
        # compare_checkIn = checkInTime - attendance_checkInTime
        checkInTime_temp = datetime.strptime(checkInTime, "%Y-%m-%d %H:%M:%S")
        checkOutTime_temp = datetime.strptime(checkOutTime, "%Y-%m-%d %H:%M:%S")
        isLate = checkInTime_temp.time() > checkIn_request
        isSooner = checkOutTime_temp.time() < checkOut_request
        newTurn = {
              # "urlimg": imgUrl,
            "isLate" : isLate,
            "isSooner": isSooner,
            "Name": name,
            "ID": idstudent,
            "checkInTime": checkInTime,
            "checkOutTime": checkOutTime,
            "request_time": request_time
        }
        history.child(str(formatted_date)).child(idstudent).set(newTurn)

    def addUrlImg(self,download_url,idstudent):
        persons = db.reference('person')
        newURL = {
            "imgURL":download_url
        }
        persons.child(idstudent).set(newURL)

    def add_field_to_person(self,idstudent,field_name,field_value):
        # Tham chiếu đến nút cụ thể trong Database
        ref = db.reference(f'person/{idstudent}')

        # Thêm trường dữ liệu mới
        ref.update({field_name: field_value})








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