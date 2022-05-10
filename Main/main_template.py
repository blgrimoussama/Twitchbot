import time
import re
import os.path
import os
import config
from twitchio.ext import commands
from encrypt_game import encrypt_game
from mastermind import mastermind
from functions import Timer

# channel_name = input('Channel Name : ')

Timer_1 = Timer()


class Bot(commands.Bot):
    def __init__(self, bot_name, chat_to):  # , chat_to):
        # global initials

        self.bot_name = bot_name.lower()
        self.chat_to = chat_to.lower()
        self.save_path = bot_name + '/message_log'
        self.mastermind = bot_name + '/mastermind'
        if not os.path.exists(self.mastermind):
            os.makedirs(self.mastermind)
            with open(os.path.join(self.mastermind, "leaderboard.json"),
                      "a") as master_leaderboard:
                master_leaderboard.write("{}")
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        # new_channel = input("New channel : ")
            # if not self.chat in initials:
            #     initials += self.chat
        super().__init__(token=config.self.bot_name,
                         prefix='!',
                         initial_channels=['channel_1', self.chat_to])  # new_channel

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in to {self.chat_to} as | {self.nick}')

    async def event_message(self, message):
        # global channel_name
        s = message.content.split()
        msg = message.content.lower()
        # dir(message.author)
        self.channel = self.get_channel(self.chat_to)  # channel_name
        try:
            name = message.author.name
            channel = re.search(".+: (.+)>", str(message.channel)).group(1)
            output = name + ' : ' + message.content + ' - ' + message.timestamp.strftime(
                "%H:%M:%S") + ' - ' + str(channel) + ' - ' + str(
                    message.author.badges)
            # print(output)
            with open(os.path.join(self.save_path,
                                   "history_log_" + channel + ".txt"),
                      "a",
                      encoding='utf-8') as f:
                f.write(str(output) + '\n')
        except KeyError and AttributeError:
            pass
        try:
            if msg == 'test':
                await self.channel.send("It's a test # {} - {} -".format(
                    message.author, message.timestamp))
                time.sleep(1)
                await self.channel.send(str(message.author.badges))
            '''if msg == 'timer':
                Timer_1.start()
                await self.channel.send('timer started')
            if msg == 'timer show':
                await self.channel.send(Timer_1.show())
            if msg == 'timer stop':
                Timer.stop()'''
            if s[0] == 'Calculate':
                try:
                    await self.channel.send(str(eval(msg[5:])))
                except SyntaxError and NameError:
                    await self.channel.send('?!?!')
            if s[0] == 'say':
                await self.channel.send(msg[4:])
            '''if s[0] == 'السلام' or s[0] == 'سلام':
                await self.channel.send('وعليكم السلام والرحمة')
            if s[0] == 'باك':
                await self.channel.send('ولكم باك')'''
        except IndexError:
            pass
        try:
            en_game = encrypt_game(message)
            if en_game[0]:
                for out in en_game:
                    await self.channel.send(out)
                    time.sleep(0.5)
            master_leaderboard = os.path.join(self.mastermind,
                                              "leaderboard.json")
            ma_game = mastermind(message, master_leaderboard)
            if ma_game[0]:
                for out in ma_game:
                    await self.channel.send(out)
                    time.sleep(0.6)
            # number_game = numbergame(message)
            # if number_game[0]:
            #    for out in number_game:
            #        await self.channel.send(out)
            #        time.sleep(0.6)
        except AttributeError:
            pass
