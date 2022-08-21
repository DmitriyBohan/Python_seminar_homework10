from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

updater = Updater('5606526865:AAGFAtNAAJeOsjIVk-6X5BmmXrGxnk6bNFs')
dispatcher = updater.dispatcher

START = 0
PLAYER_ONE_NAME = 1
PLAYER_TWO_NAME = 2
NUMBER = 3
FINISH_GAME = 4
EXAMINATION = 5

name_player_one = ''
name_player_two = ''
examination = -1
candies = 101
count = 1
number = 0


def start(update, context):
    update.message.reply_text('Тебя приветствует Телеграм-Бот игра в конфеты !\n'
                              'На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга.\n'
                              'За один ход можно забрать не более чем 28 конфет.\n'
                              'Все конфеты оппонента достаются сделавшему последний ход.\n'
                              'Как зовут первого игрока?')

    return PLAYER_ONE_NAME


def nameOnePlayer(update, context):
    global name_player_one
    name_player_one = update.message.text
    update.message.reply_text('А как зовут второго игрока ? ')

    return PLAYER_TWO_NAME


def nameTwoPlayer(update, context):
    global name_player_two
    name_player_two = update.message.text
    update.message.reply_text('Начнем ?')
    return NUMBER


def number_request(update, context):
    global candies
    global count
    if count == 1:
        update.message.reply_text(f'Ходит {name_player_one}!\n'
                                  'Сколько конфет вы возьмете?\n')
        count *= -1
    elif count == -1:
        update.message.reply_text(f'Ходит {name_player_two}!\n'
                                  'Сколько конфет вы возьмете?\n')
        count *= -1
    number = update.message.text
    candies -= int(number)
    update.message.reply_text(f'На столе осталось {candies} конфеты\n')

    return EXAMINATION


def examination_(update, context):
    if candies > 0:
        number_request(update, context)
    else:
        cancel(update, context)


def cancel(update, context):
    if count == 1:
        update.message.reply_text(f'Выйграл {name_player_one}!\n')
    elif count == -1:
        update.message.reply_text(f'Выйграл {name_player_two}!\n')

    return ConversationHandler.END


start_handler = CommandHandler('start', start)

nameOne_handler = MessageHandler(Filters.text, nameOnePlayer)
nameTwo_handler = MessageHandler(Filters.text, nameTwoPlayer, number_request)
number_handler = MessageHandler(Filters.text, number_request)
examination_handler = MessageHandler(Filters.text, examination_)
cancel_handler = CommandHandler('cancel', cancel)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        PLAYER_ONE_NAME: [nameOne_handler],
        PLAYER_TWO_NAME: [nameTwo_handler],
        NUMBER: [number_handler],
        EXAMINATION: [examination_handler],
        FINISH_GAME: [cancel_handler],

    },
    fallbacks=[cancel_handler],
)

dispatcher.add_handler(conv_handler)

print('server start')
updater.start_polling()
updater.idle()
