#myapp/telegrambot.py
# Example code for telegrambot.py module
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, InlineQueryHandler
from django_telegrambot.apps import DjangoTelegramBot
from kuhsag.constants import *
#from listerer.models import Chat, Item, Message

from kuhsag.commands import *

import io
import contextlib
import logging
logger = logging.getLogger(__name__)

import cowsay
from uuid import uuid4

def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))


speakers = [
    {'name': 'Kuh', 'func': cowsay.cow, 'emoji': '🐄', 'wrap': True},
    {'name': 'Tux', 'func': cowsay.tux, 'emoji': '🐧', 'wrap': True},
    {'name': 'Tüdelizer', 'func': tuedelize, 'emoji': '🥴'},
]

def inlinequery(bot, update):
    query = update.inline_query.query
    options = []
    for speaker in speakers:
        if speaker.get('wrap', False):
            cowtext = cowify(query, func=speaker['func'])
        else:
            cowtext = speaker['func'](query)
            print(cowtext)
        options.append(
            InlineQueryResultArticle(
                #title=f'{speaker["emoj"]} {speaker["name"]} sagt:',
                title=speaker['emoji']+' '+speaker['name'],
                id=uuid4(),
                description=query,
                input_message_content = InputTextMessageContent(f'```{cowtext}```', parse_mode='Markdown')
            )
    )

    #results = options #todo filter by query
    update.inline_query.answer(options, cache_time=0)


def main():
    logger.info("Loading handlers for kuhsagbot")
    dp = DjangoTelegramBot.getDispatcher('kuhsagbot')
    # dp = DjangoTelegramBot.getDispatcher('telebotterbot')
    for cmd in commands:
        pass_args = cmd.pass_args if hasattr(cmd, 'pass_args') else False
        name = cmd.command if hasattr(cmd, 'command') else cmd.__name__
        dp.add_handler(CommandHandler(name, cmd, pass_args=pass_args))
    #dp.add_handler(InlineQueryHandler(inlinequery))
    #dp.add_handler(CallbackQueryHandler(callback))
    #dp.add_error_handler(error)
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_error_handler(error)

    # log all errors
    #dp.add_error_handler(error)
