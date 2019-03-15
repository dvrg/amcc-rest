import os
from flask import Flask, render_template, redirect, flash, url_for, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, Length
from wtforms.fields.html5 import DateField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Halaman tidak ditemukan!'}), 404)

class FormData(FlaskForm):
    kode = StringField(u'Kode Penerbangan', validators=[DataRequired(), Length(min=5, max=5)])
    pesawat = SelectField(u'Nama Maskapai', choices=[('nam air', 'nam air'), ('lion air', 'lion air'), ('sriwijaya air', 'sriwijaya air'), ('batik air', 'batik air'), ('garuda indonesia', 'garuda indonesia')])
    tujuan = StringField(u'Tujuan', validators=[DataRequired(), Length(min=7, max=7)])
    jam = DateField(u'Jam Berangkat')
    gate = SelectField(u'Gate', choices=[('01','01'), ('02','02'), ('03','03'), ('04','04')])
    status = SelectField(u'Status', choices=[('check in', 'check in'), ('to waiting room', 'to waiting room'), ('landing', 'landing'), ('take off', 'take off')])
    submit = SubmitField(u'Simpan')

    def validate_kode(self, kode):
        kode = Pesawat.query.filter_by(kode=kode.data).first()
        if kode is not None:
            raise ValidationError('kode sudah ada, gunakan kode lain!')

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

    @validates('kode', 'pesawat', 'tujuan', 'status')
    def convert_upper(self, key, value):
        return value.upper()


@app.route('/tambah-data', methods=['GET', 'POST'])
def tambah():
    form = FormData()
    if form.validate_on_submit():
        data = Pesawat(kode=form.kode.data, pesawat=form.pesawat.data, tujuan=form.tujuan.data, gate=form.gate.data, status=form.status.data)
        db.session.add(data)
        db.session.commit()
        flash('Data Tersimpan!')
        return redirect(url_for('lihat'))
    return render_template('admin/add_data.html', form=form)

@app.route('/')
def lihat():
    data = Pesawat.query.all()
    return render_template('admin/view_data.html', data=data)

@app.route('/api/pesawat', methods=['GET'])
def get_data():
    data = Pesawat.query.all()
    result = []

    for data in data:
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

if __name__ == "__main__":
    app.run(host= '0.0.0.0')