from flask import Blueprint, jsonify

from core.EnvironmentManager import EnvironmentManager

environments_api = Blueprint('environments_api', __name__)
environmentManager = EnvironmentManager()

@environments_api.route("/environments")
def environments():
    return jsonify(list(map(lambda x: x["environment"], environmentManager.list())))
