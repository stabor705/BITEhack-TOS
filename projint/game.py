from flask import Blueprint, redirect, session, render_template

import jsonpickle

bp = Blueprint('game', __name__)

class Game():
    def __init__(self):
        self.score = 0
        self.tries = 0

@bp.get('/start_game')
def start_game_endpoint():
    game = Game()
    session['game'] = jsonpickle.encode(game)
    return redirect('my_game')
    
@bp.get('/my_game')
def game_endpoint():
    game = jsonpickle.decode(session['game'])

    return render_template('game.j2', game=game)