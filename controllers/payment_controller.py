import hashlib
import hmac
import uuid
import requests
from config import momo
from flask import jsonify
from controllers.spso.printer_controller import get_paper_price
from controllers.student_controller import add_page

def ipn_listener(query_params):
    try:
        # Kiểm tra trạng thái giao dịch
        result_code = query_params.get("resultCode")
        extra_data = query_params.get("extraData")
        student_id, page = extra_data.split()

        if result_code == "0":  # Giao dịch thành công
            #return add_page(student_id, int(page))
            return jsonify({
                "status": "success",
                "message": "Transaction successful",
                "student_id": student_id,
                "page": page
            }), 200
        else:  # Giao dịch thất bại
            return jsonify({"status": "error", "message": "Payment failed"}), 400

    except Exception as e:
        print(f"Error processing IPN: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    
def generate_signature(data, secret_key):
    raw_signature = "&".join([f"{key}={data[key]}" for key in sorted(data.keys())])
    h = hmac.new(bytes(secret_key, 'ascii'), bytes(raw_signature, 'ascii'), hashlib.sha256)
    return h.hexdigest()

def create_payment(payment_data):
    try:
        # Extract payment details from request body
        order_info = payment_data.get("orderInfo", "Pay for papers")
        request_type = payment_data.get("requestType", "payWithMethod")
        auto_capture = payment_data.get("autoCapture", True)
        student_id = payment_data.get("student_id")
        page = int(payment_data.get("page"))

        # amount min la 1000, neu thap hon thi payment ko chap nhan
        amount = str(get_paper_price() * int(page))

        # Generate unique identifiers
        order_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())

        # Prepare raw data for signature
        raw_data = {
            "accessKey": momo.accessKey,
            "amount": amount,
            "extraData": f"{student_id} {page}",
            "ipnUrl": momo.ipnUrl,
            "orderId": order_id,
            "orderInfo": order_info,
            "partnerCode": momo.partnerCode,
            "redirectUrl": momo.redirectUrl,
            "requestId": request_id,
            "requestType": request_type
        }

        # Generate signature
        signature = generate_signature(raw_data, momo.secretKey)

        # Prepare final data payload
        payload = {
            "partnerCode": momo.partnerCode,
            "orderId": order_id,
            "partnerName": momo.partnerName,
            "storeId": momo.storeId,
            "ipnUrl": momo.ipnUrl,
            "amount": amount,
            "lang": momo.lang,
            "requestType": request_type,
            "redirectUrl": momo.redirectUrl,
            "autoCapture": auto_capture,
            "orderInfo": order_info,
            "requestId": request_id,
            "extraData": f"{student_id} {page}",
            "signature": signature
        }
    
        # Make request to MoMo API
        response = requests.post(momo.endpoint, json=payload, headers={'Content-Type': 'application/json'})

        response_data = response.json()

        # Redirect user to MoMo payment page
        if response_data.get("payUrl"):
            return jsonify({
                "status": "success",
                "payUrl": response_data["payUrl"]  # Send the payUrl back to the client
            })

        # Handle errors from MoMo API
        return jsonify({
            "status": "error",
            "message": response_data.get("message", "Failed to create payment.")
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500