import os

from flask import Flask, g
def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)

    #g['DATABASE'] = 'int.db'

    from . import db
    db.init_app(app)

    return app
