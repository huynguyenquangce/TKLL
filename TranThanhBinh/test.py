from datetime import datetime

# Giả sử bạn có hai chuỗi thời gian
time_str1 = "2023-11-10 15:55:58"
time_str2 = "2023-11-10 12:30:45"

# Chuyển đổi chuỗi thành đối tượng datetime
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

# Kiểm tra điều kiện và tăng biến count nếu thỏa mãn
count = 0
if hours > 3 or (hours == 3 and minutes > 10):
    count += 1

# In kết quả
print(f"Kết quả: {count}")
