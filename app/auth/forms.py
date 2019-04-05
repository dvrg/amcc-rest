from ..models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, PasswordField, BooleanField
from wtforms.validators import (
    DataRequired,
    ValidationError,
    Length,
    Regexp,
    EqualTo,
    Email,
)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u"Password", validators=[DataRequired(), Length(6, 45)])
    remember_me = BooleanField(u"Tetap Login")
    submit = SubmitField("Login")


class FormUser(FlaskForm):
    name = StringField("Nama", validators=[DataRequired(), Length(3, 45)])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(3, 45),
            Regexp(r"^\w+$", message="Tidak boleh ada spasi dan spesial karakter."),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(6, 45),
            EqualTo("confirm", message="Password tidak cocok!"),
        ],
    )
    confirm = PasswordField(
        "Konfirmasi Password", validators=[DataRequired(), Length(6, 45)]
    )
    submit = SubmitField("Simpan")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Email sudah terdaftar.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError("Username sudah digunakan.")

