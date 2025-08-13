from app import db

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(512), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    author_link = db.Column(db.String(512), nullable=False)
    camera_mark = db.Column(db.String(255), nullable=False)
    camera_model = db.Column(db.String(255), nullable=False)
    exposure_time = db.Column(db.String(50), nullable=False)
    aperture = db.Column(db.String(50), nullable=False)
    focal_length = db.Column(db.String(50), nullable=False)
    iso = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)