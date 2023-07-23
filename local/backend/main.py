import locale
import requests
import datetime
import smtplib
from sanic_cors import CORS
from sanic import Sanic, Request
from sanic.response import json, raw, empty
from goprocam import GoProCamera
from goprocam import constants
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
from PIL import Image

import settings

gopro = GoProCamera.GoPro()
locale.setlocale(locale.LC_TIME, "de_DE")
app = Sanic("photobox-api")
CORS(app)


@app.post(uri="/foto")
async def foto_erstellen(request: Request):
    name = str(int(datetime.datetime.now().timestamp()))
    gopro.take_photo()
    print(gopro.getMedia())
    bild = requests.get(gopro.getMedia())
    Image.open(BytesIO(bild.content)).save(settings.fotos_path+"/"+name+".jpg", format="jpeg")
    return json({"id": "0"})


@app.post(uri="/teilen")
async def foto_teilen(request: Request):
    if request.json.get("methode") == "qr":
        response = requests.post(settings.FileHost.url, headers={"Authorization": settings.FileHost.key}, data=open(settings.fotos_path+"/"+request.json.get("id")+".jpg", "rb").read())
        print(response.json())
        return json({"url": response.json().get("qr-url")})

    if request.json.get("methode") == "email":
        response = requests.post(settings.FileHost.url, headers={"Authorization": settings.FileHost.key}, data=open(settings.fotos_path + "/" + request.json.get("id") + ".jpg", "rb").read())

        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(f"""<!DOCTYPE html>
<html>
    <p>Hier ist die Fotobox.</p>
    <p>Im Anhang finden Sie Ihr Bild, alternativ können Sie es über <a href="{response.json().get('url')}">diesen Link</a> herunterladen.</p>
    <p>Schönen Tag.</p>
</html>""", "html"))

        with open(settings.fotos_path+"/"+request.json.get("id")+".jpg", 'rb') as image_file:
            msg.attach(MIMEImage(image_file.read()))

        msg["Subject"] = "Ihr Bild - Fotobox"
        msg["From"] = settings.Mail.smtp_mail
        msg["To"] = request.json.get("mail")

        server = smtplib.SMTP_SSL(settings.Mail.smtp_server, settings.Mail.smtp_port)
        server.login(settings.Mail.smtp_mail, settings.Mail.smtp_passwd)
        server.send_message(msg)
        server.quit()

        return empty()

app.static("/fotos/", settings.fotos_path, name="fotos")

if __name__ == "__main__":
    app.run(port=8001)
