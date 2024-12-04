# 📋 Tài liệu API: Printer Management

## **1. Accounts**

### **Tạo tài khoản**
- **Endpoint**: `{{base_url}}/account/create`
- **Phương thức**: `POST`
- **Headers**:  
  - Không có
- **Body yêu cầu**:
```json
{
  "email": "test@hcmut.edu.vn",
  "role": "spso"
}
```
- **Response**:
```json
{
    "data": {
        "_id": "674fa9765dad6e55b5d58fde",
        "email": "test@hcmut.edu.vn",
        "maintenance_history": [],
        "role": "spso"
    },
    "status": "success"
}
```
- **Mô tả**: API này tạo tài khoản mới. Một yêu cầu thành công sẽ trả về mã trạng thái `201 Created`.

### **Lấy danh sách tài khoản**
- **Endpoint**: `{{base_url}}/account/get`
- **Phương thức**: `GET`
- **Headers**:  
  - Không có
- **Body yêu cầu**:
    - Không có
- **Response**:
```json
[
    {
        "_id": "67488c7fbc7fecd8afe2e6f1",
        "email": "kennezversion@gmail.com",
        "paper_count": 518,
        "print_history": [
            {
                "date": "2024-11-28 23:10:33",
                "file_name": "Report",
                "pages": 50,
                "printer_id": "67488c8bbc7fecd8afe2e6f3"
            }
        ],
        "report_history": [
            {
                "date": "2024-11-28 22:31:59",
                "issue": "Out of order",
                "printer_id": "67488c8bbc7fecd8afe2e6f3"
            }
        ],
        "role": "student"
    },
    {
        "_id": "67493a07daf6be88eb3818f0",
        "email": "kiet.letuan@hcmut.edu.vn",
        "maintenance_history": [
            {
                "date": "2024-12-01 18:54:46",
                "details": "test",
                "printer_id": "67488c8bbc7fecd8afe2e6f3"
            }
        ],
        "role": "spso"
    },
    {
        "_id": "674fa9765dad6e55b5d58fde",
        "email": "test@hcmut.edu.vn",
        "maintenance_history": [],
        "role": "spso"
    }
]
```
- **Mô tả**: API này lấy danh sách tài khoản. Một yêu cầu thành công sẽ trả về mã trạng thái  `200 OK`.

### **Đăng nhập**
- **Endpoint**: `{{base_url}}/account/login`
- **Phương thức**: 
- **Headers**:  
  - Không có
- **Body yêu cầu**:
    - Không có
- **Mô tả**: API này đăng nhập thông qua Oauth2.0 và chuyển hướng đến google đăng nhập.
- **Response**:
```json
{
  "access_token": "ya29.a0AeDClZAYz5YBf64RomyMDa0EenPXlChvvo9FD-qXGoEUJ0dXX_fRauopSIFBkk8yIheufkSkpEqtHQA-zxLV1rCae0sNP4nfBrOEcLVAqeFTygFlDq9czS-lSRCGgH7aOqqv3k1Pq3FemoeDjMNlYVUcDQqLpRepwckaCgYKAS4SARESFQHGX2MiAzW70a9JPNwnT76Bax3QEA0170",
  "email": "kennezversion@gmail.com",
  "role": "student"
}
```

## **1. SPSO**

### **Tạo máy in**
- **Endpoint**: `{{base_url}}/spso/printer`
- **Phương thức**: `POST`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
```json
{
    "name": "Printer A", 
    "model": "HP LaserJet 200", 
    "type": "Laser", 
    "location": "Room 101", 
    "status": "Ready", 
    "manufacturer": "HP", 
    "purchase_date": "2024-01-15", 
    "paper_count": 500, 
    "maintenance_history": [], 
    "report_history": [],
    "print_history": [],
    "ink": { 
        "type": "Black", 
        "level": 70 ,
        "max_print_pages": 1600
    }
}
```
- **Mô tả**: API này tạo một máy in mới và lưu thông tin chi tiết vào hệ thống.
- **Response**:
```json
{
    "data": {
        "_id": "674faa665dad6e55b5d58fe0",
        "ink": {
            "level": 70,
            "max_print_pages": 1600,
            "type": "Black"
        },
        "location": "Room 101",
        "maintenance_history": [],
        "manufacturer": "HP",
        "model": "HP LaserJet 200",
        "name": "Printer A",
        "paper_count": 500,
        "print_history": [],
        "purchase_date": "2024-01-15",
        "report_history": [],
        "status": "Ready",
        "type": "Laser"
    },
    "status": "success"
}
```

