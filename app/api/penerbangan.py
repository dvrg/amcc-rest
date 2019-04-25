from ..models import Penerbangan
from . import api
from app import db

from flask import Flask, redirect, url_for, jsonify, make_response, abort, request


@api.route("/penerbangan/", methods=["POST"])
def penerbangan_baru():
    data = Penerbangan.from_json(request.json)
    db.session.add(data)
    db.session.commit()
    return jsonify(data.to_json())


@api.route("/penerbangan/", methods=["GET"])
def penerbangan():
    data = Penerbangan.query.all()
    return jsonify([data.to_json() for data in data])


@api.route("/penerbangan/<int:id>", methods=["GET"])
def penerbangan_detail(id):
    data = Penerbangan.query.get_or_404(id)
    return jsonify(data.to_json())
