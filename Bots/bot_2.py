from Main.main_template import Bot

if __name__ == '__main__':
    bot = Bot('bot_channel_2', 'chat_channel_2')

    bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
