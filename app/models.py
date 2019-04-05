from app import db, login_manager
from sqlalchemy.orm import validates
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %r>" % self.username

    @validates("name", "username", "email")
    def convert_upper(self, key, value):
        return value.lower()

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Penerbangan(db.Model):
    __tablename__ = "penerbangan"
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(80), nullable=False)
    pesawat = db.Column(db.Integer, db.ForeignKey("maskapai.id"))
    tujuan = db.Column(db.String(140), nullable=False)
    jam = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    gate = db.Column(db.String(140), nullable=False)
    status = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Kode %r>" % self.kode

    @validates("kode", "tujuan", "status")
    def convert_upper(self, key, value):
        return value.upper()

    def to_json(self):
        obj = {
            "id": self.id,
            "kode": self.kode,
            "pesawat": self.pesawat,
            "tujuan": self.tujuan,
            "jam": self.jam,
            "gate": self.gate,
            "status": self.status,
        }
        return obj

    @staticmethod
    def from_json(json_data):
        body = json_data.get("body")
        if body is None or body == "":
            raise ValidationError("post doesnt have body.")
        return Penerbangan(body=body)


class Maskapai(db.Model):
    __tablename__ = "maskapai"
    id = db.Column(db.Integer, primary_key=True)
    maskapai = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False)
    penerbangan = db.relationship("Penerbangan", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Maskapai %r>" % self.maskapai

    @validates("maskapai")
    def convert_upper(self, key, value):
        return value.upper()

    def to_json(self):
        obj = {"id": self.id, "maskapai": self.id}
        return obj


def options_maskapai():
    return Maskapai.query.all()
