import os

from flask import Flask, render_template

from projint import game

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    from . import db
    db.init_app(app)
    
    app.register_blueprint(game.bp)
    @app.get("/")
    def main_endpoint():
        return render_template('home.j2', project_name = 'aseof')
    
    @app.get("/about")
    def about_endpoint():
        return render_template('about.j2')

    return app
