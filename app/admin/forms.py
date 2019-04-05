from ..models import Penerbangan, Maskapai, User, options_maskapai
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateTimeField, PasswordField
from wtforms.validators import (
    DataRequired,
    ValidationError,
    Length,
    Regexp,
    EqualTo,
    Email,
)
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class FormPenerbangan(FlaskForm):
    kode = StringField(
        u"Kode Penerbangan", validators=[DataRequired(), Length(min=5, max=5)]
    )
    pesawat = QuerySelectField(
        u"Maskapai",
        validators=[DataRequired()],
        query_factory=options_maskapai,
        allow_blank=True,
        get_label="maskapai",
        get_pk=lambda x: x.id,
        blank_text=(u"Pilih Maskapai"),
    )
    tujuan = StringField(u"Tujuan", validators=[DataRequired(), Length(min=7, max=7)])
    jam = DateField(u"Tanggal Keberangkatan")
    gate = SelectField(
        u"Gate", choices=[("01", "01"), ("02", "02"), ("03", "03"), ("04", "04")]
    )
    status = SelectField(
        u"Status",
        choices=[
            ("check in", "CHECK IN"),
            ("to waiting room", "TO WAITING ROOM"),
            ("landing", "LANDING"),
            ("take off", "TAKE OFF"),
        ],
    )
    submit = SubmitField(u"Simpan")

    def validate_kode(self, kode):
        kode = Penerbangan.query.filter_by(kode=kode.data).first()
        if kode is not None:
            raise ValidationError("kode sudah ada, gunakan kode lain!")


class FormMaskapai(FlaskForm):
    maskapai = StringField(
        u"Nama Maskapai", validators=[DataRequired(), Length(min=5, max=25)]
    )
    submit = SubmitField(u"Simpan")

    def validate_maskapai(self, maskapai):
        maskapai = Maskapai.query.filter_by(maskapai=maskapai.data.upper()).first()
        if maskapai is not None:
            raise ValidationError("maskapai sudah ada!")


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


class FormUserEdit(FormUser):
    oldpassword = PasswordField(
        "Password Lama", validators=[DataRequired(), Length(6, 45)]
    )
