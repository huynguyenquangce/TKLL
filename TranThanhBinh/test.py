# from datetime import datetime

# # Giả sử bạn có hai chuỗi thời gian
# time_str1 = "2023-11-10 15:55:58"
# time_str2 = "2023-11-10 12:30:45"
#
# # Chuyển đổi chuỗi thành đối tượng datetime
# time1 = datetime.strptime(time_str1, "%Y-%m-%d %H:%M:%S")
# time2 = datetime.strptime(time_str2, "%Y-%m-%d %H:%M:%S")
#
# # Thực hiện phép trừ
# time_difference = time1 - time2
#
# # Lấy tổng số giây chênh lệch
# total_seconds = time_difference.total_seconds()
#
# # Tách giờ, phút và giây từ tổng số giây chênh lệch
# hours, remainder = divmod(total_seconds, 3600)
# minutes, seconds = divmod(remainder, 60)
#
# print(f"{hours} giờ, {minutes} phút, {seconds} giây")
#
# # Kiểm tra điều kiện và tăng biến count nếu thỏa mãn
# count = 0
# if hours > 3 or (hours == 3 and minutes > 10):
#     count += 1
#
# # In kết quả
# print(f"Kết quả: {count}")
# from datetime import datetime
import cv2
import os
import firebase_admin
from firebase_admin import credentials, storage

# Khởi tạo Firebase với tệp tin cấu hình đã tải từ Firebase Console
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket':'fir-c20cd.appspot.com'})

def capture_and_upload_image():
    # Nhập tên từ người dùng
    ID = input("Nhập ID: ")

    # Tạo thư mục 'img' nếu nó chưa tồn tại
    img_folder = "img"
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # TODO: Thêm mã để chụp ảnh bằng OpenCV
    # Ví dụ: sử dụng OpenCV để chụp ảnh từ webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # Lưu ảnh vào thư mục với tên do người dùng nhập
    img_path = os.path.join(img_folder, f"{ID}.jpg")
    cv2.imwrite(img_path, frame)

    # Upload ảnh lên Firebase Storage
    bucket = storage.bucket()
    image_blob = bucket.blob(f"images/{ID}.jpg")
    image_blob.upload_from_filename(img_path)

    # Lấy URL của ảnh sau khi upload
    download_url = image_blob.public_url

    # TODO: Liên kết URL với dữ liệu trong Firebase Database (nếu cần)

    print("File available at", download_url)

    # Xóa tệp tin tạm thời
    os.remove(img_path)

# Chạy hàm để chụp và upload ảnh
capture_and_upload_image()


