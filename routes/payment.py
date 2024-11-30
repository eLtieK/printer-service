import json
import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from controllers import payment_controller
from middlewares.auth import student_is_required, login_is_required
import pathlib

load_dotenv(dotenv_path= pathlib.Path(__file__).parent.parent / '.env')
PAYMENT_PREFIX = os.getenv('PAYMENT_PREFIX')

payment_tuple = (Blueprint('payment_tuple', __name__), f'/{PAYMENT_PREFIX}')
payment_route, prefix_route = payment_tuple
CORS(payment_route, supports_credentials=True, origins=["http://localhost:3000"])

@payment_route.route('/payment')
def payment():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Payment</title>
            <script>
                function sendPayment() {
                    const data = {
                        student_id: "67488c7fbc7fecd8afe2e6f1",
                        page: 4,  // Gửi amount
                        orderInfo: "Pay for pages"  // Gửi order info
                    };

                    fetch('/momo/create_payment', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'  // Gửi dữ liệu dưới dạng JSON
                        },
                        body: JSON.stringify(data)  // Chuyển đối tượng JavaScript thành JSON
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);  // Xử lý dữ liệu trả về từ server
                        if (data.payUrl) {
                            window.location.href = data.payUrl;  // Chuyển hướng đến trang MoMo
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                }
            </script>
        </head>
        <body>
            <h2>Pay with MoMo</h2>
            <button onclick="sendPayment()">Pay Now</button>
        </body>
        </html>
    """

@payment_route.route('/create_payment', methods=['POST'])
# @login_is_required
# @student_is_required
def create_payment():
    data = request.get_json()

    return payment_controller.create_payment(data)

@payment_route.route('/callback', methods=['GET'])
# @login_is_required
# @student_is_required
def callback():
    # Lấy các tham số từ query string
    query_params = request.args.to_dict()
    # response = requests.post(
    #     "http://localhost:5000/add_page",
    #     json={"student_id": query_params.get("orderId"), "page": query_params.get("amount")}
    # )
    return payment_controller.ipn_listener(query_params)