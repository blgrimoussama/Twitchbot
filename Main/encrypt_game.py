from en_randomize import randomize_eng
import random
import time

num_dict = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth',
            6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth'}
last_word = []
started = False
hinted = False
hints = 0
all_hints = []
hint = ''


def encrypt_game(message):
    global started, hinted, hints, hint, all_hints, num_dict
    msg = message.content
    author = message.author
    s = msg.split()
    mod = author.is_mod
    name = author.mention
    try:
        if s[0] == 'encrypt' or s[0] == 'en':
            global last_word
            if len(s) == 2 and mod:
                if s[1] == 'start':
                    if started:
                        return ['Game already started']
                    else:
                        started = True
                        encrypt_game(['word'])
                if started:
                    if s[1] == 'end':
                        started = False
                        return ['Game ended']
                    if last_word:
                        if s[1] == 'len':
                            return [str(len(last_word[0]))]
                        if s[1] == 'answer':
                            return [last_word[0]]
                        if s[1] == 'pairs':
                            return [last_word[2]]
                        if s[1] == 'hint':
                            if hinted:
                                return ['Already hinted !', all_hints]
                            else:
                                hint_index = random.sample(
                                    range(len(last_word[0])), 1)[0]
                                ordinal_num = num_dict[hint_index + 1]
                                hinted_let = last_word[0][hint_index]
                                if hinted_let in ['a', 'e', 'i', 'o', 'u', 'h']:
                                    v_or_c = 'n'
                                else:
                                    v_or_c = ''
                                hint = 'The ' + ordinal_num + \
                                    ' letter is a' + v_or_c + ' "' + hinted_let + '"'
                                # if hint != all_hints[-1]:
                                all_hints.append(hint)
                                hints -= 1
                                #    return hint
                                if not hints:
                                    hinted = True
                                time.sleep(0.3)
                                return ['Hint : ' + hint]

        if started and msg == 'en':
            w = randomize_eng()
            last_word = w
            hinted = False
            hints = len(last_word[0])//2
            all_hints = []
            return [w[1]]
        if started and s[0].lower() == last_word[0]:
            started = False
            return ['Good Job ' + name + '.' + ' You guessed the word "' + last_word[0].upper() + '" !', 'The game is ending soon !']
        if started and sum(a == b for a, b in zip(msg, last_word[0])) >= len(last_word[0]) - 2:
            return [name + ' You are close to the answer! Keep going!']
        else:
            return [0]
    except IndexError:
        return [0]
