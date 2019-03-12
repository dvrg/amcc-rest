import os
from flask import Flask, render_template, redirect, flash, url_for, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateTimeField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)

#config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

class FormData(FlaskForm):
    kode = StringField(u'Kode Penerbangan', validators=[DataRequired()])
    pesawat = StringField(u'Nama Maskapai', validators=[DataRequired()])
    tujuan = StringField(u'Tujuan', validators=[DataRequired()])
    #jam = DateField(u'Jam Berangkat')
    gate = StringField(u'Gate', validators=[DataRequired()])
    status = SelectField(u'Status', choices=[('check in', 'check in'), ('to waiting room', 'to waiting room'), ('landing', 'landing'), ('take off', 'take off')])
    submit = SubmitField(u'Simpan')

class Pesawat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(80), nullable=False)
    pesawat = db.Column(db.String(80), nullable=False)
    tujuan = db.Column(db.String(140), nullable=False)
    jam = db.Column(db.String(), nullable=False, default=datetime.now())
    gate = db.Column(db.String(140), nullable=False)
    status = db.Column(db.String(140), nullable=False)

    def __repr__(self):
        return '<Kode %r>' % self.kode

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tambah-data', methods=['GET', 'POST'])
def tambah():
    form = FormData()
    if form.validate_on_submit():
        data = Pesawat(kode=form.kode.data, pesawat=form.pesawat.data, tujuan=form.tujuan.data, gate=form.gate.data, status=form.status.data)
        db.session.add(data)
        db.session.commit()
        flash('Data Tersimpan!')
        return redirect(url_for('lihat'))
    return render_template('add.html', form=form)

@app.route('/')
def lihat():
    datas = Pesawat.query.all()
    return render_template('view.html', datas=datas)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    datas = Pesawat.query.all()
    result = []

    for data in datas:
        obj = {
            'id': data.id,
            'kode': data.kode,
            'pesawat': data.pesawat,
            'tujuan': data.tujuan,
            'jam': data.jam,
            'gate': data.gate,
            'status': data.status
        }
        result.append(obj)
    response = jsonify(result)
    response.status_code = 200
    return response