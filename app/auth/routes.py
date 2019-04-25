from ..models import User
from . import auth
from app import db
from .forms import RegistrationForm, LoginForm
from ..email import send_email
from flask import Flask, render_template, redirect, flash, url_for, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime


@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated
        and not current_user.confirmed
        and request.blueprint != "auth"
        and request.endpoint != "static"
    ):
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
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
        flash("Berhasil Registrasi. Cek email anda untuk konfirmasi.")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("admin.dashboard")
            return redirect(next)
        flash("username atau password salah.")
    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Berhasil logout.")
    return redirect(url_for("auth.login"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("auth.login"))
    return render_template("unconfirmed.html")


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("admin.dashboard"))
    if current_user.confirm(token):
        db.session.commit()
        flash("Akun sudah terkonfirmasi, silahkan login.")
    else:
        flash("Link konfirmasi invalid atau sudah tidak berlaku")
    return redirect(url_for("admin.dashboard"))


@auth.route("confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    html = render_template(
        "mail/confirm.html", data=current_user, datetime=datetime.utcnow(), token=token
    )
    send_email(current_user.email, "Konfirmasi Ulang Akun", html)
    flash("Email konfirmasi ulang telah berhasil terkirim.")
    return redirect(url_for("auth.login"))
