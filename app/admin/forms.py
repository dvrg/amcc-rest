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
from wtforms.fields.html5 import DateField, DateTimeField, DateTimeLocalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from datetime import datetime
from flask_babel import lazy_gettext as _l


class FormPenerbangan(FlaskForm):
    kode = StringField(
        _l(u"Kode Penerbangan", validators=[DataRequired(), Length(min=5, max=5)])
    )
    pesawat = QuerySelectField(
        _l(
            u"Maskapai",
            validators=[DataRequired()],
            query_factory=options_maskapai,
            allow_blank=True,
            get_label="maskapai",
            get_pk=lambda x: x.id,
            blank_text=(u"Pilih Maskapai"),
        )
    )
    asal = StringField(_l(u"Asal", validators=[DataRequired(), Length(min=3, max=20)]))
    tujuan = StringField(
        _l(u"Tujuan", validators=[DataRequired(), Length(min=3, max=20)])
    )
    waktu_keberangkatan = DateTimeLocalField(
        _l(
            u"Waktu Keberangkatan",
            format="%Y-%m-%dT%H:%M:%S",
            default=datetime.today(),
            validators=[DataRequired()],
        )
    )
    waktu_kedatangan = DateTimeLocalField(
        _l(
            u"Waktu Kedatangan",
            format="%Y-%m-%dT%H:%M:%S",
            default=datetime.today(),
            validators=[DataRequired()],
        )
    )
    gate = SelectField(
        _l(u"Gate", choices=[("01", "01"), ("02", "02"), ("03", "03"), ("04", "04")])
    )
    status = SelectField(
        _l(
            u"Status",
            choices=[
                ("check in", "CHECK IN"),
                ("to waiting room", "TO WAITING ROOM"),
                ("landing", "LANDING"),
                ("take off", "TAKE OFF"),
            ],
        )
    )
    submit = SubmitField(_l(u"Simpan"))

    def validate_kode(self, kode):
        kode = Penerbangan.query.filter_by(kode=kode.data).first()
        if kode is not None:
            raise ValidationError("kode sudah ada, gunakan kode lain!")


class FormMaskapai(FlaskForm):
    maskapai = StringField(
        _l(u"Nama Maskapai", validators=[DataRequired(), Length(min=5, max=25)])
    )
    submit = SubmitField(_l(u"Simpan"))

    def validate_maskapai(self, maskapai):
        maskapai = Maskapai.query.filter_by(maskapai=maskapai.data.upper()).first()
        if maskapai is not None:
            raise ValidationError("maskapai sudah ada!")


class FormUser(FlaskForm):
    name = StringField(_l("Nama", validators=[DataRequired(), Length(3, 45)]))
    username = StringField(
        _l(
            "Username",
            validators=[
                DataRequired(),
                Length(3, 45),
                Regexp(r"^\w+$", message="Tidak boleh ada spasi dan spesial karakter."),
            ],
        )
    )
    email = StringField(
        _l("Email", validators=[DataRequired(), Email(), Length(1, 64)])
    )
    password = PasswordField(
        _l(
            "Password",
            validators=[
                DataRequired(),
                Length(6, 45),
                EqualTo("confirm", message="Password tidak cocok!"),
            ],
        )
    )
    confirm = PasswordField(
        _l("Konfirmasi Password", validators=[DataRequired(), Length(6, 45)])
    )
    submit = SubmitField(_l("Simpan"))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Email sudah terdaftar.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError("Username sudah digunakan.")


class FormUserEdit(FormUser):
    oldpassword = PasswordField(
        _l("Password Lama", validators=[DataRequired(), Length(6, 45)])
    )
