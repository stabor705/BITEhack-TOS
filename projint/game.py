from flask import Blueprint, redirect, session, render_template

import jsonpickle

bp = Blueprint('game', __name__)

class Transformation:
    def __init__(self, idx: int, content: str):
        self.idx = idx
        self.content = content
class Round:
    def __init__(self, integral: str, transformations: list[Transformation]):
        self.integral = integral
        self.transformations = transformations

class Game:
    def __init__(self, rounds: list[Round]):
        self.score = 0
        self.tries = 0
        self.rounds = rounds
        self.current_round = 0

@bp.get('/start_game')
def start_game_endpoint():
    game = Game()
    session['game'] = jsonpickle.encode(game)
    return redirect('my_game')
    
@bp.get('/my_game')
def game_endpoint():
    game = jsonpickle.decode(session['game'])
    return render_template('game.j2', score=game.score, tries=game.tries, round=game.rounds[game.current_round])