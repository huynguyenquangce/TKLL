from datetime import time, timedelta

checkIn_request = time(2, 16, 0)
checkOut_request = time(2, 17, 5)

# Tạo đối tượng timedelta bằng cách lấy sự chênh lệch giữa hai thời điểm
time_difference = timedelta(hours=checkOut_request.hour - checkIn_request.hour,
                            minutes=checkOut_request.minute - checkIn_request.minute,
                            seconds=checkOut_request.second - checkIn_request.second)

# Chuyển đổi khoảng thời gian từ timedelta sang giây
seconds_difference = time_difference.total_seconds()

print("Khoảng thời gian giữa hai thời điểm là:", seconds_difference, "giây")
