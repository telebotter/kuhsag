import logging
import cowsay
import io
import contextlib
import random

from tudel_dict import tudel

#logging.basicConfig(filename='/home/django/telebotter/wuerfeln/commands.log',level=logging.DEBUG)
from kuhsag.constants import *
commands = []

def tuedelize(text):
    message = list(text)
    reply = []
    for i in message:
        if i in tudel:
            reply.append(random.choice(tudel[i]))
        else:
            reply.append(i)
    reply = ''.join(reply)
    return reply

def cowify(text, func=cowsay.cow):
    """ catches the output of cowsay commands and converts it to a string """
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        func(text)
    string = stream.getvalue()
    return string


def asciify():
    pass


def start(bot, update):
    # get or create + logging
    #text = f'<code>{cowsay.cow(MESSAGES["start"])}</code>'
    try:
        cowtext = cowify("/help für Hilfe")
        text = f'```{cowtext}```'
    except Exception as e:
        text = str(e)
    update.message.reply_text(text, parse_mode='Markdown')
start.short = 'Beginne die Unterhaltung'
start.long = 'Damit ich nicht direkt allen auf die Nerven gehen kann, erlaubt Telegram mir nur mit Leuten zu schreiben, die die Unterhaltung durch /start oder drücken des Start-Buttons beginnen.'
commands.append(start)

def help(bot, update):
    text = "Ich bin ein Inlinebot, das heißt du kannst mich in jeder Unterhaltung benutzen indem du deine Nachricht mit @kuhsagbot beginnst."
    update.message.reply_text(text)
help.short = 'Hilfe und Befehle anzeigen'
help.long = 'Ich zeige dir wie du mit mir umgehen kannst '
commands.append(help)
