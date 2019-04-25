from ..models import Penerbangan, Maskapai, User
from . import admin
from .forms import FormPenerbangan, FormMaskapai, FormUser, FormUserEdit
from app import db
from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    make_response,
    abort,
    request,
)
from datetime import datetime
from slugify import slugify
from flask_login import login_required
from ..email import send_email


@admin.route("/")
@login_required
def dashboard():
    user = User.query.count()
    maskapai = Maskapai.query.count()
    penerbangan = Penerbangan.query.count()
    return render_template(
        "dashboard.html", user=user, maskapai=maskapai, penerbangan=penerbangan
    )


@admin.route("/penerbangan")
@login_required
def lihat_penerbangan():
    data = (
        db.session.query(
            Penerbangan.kode,
            Maskapai.maskapai,
            Penerbangan.asal,
            Penerbangan.tujuan,
            Penerbangan.gate,
            Penerbangan.status,
            Penerbangan.waktu_keberangkatan,
            Penerbangan.waktu_kedatangan,
        )
        .join(Maskapai, Penerbangan.pesawat == Maskapai.id)
        .all()
    )
    return render_template("lihat_penerbangan.html", data=data)


@admin.route("/penerbangan/baru", methods=["GET", "POST"])
@login_required
def tambah_penerbangan():
    form = FormPenerbangan()
    if form.validate_on_submit():
        data = Penerbangan(
            kode=form.kode.data,
            pesawat=form.pesawat.data.id,
            asal=form.asal.data,
            tujuan=form.tujuan.data,
            waktu_keberangkatan=form.waktu_keberangkatan.data,
            waktu_kedatangan=form.waktu_kedatangan.data,
            gate=form.gate.data,
            status=form.status.data,
            slug=slugify(form.kode.data),
        )
        db.session.add(data)
        db.session.commit()
        flash("Data Tersimpan!")
        return redirect(url_for("admin.lihat_penerbangan"))
    return render_template("tambah_penerbangan.html", form=form)


@admin.route("/maskapai", methods=["GET", "POST"])
@login_required
def lihat_maskapai():
    data = Maskapai.query.all()
    form = FormMaskapai()
    if form.validate_on_submit():
        data = Maskapai(maskapai=form.maskapai.data, slug=slugify(form.maskapai.data))
        db.session.add(data)
        db.session.commit()
        flash("Data Tersimpan!")
        return redirect(url_for("admin.lihat_maskapai"))
    return render_template("lihat_maskapai.html", data=data, form=form)


@admin.route("/maskapai/edit/<string:slug>", methods=["GET", "POST"])
@login_required
def edit_maskapai(slug):
    form = FormMaskapai()
    data = Maskapai.query.all()
    edit = Maskapai.query.filter_by(slug=slug).first()
    if form.validate_on_submit():
        edit.maskapai = form.maskapai.data
        db.session.commit()
        flash("Data Tersimpan!")
        return redirect(url_for("admin.lihat_maskapai"))
    form.maskapai.data = edit.maskapai
    return render_template("lihat_maskapai.html", form=form, data=data)


@admin.route("/user")
@login_required
def lihat_user():
    data = User.query.all()
    return render_template("lihat_user.html", data=data)


@admin.route("/user/baru", methods=["GET", "POST"])
@login_required
def tambah_user():
    form = FormUser()
    if form.validate_on_submit():
        data = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(data)
        db.session.commit()
        token = data.generate_confirmation_token()
        html = render_template(
            "mail/confirm.html", data=data, datetime=datetime.utcnow(), token=token
        )
        send_email(data.email, "Konfirmasi Akun", html)
        flash("Data Tersimpan!")
        return redirect(url_for("admin.lihat_user"))
    return render_template("tambah_user.html", form=form)


@admin.route("/user/<string:username>", methods=["GET", "POST"])
@login_required
def edit_user(username):
    form = FormUserEdit()
    edit = User.query.filter_by(username=username).first()
    if form.validate_on_submit():
        edit.name = (form.name.data,)
        edit.username = (form.username.data,)
        edit.email = (form.email.data,)
        edit.password = (form.password.data,)
        db.session.commit()
        flash("Data Tersimpan!")
        return redirect(url_for("admin.lihat_user"))
    form.name.data = edit.name
    form.username.data = edit.username
    form.email.data = edit.email
    return render_template("edit_user.html", form=form)


@admin.route("/dokumentasi-api")
@login_required
def api_documentation():
    return render_template("dokumentasi_api.html")

