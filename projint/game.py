from flask import Blueprint, redirect, session, render_template, request

import jsonpickle
import random
import datetime
from . import db

bp = Blueprint('game', __name__)

class Transformation:
    def __init__(self, idx: int, content: str):
        self.idx = idx
        self.content = content
class Round:
    def __init__(self, integral: str, answers_num: int, transformations: list[Transformation]):
        self.integral = integral
        self.transformations = transformations
        self.transformations_num = answers_num

class Game:
    def __init__(self, ID:int, rounds: list[Round]):
        self.score = 0
        self.tries = 0
        self.rounds = rounds
        self.current_round = -1
        self.failures = 0
        self.gameID = ID

def getRound(ind):
    app_db = db.get_db()

    answers = app_db.execute("""select ans_windows.answers from ans_windows where id = ? ORDER BY window_number""",
                             (ind,)).fetchall()
    other_windows = app_db.execute("""select user_windows.proposed_answers from user_windows where id = ?""",
                                   (ind,)).fetchall()
    transformations = [Transformation(i, answers[i]['answers']) for i in range(len(answers))] + \
                      [Transformation(-1, item['proposed_answers']) for item in other_windows]
    return Round(app_db.execute("""select integrals.integral_string from integrals where id = ?""",
                             (ind,)).fetchone()['integral_string'],  len(answers), transformations)

def getRounds(n, level):
    """Return list of n rounds with defined level """
    app_db = db.get_db()
    ans = []
    items = app_db.execute("""select * from integrals where integral_level = ?""", (level,)).fetchall()
    inds = [(item['id'], item['integral_string']) for item in items]
    random.shuffle(inds)
    for item in items:
        for i in range(n):
            if(item['id'] == inds[i][0]):
                ans.append(getRound(item['id']))
    return ans

@bp.get('/start_game')
def start_game_endpoint():
    app_db = db.get_db()
    # ints = app_db.execute("""select * from integrals""").fetchone()
    # answer = Transformation(0, app_db.execute(
    #     """select ans_windows.answers from ans_windows where id = ?""", (ints['id'],)).fetchone())
    # wrong_answers = app_db.execute(
    #     """select user_windows.proposed_answers from user_windows where id = ?""", (ints['id'],)).fetchall()

    # Transformation(app_db.execute(
    #     """select ans_windows.answers from ans_windows where id = ?""", (ints['id'],)).fetchone())
    # transformations = [answer] + [Transformation(-1, item['proposed_answers']) for item in wrong_answers]
    #
    # rounds = Round(ints['integral_string'], [transformations])

    app_db.execute('''insert into game_data (user_id, game_start_time) VALUES (0, ?);''', (datetime.datetime.now(),))
    gameId = app_db.execute('''select id from game_data order by id desc limit 1''').fetchone()['id']
    game = Game(gameId,
                getRounds(3, 0) + getRounds(2, 1))
    print(game.gameID)

    session['game'] = jsonpickle.encode(game)
    return redirect('my_game')

def checkRound(game, ind):
    round = game.rounds[ind]
    for i in range(round.transformations_num):
        if request[f'{i}'] == i:
            game.score += 10

@bp.route('/my_game', methods=('GET', 'POST'))
def game_endpoint():
    app_db = db.get_db()
    game = jsonpickle.decode(session['game'])

    game.current_round += 1
    session['game'] = jsonpickle.encode(game)
    if game.current_round == 5:
        app_db.execute("""update game_data set game_finish_time = ?, score_in_game = ?, longest_series = ? 
            where id = ?""",
                       (datetime.datetime.now(), game.score, 0, game.gameID))
        return redirect("/")

    return render_template('game.j2', score=game.score, tries=game.tries, round=game.rounds[game.current_round])