from bson import ObjectId


def convert_objectid_to_string(data):
    """
    Duyệt qua tất cả các trường trong đối tượng và chuyển ObjectId thành chuỗi.
    """
    if isinstance(data, dict):  # Nếu data là dictionary
        return {key: convert_objectid_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):  # Nếu data là list
        return [convert_objectid_to_string(item) for item in data]
    elif isinstance(data, ObjectId):  # Nếu là ObjectId
        return str(data)  # Chuyển ObjectId thành string
    return data  # Nếu không phải kiểu ObjectId thì giữ nguyên