### **Cập nhật thông tin máy in**
- **Endpoint**: `{{base_url}}/spso/printer/{printer_id}`
- **Phương thức**: `PATCH`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
    - Không có
- **Mô tả**: API này cho phép cập nhật thông tin máy in. Trường nào cần thay đổi thì chỉ cần truyền đúng trường đó.
- **Response**:
```json
{
    "message": "Printer with ID 674b2b0a04b739e03f4eac22 has been updated.",
    "status": "success"
}
```

### **Xóa máy in theo ID**
- **Endpoint**: `{{base_url}}/spso/printer/{printer_id}`
- **Phương thức**: `DELETE`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
```json
{
    //có thể thay đổi bất kì trường nào có trong data printer
    "name": "Printer B" 
}
```
- **Mô tả**: API này xóa máy in theo ID.
- **Response**:
```json
{
    "message": "Printer with ID 674faa665dad6e55b5d58fe0 has been deleted.",
    "status": "success"
}
```

### **Xem danh sách các máy in**
- **Endpoint**: `{{base_url}}/spso/printer`
- **Phương thức**: `GET`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
    - Không có
- **Mô tả**: API này trả về danh sách tất cả các máy in trong hệ thống.
- **Response**:
```json
[
    {
        "_id": "67488c8bbc7fecd8afe2e6f3",
        "ink": {
            "level": 63.75,
            "max_print_pages": 1600,
            "type": "Black"
        },
        "location": "Room 101",
        "maintenance_history": [
            {
                "date": "2024-12-01 18:54:46",
                "details": "test",
                "spso_id": "67493a07daf6be88eb3818f0"
            }
        ],
        "manufacturer": "HP",
        "model": "HP LaserJet 200",
        "name": "Printer A",
        "paper_count": 350,
        "print_history": [
            {
                "date": "2024-11-01 23:10:33",
                "file_name": "Report",
                "pages": 50,
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "purchase_date": "2024-01-15",
        "report_history": [
            {
                "date": "2024-11-28 22:31:59",
                "issue": "Out of order",
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "status": "Ready",
        "type": "Laser"
    },
    {
        "_id": "67495ce35fb7c916e6c35ce3",
        "paper_price": 1000
    },
    {
        "_id": "674b2b0a04b739e03f4eac22",
        "ink": {
            "level": 70,
            "max_print_pages": 1600,
            "type": "Black"
        },
        "location": "Room 101",
        "maintenance_history": [],
        "manufacturer": "HP",
        "model": "HP LaserJet 200",
        "name": "Printer B",
        "paper_count": 500,
        "print_history": [
            {
                "date": "2024-11-28 23:10:33",
                "file_name": "Report",
                "pages": 50,
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "purchase_date": "2024-01-15",
        "report_history": [],
        "status": "Ready",
        "type": "Laser"
    }
]
```

### **Xem danh sách máy in theo id**
- **Endpoint**: `{{base_url}}/spso/printer/{printer_id}`
- **Phương thức**: `GET`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
    - Không có
- **Mô tả**: API này trả về máy in theo id.
- **Response**:
```json
{
    "data": {
        "_id": "67488c8bbc7fecd8afe2e6f3",
        "ink": {
            "level": 63.75,
            "max_print_pages": 1600,
            "type": "Black"
        },
        "location": "Room 101",
        "maintenance_history": [
            {
                "date": "2024-12-01 18:54:46",
                "details": "test",
                "spso_id": "67493a07daf6be88eb3818f0"
            }
        ],
        "manufacturer": "HP",
        "model": "HP LaserJet 200",
        "name": "Printer A",
        "paper_count": 350,
        "print_history": [
            {
                "date": "2024-11-01 23:10:33",
                "file_name": "Report",
                "pages": 50,
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "purchase_date": "2024-01-15",
        "report_history": [
            {
                "date": "2024-11-28 22:31:59",
                "issue": "Out of order",
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "status": "Ready",
        "type": "Laser"
    },
    "status": "success"
}
```

