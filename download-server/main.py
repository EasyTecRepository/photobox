import random
import string
from json import loads
from sanic import Sanic, Request
from sanic.response import file, html
from sanic.exceptions import BadRequest, Unauthorized
from sanic_cors import CORS
from hashlib import sha256
from os import listdir
from PIL import Image
from io import BytesIO
from qrcode import QRCode, constants


def load_config():
    with open("config.json", "r") as cfg:
        return loads(cfg.read())


app = Sanic(__name__)
CORS(app)
config = load_config()


@app.post(uri="/create")
async def create_photo(rq: Request):
    if not rq.headers or not rq.body:
        raise BadRequest()

    if not rq.headers.get("Authorization") or sha256(
            rq.headers.get("Authorization").encode("UTF-8")).hexdigest() != config.get("token_hash"):
        raise Unauthorized()

    while True:
        code = "".join(random.choice(string.ascii_letters) for x in range(10))
        if code not in listdir(config.get("photo_dir")):
            break

    print(rq.content_type)
    img = Image.open(BytesIO(rq.body))
    img.save(f"{config.get('photo_dir')}/{code}", format="jpeg")

    url = f"{'https' if config.get('ssl').get('enabled') else 'http'}://{config.get('host')}/download?id=" + code

    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr.make_image(fill_color="black", back_color="white").save(f"{config.get('qr_dir')}/{code}.png")

    return await file(location=f"{config.get('qr_dir')}/{code}.png")


@app.get(uri="/foto")
async def get_photo(rq: Request):
    if not rq.args:
        raise BadRequest()

    if rq.args.get("id") not in listdir(config.get('photo_dir')):
        raise BadRequest()

    return await file(f"{config.get('photo_dir')}/{rq.args.get('id')}", mime_type="image/jpeg")


@app.get(uri="/download")
async def get_downlaod_page(rq: Request):
    if not rq.args:
        raise BadRequest()

    if rq.args.get("id") not in listdir(config.get('photo_dir')):
        raise BadRequest()

    html_site = """
    <!DOCTYPE html>
<html>
<head>
  <title>Herunterladen Ihres Bildes</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.19.2/axios.min.js"></script>
</head>
<body>
  <img id="preview" src="//" width="500" />
  <br>
  <button id="download_btn" onclick="download()">Herunterladen</button>
  <script>
    var id = getQueryVariable("id");
    console.log(id);
    var image = document.getElementById("preview");
    image.src = `http://127.0.0.1:8000/foto?id=${id}`;

    function download() {
      axios({
        url: `http://127.0.0.1:8000/foto?id=${id}`,
        method: 'GET',
        responseType: 'blob'
      })
        .then((response) => {
          const url = window.URL
            .createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'Fotobox.jpg');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        })
    }
    function getQueryVariable(variable) {
      var query = window.location.search.substring(1);
      var vars = query.split("&");
      for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
          return pair[1];
        }
      }
      return null;
    }
  </script>
  <style>
    body {
      background-color: darkgrey;
      text-align: center;
    }

    img {
      border-radius: 15px;
    }
    button {
      font-size: 40px;
      font-family: Arial, Helvetica, sans-serif;
    }
  </style>
</body>
</html>
    """
    return html(html_site)


if "__main__" == __name__:
    app.run(host=config.get("host"), port=config.get("port") if config.get("ssl").get("enabled") else 80, ssl=config.get('ssl') if config.get("ssl").get("enabled") else None)
