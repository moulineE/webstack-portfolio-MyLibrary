#!/usr/bin/python3
""" Index api """
from api.v1.views import app_views
from flask import jsonify, session
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Status """
    return jsonify({"status": "OK"})


@app_views.route('/languages_by_id/<lang_id>', strict_slashes=False)
def languages_by_id(lang_id):
    """ languages by id """
    lang = session['lang']
    return jsonify(lang)