### **Export báo cáo về việc in**
- **Endpoint**: `{{base_url}}/spso/printer/export_printing_report`
- **Phương thức**: `GET`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
```json
{
    "date_range": "monthly"
}
// """
//     Export printing report with optional filters and date ranges.
    
//     Args:
//         printer_id (str): Optional. ID of the printer to filter by.
//         student_id (str): Optional. ID of the student to filter by.
//         date_range (str): Optional. Date range for the report. Can be 'daily', 'weekly', 'monthly', or 'custom'.
//         start_date (str): Optional. Start date for custom date range in 'YYYY-MM-DD' format.
//         end_date (str): Optional. End date for custom date range in 'YYYY-MM-DD' format.
//     """
```
- **Mô tả**: API này trả về báo cáo với nội dung tuỳ thuộc vào các thông tin yêu cầu.
- **Response**:
```json
{
    "report": [
        {
            "location": "Room 101",
            "model": "HP LaserJet 200",
            "name": "Printer A",
            "print_history": [
                {
                    "date": "2024-11-01 23:10:33",
                    "file_name": "Report",
                    "pages": 50,
                    "student_id": "67488c7fbc7fecd8afe2e6f1"
                }
            ],
            "printer_id": "67488c8bbc7fecd8afe2e6f3",
            "total_pages_printed": 50,
            "total_print_jobs": 1
        },
        {
            "location": "Room 101",
            "model": "HP LaserJet 200",
            "name": "Printer B",
            "print_history": [
                {
                    "date": "2024-11-28 23:10:33",
                    "file_name": "Report",
                    "pages": 50,
                    "student_id": "67488c7fbc7fecd8afe2e6f1"
                }
            ],
            "printer_id": "674b2b0a04b739e03f4eac22",
            "total_pages_printed": 50,
            "total_print_jobs": 1
        }
    ],
    "status": "success",
    "total_pages_printed": 100
}
```

### **Thay đổi giá mua 1 tờ giấy**
- **Endpoint**: `{{base_url}}/spso/printer/paper_price/{price}`
- **Phương thức**: `PATCH`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
    - Không có
- **Mô tả**: API này thay đổi giá.
- **Response**:
```json
{
    "message": "Updated page price.",
    "status": "success"
}
```

### **Lấy danh sách các khiếu nại của người dùng**
- **Endpoint**: `{{base_url}}/spso/printer/issues`
- **Phương thức**: `GET`
- **Params**:
    - date_range (str): Optional. Date range for the issues. Can be 'daily', 'weekly', 'monthly'.
    - start_date (str): Optional. Start date for custom date range in 'YYYY-MM-DD' format.
    - end_date (str): Optional. End date for custom date range in 'YYYY-MM-DD' format.
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
    - Không có
- **Mô tả**: API này lấy danh sách khiếu nại dựa theo thông tin yêu cầu.
- **Response**:
```json
{
    "data": [
        {
            "date": "2024-11-28 22:31:59",
            "issue": "Out of order",
            "printer_id": "67488c8bbc7fecd8afe2e6f3",
            "student_id": "67488c7fbc7fecd8afe2e6f1"
        }
    ],
    "status": "success"
}
```

### **Thêm 1 thông tin bảo trì của máy in**
- **Endpoint**: `{{base_url}}/spso/printer/{printer_id}/maintenance`
- **Phương thức**: `PATCH`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
```json
{
    "spso_id": "67493a07daf6be88eb3818f0",
    "details": "test"
}
```
- **Mô tả**: API này thêm 1 thông tin bảo trì thông qua printer_id
- **Response**:
```json
{
    "message": "Updated maintenance history for printer 67488c8bbc7fecd8afe2e6f3.",
    "status": "success"
}
```

### **Lấy danh sách các thông tin bảo trì của máy in**
- **Endpoint**: `{{base_url}}/spso/printer/{printer_id}/maintenance_history`
- **Phương thức**: `GET`
- **Params**:
    - date_range (str): Optional. Date range for the issues. Can be 'daily', 'weekly', 'monthly'.
    - start_date (str): Optional. Start date for custom date range in 'YYYY-MM-DD' format.
    - end_date (str): Optional. End date for custom date range in 'YYYY-MM-DD' format.
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
    - Không có
