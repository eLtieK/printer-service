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
redirectUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
ipnUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
partnerName = "MoMo Payment"
storeId = "Printer Management"
lang = "vi"