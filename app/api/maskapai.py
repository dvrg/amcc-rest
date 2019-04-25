from ..models import Maskapai
from . import api
from app import db

from flask import Flask, redirect, url_for, jsonify, make_response, abort, request


@api.route("/maskapai/", methods=["POST"])
def maskapai_baru():
    data = Maskapai.from_json(request.json)
    db.session.add(data)
    db.session.commit()
    return jsonify(data.to_json())


@api.route("/maskapai/", methods=["GET"])
def maskapai():
    data = Maskapai.query.all()
    return jsonify([data.to_json() for data in data])


@api.route("/maskapai/<int:id>", methods=["GET"])
def maskapai_detail(id):
    data = Maskapai.query.get_or_404(id)
    return jsonify(data.to_json())