- **Mô tả**: API này lấy danh sách thông tin bảo trì của printer_id dựa theo thông tin yêu cầu.
- **Response**:
```json
{
    "data": [
        {
            "date": "2024-12-01 18:54:46",
            "details": "test",
            "spso_id": "67493a07daf6be88eb3818f0"
        },
        {
            "date": "2024-12-04 08:26:08",
            "details": "test",
            "spso_id": "67493a07daf6be88eb3818f0"
        }
    ],
    "status": "success"
}
```

### **Lấy danh sách các thông tin người dùng dựa theo role**
- **Endpoint**: `{{base_url}}/spso/account`
- **Phương thức**: `GET`
- **Headers**:  
  - Role: Spso
  - Authorization: Access token
- **Body yêu cầu**:
```json
{
    "role": "student"
}
```
- **Mô tả**: API này lấy danh sách thông tin người dùng dựa theo role
- **Response**:
```json
{
    "data": [
        {
            "_id": "67488c7fbc7fecd8afe2e6f1",
            "email": "kennezversion@gmail.com",
            "paper_count": 518,
            "print_history": [
                {
                    "date": "2024-11-28 23:10:33",
                    "file_name": "Report",
                    "pages": 50,
                    "printer_id": "67488c8bbc7fecd8afe2e6f3"
                }
            ],
            "report_history": [
                {
                    "date": "2024-11-28 22:31:59",
                    "issue": "Out of order",
                    "printer_id": "67488c8bbc7fecd8afe2e6f3"
                }
            ],
            "role": "student"
        }
    ],
    "status": "success"
}
```

## **3. Student**

### **Báo cáo sự cố**
- **Endpoint**: `{{base_url}}/student/report_issue`
- **Phương thức**: `POST`
- **Headers**:  
  - Role: Student
  - Authorization: Access token
- **Body yêu cầu**:
```json
{
    "student_id": "67488c7fbc7fecd8afe2e6f1",
    "printer_id": "67488c8bbc7fecd8afe2e6f3",
    "issue": "Out of order"
}
```
- **Response**:
```json
{
    "message": "Reported issue for printer 67488c8bbc7fecd8afe2e6f3 by student 67488c7fbc7fecd8afe2e6f1.",
    "status": "success"
}
```
- **Mô tả**: API này cho phép sinh viên báo cáo sự cố liên quan đến máy in.

### **In tài liệu**
- **Endpoint**: `{{base_url}}/student/print_document`
- **Phương thức**: `POST`
- **Headers**:  
  - Role: Student
  - Authorization: Access token
- **Body yêu cầu**:
```json
{
    "student_id": "67488c7fbc7fecd8afe2e6f1",
    "printer_id": "67488c8bbc7fecd8afe2e6f3",
    "file_name": "Report",
    "page_count": 50
}
```
- **Response**:
```json
{
    "message": "Document printed successfully.",
    "status": "success"
}
```
- **Mô tả**: API này cho phép sinh viên gửi yêu cầu in tài liệu.

### **Tải danh sách máy in**
- **Endpoint**: `{{base_url}}/student/printer`
- **Phương thức**: `GET`
- **Headers**:  
  - Role: Student
  - Authorization: Access token
- **Body yêu cầu**:
    - Không có
- **Response**:
```json
[
    {
        "_id": "67488c8bbc7fecd8afe2e6f3",
        "ink": {
            "level": 60.625,
            "max_print_pages": 1600,
            "type": "Black"
        },
        "location": "Room 101",
        "maintenance_history": [
            {
                "date": "2024-12-01 18:54:46",
                "details": "test",
                "spso_id": "67493a07daf6be88eb3818f0"
            },
            {
                "date": "2024-12-04 08:26:08",
                "details": "test",
                "spso_id": "67493a07daf6be88eb3818f0"
            }
        ],
        "manufacturer": "HP",
        "model": "HP LaserJet 200",
        "name": "Printer A",
        "paper_count": 300,
        "print_history": [
            {
                "date": "2024-11-01 23:10:33",
                "file_name": "Report",
                "pages": 50,
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            },
            {
                "date": "2024-12-04 08:36:01",
                "file_name": "Report",
                "pages": 50,
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "purchase_date": "2024-01-15",
        "report_history": [
            {
                "date": "2024-11-28 22:31:59",
                "issue": "Out of order",
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            },
            {
                "date": "2024-12-04 08:33:17",
                "issue": "Out of order",
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "status": "Ready",
        "type": "Laser"
    },
    {
        "_id": "67495ce35fb7c916e6c35ce3",
        "paper_price": 200
    },
    {
        "_id": "674b2b0a04b739e03f4eac22",
        "ink": {
            "level": 70,
            "max_print_pages": 1600,
            "type": "Black"
        },
        "location": "Room 101",
        "maintenance_history": [],
        "manufacturer": "HP",
        "model": "HP LaserJet 200",
        "name": "Printer B",
        "paper_count": 500,
        "print_history": [
            {
                "date": "2024-11-28 23:10:33",
                "file_name": "Report",
                "pages": 50,
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "purchase_date": "2024-01-15",
        "report_history": [],
        "status": "Ready",
        "type": "Laser"
    }
]
```
- **Mô tả**: API này trả về danh sách máy in mà sinh viên có thể sử dụng.

