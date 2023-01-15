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
    def __init__(self, integral: str, answers_num: int, level:int, transformations: list[Transformation]):
        self.integral = integral
        self.transformations = transformations
        self.transformations_num = answers_num
        self.level = level
        self.tries = 0
class Game:
    def __init__(self, ID:int, rounds: list[Round]):
        self.previousSerie = True
        self.score = 0
        self.rounds = rounds
        self.current_round = -1
        self.failures = 0
        self.gameID = ID
        self.longest_serie = 0
        self.serie = -1

def getRound(ind):
    app_db = db.get_db()

    answers = app_db.execute("""select ans_windows.answers from ans_windows where id = ? ORDER BY window_number""",
                             (ind,)).fetchall()
    other_windows = app_db.execute("""select user_windows.proposed_answers from user_windows where id = ?""",
                                   (ind,)).fetchall()
    transformations = [Transformation(i, answers[i]['answers']) for i in range(len(answers))] + \
                      [Transformation(-1, item['proposed_answers']) for item in other_windows]
    random.shuffle(transformations)
    return Round(app_db.execute("""select integrals.integral_string from integrals where id = ?""",
                             (ind,)).fetchone()['integral_string'],  len(answers),
                 app_db.execute("""select integrals.integral_level from integrals where id = ?""",
                             (ind,)).fetchone()['integral_level']
                 , transformations)

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

@bp.route('/start_game', methods=('GET', 'POST'))
def start_game_endpoint():
    app_db = db.get_db()

    app_db.execute('''insert into game_data (user_id, score_in_game, longest_series, game_start_time, game_finish_time) VALUES (0,NULL, NULL, ?, NULL);''',
                   (datetime.datetime.now(),))
    app_db.commit()
    gameId = app_db.execute('''select id from game_data order by id desc limit 1''').fetchone()['id']
    level = (int)(request.form['level'])
    game = None
    if level == 0:
        game = Game(gameId,
                    getRounds(5, 0))
    elif level == 1:
        game = Game(gameId,
                    getRounds(3, 0) + getRounds(2, 1))
    else:
        game = Game(gameId,
                    getRounds(2, 0) + getRounds(2, 1) + getRounds(1, 1))
    print(game.gameID)

    session['game'] = jsonpickle.encode(game)
    return redirect('my_game')

def checkRound(game, ind):
    app_db = db.get_db()
    round = game.rounds[ind]
    is_right_answer = []
    add_sum = 0
    game.serie += 1
    for i in range(round.transformations_num):
        print(request.form[f'{i}'], i)
        if (request.form[f'{i}']) != '' and (int)(request.form[f'{i}']) == i:
            #add_sum += 10 * (game.serie + 1)
            is_right_answer.append(True)
        else:
            game.longest_serie = max(game.longest_serie, game.serie)
            game.serie = -1
            is_right_answer.append(False)

    if  not False in is_right_answer:
        game.score += ((round.level+1) * (game.serie+1) * 10)

    return is_right_answer


@bp.route('/my_game', methods=('GET', 'POST'))
def game_endpoint():
    game = jsonpickle.decode(session['game'])
    answers = None
    if game.current_round != -1:
        answers = checkRound(game, game.current_round)
        if False in answers:
            game.rounds[game.current_round].tries += 1
            game.current_round -= 1

        else:
            answers = None
        #request.form['answers'] = answers

    game.current_round += 1
    session['game'] = jsonpickle.encode(game)
    if game.current_round == 5:
        app_db = db.get_db()
        app_db.execute("""update game_data set game_finish_time = ?, score_in_game = ?, longest_series = ? 
            where id = ?""",
                       (datetime.datetime.now(), game.score, 0, game.gameID))
        app_db.commit()

        return redirect("/")

    return render_template('game.j2', game=game, round=game.rounds[game.current_round], answers=answers)

# @bp.route('/stats', method=('POST', 'GET'))
# def make_stats_endpoint():
#     app_db = db.get_db()
#     stats =  app_db.execute('''select * from game_data where game_finish_time IS NOT NULL''').fetchall()
#
#     statistics = [len(stats) * 5, sum(( (datetime)(stats[i]['game_finish_time']) - (datetime.datetime)(stats[i]['game_start_time'])) for i in stats)]
