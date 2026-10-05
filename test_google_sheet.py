import requests

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzDjRiuUmnVQp-LXBgksgi-Qg4cjUlsDdyw_LTuwjDfycLX4Hkr1vPtSJFDWrRduA3seA/exec"
data = {
    "vehicle_number": "MH12AB1234"
}

response = requests.post(
    WEB_APP_URL,
    json=data,
    timeout=30
)

print("Status Code:", response.status_code)
print("Response:", response.text)