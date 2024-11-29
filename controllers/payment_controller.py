import hashlib
import hmac
import uuid
import requests
from config import momo
from flask import jsonify, redirect, request

def verify_signature(data, secret_key, signature):
    raw_signature = "&".join([f"{key}={data[key]}" for key in sorted(data.keys()) if key != "signature"])
    h = hmac.new(bytes(secret_key, 'ascii'), bytes(raw_signature, 'ascii'), hashlib.sha256)
    return h.hexdigest() == signature

def ipn_listener():
    try:
        # Nhận dữ liệu từ MoMo
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        signature = data.pop("signature", None)

        # Kiểm tra chữ ký (đảm bảo rằng thông báo là từ MoMo)
        if not verify_signature(data, momo.secretKey, signature):
            return jsonify({"status": "error", "message": "Invalid signature"}), 400

        # Kiểm tra trạng thái giao dịch
        result_code = data.get("resultCode")
        order_id = data.get("orderId")

        if result_code == 0:  # Giao dịch thành công
            # Cập nhật trạng thái giao dịch trong database
            print(f"Payment successful for order {order_id}")
            # Ví dụ: cập nhật trạng thái order trong database
            # update_order_status(order_id, status="PAID")
            return jsonify({"status": "success", "message": "Payment confirmed"}), 200
        else:  # Giao dịch thất bại
            print(f"Payment failed for order {order_id} with resultCode {result_code}")
            # Ví dụ: cập nhật trạng thái order trong database
            # update_order_status(order_id, status="FAILED")
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
        amount = str(payment_data.get("amount", "50000"))
        order_info = payment_data.get("orderInfo", "Pay for papers")
        request_type = payment_data.get("requestType", "payWithMethod")
        auto_capture = payment_data.get("autoCapture", True)

        # Generate unique identifiers
        order_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())

        # Prepare raw data for signature
        raw_data = {
            "accessKey": momo.accessKey,
            "amount": amount,
            "extraData": "",
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
            "extraData": "",
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