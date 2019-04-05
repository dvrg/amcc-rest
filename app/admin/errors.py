from . import admin
from flask import redirect, make_response, abort, jsonify


@admin.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Tidak Ada Data!"}), 404)


@admin.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
