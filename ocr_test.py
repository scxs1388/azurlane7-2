import base64
import os
import sys

import requests

filepath = "2021-02-19-08-47-03_item_2.png"

f = open(os.path.join(r"D:\Programming\Codefiles\pythonfiles\azurlane7-2\image", filepath), "rb")
img = base64.b64encode(f.read())

client_id = "06FmxtlHldli2NnjHAkf0IfG"
client_secret = "g0QPfDM8FKbDrmULSPDq49MHxKhQORWD"

url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
response = requests.get(url)
if response:
    access_token = (response.json()["access_token"])

host = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token={access_token}"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "image": img
}
res = requests.post(url=host, headers=headers, data=data)
list = res.json()["words_result"]

for i in list:
    print(i["words"])
