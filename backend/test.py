import vk_api
import requests
import json
res = requests.get("https://api.vk.com/method/photos.getWallUploadServer?access_token=vk1.a.ssfe8NTR57rT4WiHQAfjNaUg0GayVrwzufXqRgFTou935loa2zLZ0pwH1cQ6zlS9Z4mAMNDf4Df8gv-SCSRhTkFq5TkuJSprACdTMOAPnJqVKK8QywRLVXLNhtq68gBIeWy_CmBMZEc2UwIrkHTN-FrhIyyB2-zTzArW1PMRP2adBTmOw-rQrQu1IFyFxcpU&v=5.131")
print(res.json())
url = res.json()["response"]["upload_url"]
user = res.json()["response"]["user_id"]
import base64
import os
import requests

with open("./short_stats.png", 'rb') as img:
  name_img= os.path.basename("./short_stats.png")
  files= {'photo': (name_img,img,'multipart/form-data',{'Expires': '0'}) }
  with requests.Session() as s:
    r = s.post(url, files=files)
    print(r.json())

print(json.loads(r.json()["photo"]))
res2 = requests.post("https://api.vk.com/method/photos.saveWallPhoto?access_token=vk1.a.ssfe8NTR57rT4WiHQAfjNaUg0GayVrwzufXqRgFTou935loa2zLZ0pwH1cQ6zlS9Z4mAMNDf4Df8gv-SCSRhTkFq5TkuJSprACdTMOAPnJqVKK8QywRLVXLNhtq68gBIeWy_CmBMZEc2UwIrkHTN-FrhIyyB2-zTzArW1PMRP2adBTmOw-rQrQu1IFyFxcpU&v=5.131&photo="+r.json()["photo"]+"&server="+str(r.json()["server"])+"&hash="+str(r.json()["hash"])+"&user_id="+str(user))

print(res2.json())


res3 = requests.post("https://api.vk.com/method/wall.post?access_token=vk1.a.ULwfH0bK9ni50QougzG6vJV_dZ_32J8ewdTCsh34tkL9DsZgpdbhaf68KAAoXHBC2uBJevs2bvE6mHRx5DTAj54uTB9n-uqB6Gw6M25yMF8bNCj8aV2vbdTHhvXl6e5rOHkWq6gyd0mu4mR10LxfpsHqyT95YlE92JpDjJc691oH-Hh0cJiVap3c_Ia4q06Fzv8WMIgo8teMKmfkNklAsg&v=5.131"+"&attachment="+','.join('photo{owner_id}_{id}'.format(**item) for item in res2.json()["response"])+"&owner_id="+str(user)+"&message=" + 'test')

print(res3.json())
# with open("./short_stats.png", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())
# req = requests.post(url, data=, headers={
#       'Content-Type': 'multipart/form-data'
#     })
# print(req.json())
# vk_session = vk_api.VkApi(token="vk1.a.ssfe8NTR57rT4WiHQAfjNaUg0GayVrwzufXqRgFTou935loa2zLZ0pwH1cQ6zlS9Z4mAMNDf4Df8gv-SCSRhTkFq5TkuJSprACdTMOAPnJqVKK8QywRLVXLNhtq68gBIeWy_CmBMZEc2UwIrkHTN-FrhIyyB2-zTzArW1PMRP2adBTmOw-rQrQu1IFyFxcpU")
# vk_session.auth(token_only=True)
#
# vk = vk_session.get_api()
#
# print(vk.wall.post(message='Hello world!'))