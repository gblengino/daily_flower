import requests
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, session
from sqlalchemy import desc
from datetime import date

app = Flask(__name__)

app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://root@localhost/db_flores")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Photo

url = "https://api.unsplash.com/photos/random"
params = {
    "collections": "b95eewkShSI", 
    "client_id": "H0sT_KBtghBprAlJPc_m6N5VbgmlMUsN260o5YcDkrY",
}

@app.route('/')
def index():

    last_flower = Photo.query.order_by(Photo.date.desc()).first()
    today = date.today()

    campos_exif = {
    "camera_mark": "make",
    "camera_model": "model",
    "exposure_time": "exposure_time",
    "aperture": "aperture",
    "focal_length": "focal_length",
    "iso": "iso"
    }

    if  not last_flower or last_flower.date != today:

        data_flower = requests.get(url, params=params).json()

            # Obtenemos el diccionario 'exif' de forma segura
        exif = data_flower.get("exif", {})

        # Creamos un diccionario con valores o "No especificado" si están vacíos
        datos_exif = {
            campo: exif.get(clave, "No especificado") or "No especificado"
            for campo, clave in campos_exif.items()
        }

        daily_photo = Photo(    
            img_url = data_flower['urls']['regular'],
            author = data_flower['user']['name'],
            author_link = data_flower['user']['links']['html'],
            date = date.today(),
            **datos_exif,
        )

        db.session.add(daily_photo)
        db.session.commit()
        print('Nueva foto cargada a la db!')
        last_flower = Photo.query.order_by(Photo.date.desc()).first()

    return render_template('index.html',
                           flower = last_flower,
                           today = today)

@app.route('/tests')
def tests():
    data_flower = requests.get(url, params=params).json()

    return data_flower