### **Lây thông tin máy in theo id**
- **Endpoint**: `{{base_url}}/student/printer/{printer_id}`
- **Phương thức**: `GET`
- **Headers**:  
  - Role: Student
  - Authorization: Access token
- **Body yêu cầu**:
    - Không có
- **Response**:
```json
{
    "data": {
        "_id": "67488c8bbc7fecd8afe2e6f3",
        "ink": {
            "level": 60.625,
            "max_print_pages": 1600,
            "type": "Black"
        },
        "location": "Room 101",
        "maintenance_history": [
            {
                "date": "2024-12-01 18:54:46",
                "details": "test",
                "spso_id": "67493a07daf6be88eb3818f0"
            },
            {
                "date": "2024-12-04 08:26:08",
                "details": "test",
                "spso_id": "67493a07daf6be88eb3818f0"
            }
        ],
        "manufacturer": "HP",
        "model": "HP LaserJet 200",
        "name": "Printer A",
        "paper_count": 300,
        "print_history": [
            {
                "date": "2024-11-01 23:10:33",
                "file_name": "Report",
                "pages": 50,
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            },
            {
                "date": "2024-12-04 08:36:01",
                "file_name": "Report",
                "pages": 50,
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "purchase_date": "2024-01-15",
        "report_history": [
            {
                "date": "2024-11-28 22:31:59",
                "issue": "Out of order",
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            },
            {
                "date": "2024-12-04 08:33:17",
                "issue": "Out of order",
                "student_id": "67488c7fbc7fecd8afe2e6f1"
            }
        ],
        "status": "Ready",
        "type": "Laser"
    },
    "status": "success"
}
```
- **Mô tả**: API lấy thông tin máy in dựa theo printer_id

### **Thêm trang vào tài khoản student**
- **Endpoint**: `{{base_url}}/student/add_page`
- **Phương thức**: `POST`
- **Headers**:  
  - Role: Student
  - Authorization: Access token
- **Body yêu cầu**:
```json
{
    "student_id": "67488c7fbc7fecd8afe2e6f1",
    "page": 50
}
```
- **Response**:
```json
{
    "message": "Pages added successfully.",
    "status": "success"
}
```
- **Mô tả**: API này thêm số trang yêu cầu dựa vào student_id.

## **4. Payment**

### **Tạo thanh toán**
- **Endpoint**: `{{base_url}}/momo/create_payment`
- **Phương thức**: `POST`
- **Headers**:  
    - Không có
- **Body yêu cầu**:
```json
{
    "student_id": "67488c7fbc7fecd8afe2e6f1",
    "page": 10
}
```
- **Response**:
```json
{
    "payUrl": "https://test-payment.momo.vn/v2/gateway/pay?s=c538c94999a568cd37e4914b8f396a5f5dce6a5c0b073f9f1a16843cc7de2343&t=TU9NT3w2ZWRjOThlZi02YTM3LTQ3Y2ItOTM1YS05MzllMWRjZTcyNDU",
    "status": "success"
}
```
- **Mô tả**: API này sẽ chuyển hướng đến thanh toán momo 

### **Trạng thái thanh toán**
- **Endpoint**: `{{base_url}}/momo/callback`
- **Phương thức**: `GET`
- **Headers**:  
    - Không có
- **Body yêu cầu**:
    - Không có
- **Response**:
```json
{
    "status": "success",
    "message": "Transaction successful",
    "student_id": "67488c7fbc7fecd8afe2e6f1",
    "page": 10
}
```
- **Mô tả**: API này sẽ tự động gọi khi thanh toán thông qua momo thành công


