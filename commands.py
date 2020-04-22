import logging
import cowsay
import io
import contextlib
import random
import codecs
import re

from kuhsag.tudel_dict import tudel
from kuhsag.dicts import de_edit,en_edit

#logging.basicConfig(filename='/home/django/telebotter/wuerfeln/commands.log',level=logging.DEBUG)
from kuhsag.constants import *
commands = []

def emojize(text):
    #b=codecs.decode("F09F9982", "hex").decode('utf-8')
    dict1 = de_edit.de_dict
    dict2 = en_edit.en_dict
    new_dict = {}
    for dicts in dict1,dict2:
        #alle eingetragenen dicts durchiterieren
        for key in dicts:
            #print(codecs.decode(str(key), "hex").decode('utf-8'))
            #alle keys (Hex strings) durchiterieren
            if type(dicts[key]) == tuple:
                tuple_item = dicts[key]
            elif type(dicts[key]) == str:
                tuple_item = (dicts[key],)
            else:
                print('Fehler: Element ist werder str, noch tupel')
            for new_key in tuple_item:
                #durch die elemente des tupels iterieren
                if len(new_key) > 2:
                    if not new_key in new_dict:
                        new_dict[new_key] = (str(key),)
                    else:
                        #eigentlich ist der key nicht neu sondern alt...
                        old_value = new_dict[new_key]
                        new_dict[new_key] = (str(key),) + old_value
                else:
                    pass

    #text = 'okay, für heute bin ich ganz zufrieden :) gute nacht lukas'#Hallo, ich bins, hendrik. Wie gehts dem Hai? Dies ist ein etwas längerer Text, um mal zu sehen was der emojizer so alles drauf hat nech :) ausserdem habe ich eine random funktion eingebaut, die dafür sorgt das aus der auswahl der möglichen emojis immer ein zufälliger genommen wird. vorher habe ich immer das nullte element genommen. lol. deshalb den text von anfangs nochmal: hallo, ich bin der hendrik. dem hai gehts gut!'
    text = text.lower()
    word_list = re.findall("\w+", text) #gibt eine liste mit wörtern(strings)

    for key in sorted(new_dict, key=len, reverse=True):
        #Through keys sorted by length, damit die mehrfachkeys erkannt werden
        # key ist das kleine text schnipsel was durch emoji ersetzt werden soll
        if ' ' in key:
            #wenn key ein leerzeichen enthält, einfach ersetzen
            replacement = new_dict[key]
            replacement = codecs.decode(random.choice(replacement), "hex").decode('utf-8')
            text = text.replace(key, str(replacement))
        else:
            #wenn kein leerzeichen vorhanden ist muss regex benutz werden um ganze wörter zu finden
            for word in word_list:
                if word == key:
                    replacement = new_dict[word]
                    replacement = codecs.decode(random.choice(replacement), "hex").decode('utf-8')
                    text = re.sub(r"\b%s\b" % word,replacement,text)#text.replace(word, str(replacement))
                elif len(key) > 4:
                    if key in word:
                        replacement = new_dict[key]
                        replacement = codecs.decode(random.choice(replacement), "hex").decode('utf-8')
                        text = re.sub(r"\b%s\b" % word,replacement,text)
                    else:
                        pass
                else:
                    pass
    return text

def tuedelize(text):
    message = list(text)
    reply = []
    for i in message:
        reply.append(random.choice(tudel.get(i, i)))
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
