# Printer Service

## Giới thiệu
Đây là phần triển khai backend cho dự án, cung cấp các API để quản lý và tích hợp dịch vụ in ấn.

## Cấu Trúc Thư Mục
- **config/**: Chứa các tệp cấu hình cho dự án.
- **controllers/**: Chứa các controller xử lý logic của ứng dụng.
- **helper/**: Chứa các hàm tiện ích dùng chung.
- **middlewares/**: Chứa các middleware dùng để kiểm tra và xử lý trước/giữa các yêu cầu.
- **models/**: Chứa các mô hình dữ liệu liên quan.
- **routes/**: Chứa các tệp định tuyến API.  

## Files
- **.env**: Tệp chứa các biến môi trường như thông tin kết nối cơ sở dữ liệu, khóa bí mật, v.v.
- **api.md**: Tài liệu chi tiết về các API mà hệ thống cung cấp.
- **main.py**: Tệp chính để khởi động ứng dụng.
- **requirements.txt**: Danh sách các thư viện cần thiết cho dự án.
  
## Yêu cầu hệ thống
- Python 3.x
- Các thư viện được liệt kê trong `requirements.txt`
- Môi trường cấu hình như trong tệp `.env`

## Cách Chạy Dự Án 
1. **Clone kho lưu trữ**:
```sh
git clone https://github.com/eLtieK/printer-service.git
cd printer-service
```
2. **Cài đặt các yêu cầu**:
- Đảm bảo bạn đang trong môi trường Python ảo (virtual environment).
```sh
pip install -r requirements.txt
```
3. **Chạy dự án**:
```sh
python main.py
```
4. **Chạy dự án**:
Mặc định, ứng dụng sẽ chạy ở địa chỉ `http://localhost:8000`

## Chú ý
- Nếu có lỗi phát sinh, kiểm tra lại tệp `.env` và đảm bảo cơ sở dữ liệu hoặc các dịch vụ phụ trợ đang hoạt động.
- Đọc thêm tài liệu trong `api.md` để biết cách sử dụng các API.

