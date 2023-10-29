import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-8bc2f-default-rtdb.firebaseio.com/"
})

# # person = db.reference('persons')
# history = db.reference('history')
# flag = db.reference('flags')

class Firebase:
    def updateFlag(self):
        flag = db.reference('flags')
        flag.update({'Flagcheck': True})

    def clearHistory(self):
        history = db.reference('history')
        history.delete()
        return "delete all turns"

    def clearPerson(self):
        persons = db.reference('persons')
        persons.delete()
        return "Delete all persons"

    def getNameById(self, id):
        persons = db.reference('persons')
        # Sử dụng get() để lấy dữ liệu của "persons"
        persons_data = persons.get()
        Fname, Lname = "", ""
        for person_id, person_info in persons_data.items():
            if person_id == id:
                Fname = person_info.get('Fname', '')
                Lname = person_info.get('Lname', '')
                break  # Thoát khỏi vòng lặp khi tìm thấy ID phù hợp
        return Fname, Lname

class Control:
    def addPerson(self,Fname,Lname,status=True):
        persons = db.reference('persons')
        # Lấy danh sách người từ Firebase
        persons_data = persons.get()
        num_persons = len(persons_data) if persons_data else 0

        # Tạo một bản ghi mới
        newPerson = {
            "id": num_persons,
            "Fname": Fname,
            "Lname": Lname,
            "Status": status,
            "createAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updateAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "__v": 0,
        }
        persons.child(str(num_persons)).set(newPerson)

    def addHistory(self,imgUrl,Personid,__v,Status=True,Response=False):
        history = db.reference('history')
        timeEvent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Tạo một lượt mới
        newTurn = {
            "urlimg": imgUrl,
            "Status": Status,
            "createAt": timeEvent,
            "__v": __v,
            "Response": Response
        }
        # Thêm lượt mới vào Firebase với Personid là tên của node con
        history.child(Personid).push(newTurn)

    # get imgUrl
    # def getImageUrl(self):
    #     files = glob.glob("..\public\img\*.jpg")
    #     imgName = max(files, key=os.path.getctime)
    #     imgUrl = "../img/" + imgName[14::]
    #     return str(imgUrl)