import json
import uuid
import requests
import hmac
import hashlib

# parameters send to MoMo get get payUrl
endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
accessKey = "F8BBA842ECF85"
secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
partnerCode = "MOMO"
redirectUrl = "http://localhost:5000/momo/callback"
ipnUrl = "http://localhost:5000/momo/callback"
partnerName = "MoMo Payment"
storeId = "Printer Management"
lang = "vi"
orderGroupId = ""