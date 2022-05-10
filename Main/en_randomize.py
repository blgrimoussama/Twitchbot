import random
import os.path


def randomize_eng():
    symbols = [chr(i) for i in range(34, 127)]
    english_letters = [chr(i) for i in range(97, 123)]
    # print(english_letters)
    random_list = random.sample(symbols, k=26)

    # print(len(arabic_letters))
    # print(arabic_letters)
    # print(random_list)

    couples_dict = dict(el for el in zip(english_letters, random_list))
    # print(couples_dict)

    words = open(os.path.join('Main', "word_list.txt")).read().splitlines()
    word = random.choice(words)
    # print(word)

    output = ' '.join([couples_dict[letter] for letter in word])
    # print(output)
    return [word, output, couples_dict]
