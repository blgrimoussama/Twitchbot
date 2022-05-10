import random
from tabnanny import check
import time
import os
import json
import re

players = []
started = False
closed = False
balls = ['🔴', '🟢', '🟤', '🟡', '🔵', '🟣']  # , '⚫']
check_balls = ['⚪', '🟠']
versus = []
rounds = []
combination = []
first_start = ''
rem_rounds = 8
all_combinations = []


# print(leaderboard)


def mastermind(message, leaderboard_path):
    global players, started, closed, balls, check_balls
    global rem_rounds, versus, rounds, combination, first_start
    global all_combinations
    author = message.author
    msg = message.content.lower()
    s = msg.split()
    mod = author.is_mod
    name = author.mention.replace('@', '')
    with open(leaderboard_path, "r") as data:
        leaderboard = json.load(data)
    try:
        if msg == 'colors':
            return ['The available colors are:' + ''.join(balls)]
        if msg == 'check colors':
            return [check_balls[0] + "means it's in the combination but not in the right place", check_balls[1] + "means it's in the combination and in the right place"]
        if msg == 'master' and not started and mod:
            started = True
            closed = False
            return ['Mastermind has just started ! Type "Play" to join']
        if msg == 'master leaderboard':
            return [leaderboard]
        if started:
            if not closed:
                if msg == 'play':
                    if name not in players:
                        players.append(name)
                        time.sleep(0.5)
                        return ['You joined the game ! ' + name]
                    else:
                        time.sleep(0.5)
                        return ["You've already joined the game ! " + name]
                '''if msg == 'open' and mod:
                    closed = False
                    versus = random.sample(players, 2)'''
                if msg == 'close' and mod:
                    if len(players) >= 2:
                        closed = True
                        versus = random.sample(players, 2)
                        random.shuffle(versus)
                        rounds = versus * 4
                        combination = random.sample(balls, 4)
                        random.shuffle(combination)
                        return ['Round has started !', 'It is ' + versus[0] + ' vs ' + versus[1] + '. The first to start is : {}.'.format(versus[0])]
                    else:
                        return ['Need a minimum of 2 players to start the game !']
            if msg == 'answer' and mod:
                return ['The answer is : ' + ''.join(combination)]
            if msg == 'rounds':
                return ['There is ' + str(rem_rounds) + ' rounds left. ' + name]
            if rem_rounds <= 7:
                if msg == 'last':
                    return [all_combinations[-1]]
                if msg == 'all previous':
                    return [all_combinations]
            if s[0] == 'guess' and name in versus:
                if name != rounds[0]:
                    return ['It is not your turn !']
                else:
                    '''if s[1] == 'random':
                        guess = random.sample(balls, 4)
                        random.shuffle(guess)
                        return ['Your random guess is: ' + ''.join(guess),]'''
                    guess = list(re.sub('(\w| )', '', msg))
                    guess = [c for c in guess if c in balls][:4]
                    # print(name + "'s Guess for the " + str(8 - rem_rounds) + "round is " + str(guess) + "at " + str(message.timestamp.strftime("%H:%M:%S")))
                    if len(guess) == 0:
                        return ['Wrong Syntax !']
                    elif len(guess) < 4:
                        return ['Your guess must have 4 colors !']
                    elif guess == combination:
                        players = []
                        started = False
                        rem_rounds = 8
                        output = 'Good Job ' + name + '.' + \
                            ' You guessed the combination "{}" !'.format(
                                ''.join(combination))
                        leaderboard[name] = leaderboard.get(name, 0) + 1
                        with open(leaderboard_path, 'w') as f:
                            json.dump(leaderboard, f)
                        combination = []
                        all_combinations = []
                        return [output, 'The game is ending soon !', 'The leaderboard is : ' + str(leaderboard)]
                    else:
                        outcome = ''
                        for i in guess:
                            if i in combination:
                                if guess.index(i) == combination.index(i):
                                    outcome += '1'
                                else:
                                    outcome += '0'
                        # print(outcome)
                        output = ''.join(outcome.count('1') * [check_balls[1]] +
                                         outcome.count('0') * [check_balls[0]])
                        # print(output)
                        rounds.remove(name)
                        rem_rounds -= 1
                        all_combinations.append(
                            ''.join(guess) + ' ==> ' + output)
                        return [name + ' your matches are : ' + output]
            if (msg == 'end' and mod) or rem_rounds == 0:
                players = []
                started = False
                rem_rounds = 8
                comb_copy = combination
                combination = []
                all_combinations = []
                return ['The round has ended ! the answer is :' + ''.join(comb_copy)]
            else:
                return [0]
        else:
            return [0]
    except IndexError:
        return [0]
