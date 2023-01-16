from flask import Flask, request, send_file
from flask_cors import CORS
import json
import os
import requests
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def hello():
    print("hello")
    return "Hello very World!"


@app.route("/save-image", methods=["POST", "PUT"])
def save_image():
    file_name = request.json["name"]
    file_content = request.json["file"]
    file_type = request.json["type"]
    with open('/backend/'+file_name+'.'+file_type.split('/')[-1], "wb") as fh:
        fh.write(base64.urlsafe_b64decode(file_content))
    return {"response": 'ok', "code": 200}, 200


@app.route("/image", methods=["GET"])
def return_image():
    file_name = request.args["name"]
    file_type = request.args["type"]
    return send_file(file_name+'.'+file_type.split('/')[-1])


@app.route("/post-image", methods=["POST"])
def post_image():
    file_name = request.args["name"]
    file_type = request.args["type"]
    access_token = request.args["token"]
    res = requests.get(
        f"https://api.vk.com/method/photos.getWallUploadServer?access_token={access_token}&v=5.131")
    print(res.json())
    url = res.json()["response"]["upload_url"]
    user = res.json()["response"]["user_id"]
    with open("/backend/"+file_name+'.'+file_type.split('/')[-1], 'rb') as img:
        name_img = os.path.basename("/backend/"+file_name+'.'+file_type.split('/')[-1])
        files = {'photo': (name_img, img, 'multipart/form-data', {'Expires': '0'})}
        with requests.Session() as s:
            r = s.post(url, files=files)
            print(r.json())

    print(json.loads(r.json()["photo"]))
    res2 = requests.post(
        f"https://api.vk.com/method/photos.saveWallPhoto?access_token={access_token}&v=5.131&photo=" +
        r.json()["photo"] + "&server=" + str(r.json()["server"]) + "&hash=" + str(r.json()["hash"]) + "&user_id=" + str(
            user))

    print(res2.json())

    res3 = requests.post(
        f"https://api.vk.com/method/wall.post?access_token={access_token}&v=5.131" + "&attachment=" + ','.join(
            'photo{owner_id}_{id}'.format(**item) for item in res2.json()["response"]) + "&owner_id=" + str(
            user) + "&message=" + 'test')

    print(res3.json())
    return {"getserver": res.json(), 'photo': r.json(), 'savephotos': res2.json(), 'post': res3.json(), "code": 200}, 200


if __name__ == "__main__":
    app.run()
