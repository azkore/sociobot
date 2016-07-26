import config
import telebot
from telebot import *

import sqlite3 as sql

bot = telebot.TeleBot(config.token)
#storefile='sooctypes.txt'
    #cur.execute("CREATE TABLE soctypes(User INT uniq, firstname text, lastname text, nick text, Type TEXT)")
soctypes=('дон','дюма', 'гюго', 'роб', 'гам', 'макс', 'жук', 'еся', 'нап','баль', 'джек', 'драй', 'штир', 'дост', 'гек', 'габ')
pitypes=('ЭЛВФ', 'ЭЛФВ', 'ЭВЛФ', 'ЭВФЛ', 'ЭФВЛ', 'ЭФЛВ', 'ЛЭФВ', 'ЛВФЭ', 'ЛВЭФ', 'ЛЭВФ', 'ЛФЭВ', 'ЛФВЭ', 'ВЛЭФ', 'ВЛФЭ', 'ВФЛЭ', 'ВФЭЛ', 'ВЭЛФ', 'ВЭФЛ', 'ФЭЛВ', 'ФЭВЛ', 'ФЛЭВ', 'ФЛВЭ', 'ФВЭЛ', 'ФВЛЭ')
allowed_chats=(-146621358, -1001053711520)

def plist(l):
    res=''
    for i in l:
        res=res  + '|<b>' + i + '</b>'
        
    res=', '.join(res.split('|')[1:])
    return res

#@bot.message_handler(content_types=["text"])
def verify_chat(message):
    if(not (message.chat.id in allowed_chats)):
        print("Sorry, I belong to Mya! {}, list {}".format(message.chat.id, str(allowed_chats)))
        bot.send_message(message.chat.id, "Sorry, I belong to Mya! (https://telegram.me/myyyaaa) \n Get me out of here")
        return False
    else:
        return True

#@bot.message_handler(content_types=["text"])
#def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
#    bot.send_message(message.chat.id, message.text)
def get_soctype(soctype):
    con = sql.connect(db)
    with con:
        cur = con.cursor()
        print("select firstname, lastname, nick  from soctypes where type='{}'".format(soctype));
        cur.execute("select firstname, lastname, nick from soctypes where type='{}'".format(soctype));
        
        rows = cur.fetchall()

        res=[]
        for row in rows:
            res.append(row[0])
        print("res" + str(res))
    return res

def show_types(message, soctype):
    #try:
    #    soctype=message.text.split(' ')[1]
    #except IndexError:
    #    soctype=''
    #soctype=message.text[6:]
    res=''
    total=0
    if soctype:
        members=get_soctype(soctype)
        print(str(members))
        res='('+str(len(members))+') '+ plist(members)
    else:
       for type in soctypes:
           members=get_soctype(type)
           res=res + type + '(' + str(len(members)) + '): ' + plist(members) + '\n'
           total=total+len(members)
       res=res+'Всего: <b>{}</b>'.format(str(total)) 
    bot.reply_to(message, str(res),parse_mode='HTML')


def show_user(message, match):
    #match=message.text[7:]
    #try:
    #    match=message.text.split(' ')[1]
    #except IndexError:
    #    match=''
    con = sql.connect(db)
    with con:
        cur = con.cursor()
        match=match.replace('@','')
        req=("select firstname, type from soctypes"
             " where lower(firstname) like lower ('%{}%')"
             " or lower(lastname) like lower ('%{}%')"
             " or lower(nick) like lower ('%{}%')").format(match,match,match)
        print(req);
        cur.execute(req);
        rows = cur.fetchall()

        res=""
        for row in rows:
            res=res+"{}: {}".format(row[0], row[1])
        print("res" + str(res))

        req=("select type from pitypes"
             " where lower(firstname) like lower ('%{}%')"
             " or lower(lastname) like lower ('%{}%')"
             " or lower(nick) like lower ('%{}%')").format(match,match,match)
        print(req);
        cur.execute(req);
        rows = cur.fetchall()

        for row in rows:
            res=res+" {}".format(row[0])
        print("res" + str(res))

        bot.reply_to(message, str(res))


@bot.message_handler(commands=['show','whois','s'])
def show(message):
    try:
        match=message.text.split(' ')[1]
    except IndexError:
        match=''
    if(not match or match in soctypes):
        show_types(message, match)
    else:
        show_user(message, match) 

@bot.message_handler(commands=['pitype'])
def pitest(message):
    try:
        arg=message.text.split(' ')[1]
    except IndexError:
        arg=''

    markup = types.ReplyKeyboardMarkup(row_width=6, one_time_keyboard=False, selective=True)
    markup.add(*pitypes)

    if((arg=="all") and (message.from_user.username=='azcore')):
        markup = types.ReplyKeyboardMarkup(row_width=6, one_time_keyboard=False, selective=False)
        markup.add(*soctypes)
        bot.send_message(message.chat.id, "Вы кто такие все по пй?", reply_markup=markup)
    elif(message.reply_to_message):
        bot.reply_to(message.reply_to_message, "Кто ты по пй, " + message.reply_to_message.from_user.first_name + '?', reply_markup=markup)
    elif(arg):
        bot.send_message(message.chat.id, "Кто ты по пй, " + arg  + '?', reply_markup=markup)
    else:
        bot.reply_to(message, "Кто ты по пй, " + message.from_user.first_name + '?', reply_markup=markup)


@bot.message_handler(commands=['type', 't'])
#@bot.message_handler(commands=['type'])
def default_test(message):
    try:
        arg=message.text.split(' ')[1]
    except IndexError:
        arg=''
    #keyboard = types.InlineKeyboardMarkup()
    #url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    #keyboard.add(url_button)
    #bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard)

# Using the ReplyKeyboardMarkup class
# It's constructor can take the following optional arguments:
# - resize_keyboard: True/False (default False)
# - one_time_keyboard: True/False (default False)
# - selective: True/False (default False)
# - row_width: integer (default 3)
# row_width is used in combination with the add() function.
# It defines how many buttons are fit on each row before continuing on the next row.
    markup = types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=False, selective=True)
    markup.add(*soctypes)
    if((arg=="all") and (message.from_user.username=='azcore')):
        markup = types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=False, selective=False)
        markup.add(*soctypes)
        bot.send_message(message.chat.id, "Вы кто такие все?", reply_markup=markup)
    elif(message.reply_to_message):
        bot.reply_to(message.reply_to_message, "Кто ты, " + message.reply_to_message.from_user.first_name + '?', reply_markup=markup)
    elif(arg):
        bot.send_message(message.chat.id, "Кто ты, " + arg  + '?', reply_markup=markup)
    else:
        bot.reply_to(message, "Кто ты, " + message.from_user.first_name + '?', reply_markup=markup)

def is_soctype(arg):
    if(arg.text in soctypes):
        return True
    #else:
    #    print(arg)

def is_pitype(arg):
    if(arg.text in pitypes):
        return True

@bot.message_handler(func=is_soctype)
def answer(message):
    if(not verify_chat(message)):
        return()
    keyboard_hider = types.ReplyKeyboardHide(selective=True)
    text='ok'
    if(message.text.startswith('дон')):
         text='Малаца, так держать!'
    if(message.text.startswith('еся')):
         text='Маленькая есечка!'
    if(message.text.startswith('гек')):
         text='Опасайся злобной блуд!'
    if(message.text.startswith('гек') and message.from_user.username=='BlaBla7'):
         text='Опасайся злобной блуд! А. ты ж и есть злобная блуд...'
    if(message.from_user.first_name=='gr'):
        if(message.text.startswith('еся')):
            text='Правду говорить легко и приятно!'
        else:
            text='Ну мы-то знаем...'
    #with shelve.open(storefile) as store:
        #store[str(message.from_user.id)]=message.text
        #try:
        #    store[message.text].add(str(message.from_user.id))
        #except KeyError:
        #    store[message.text]=[str(message.from_user.id)]
    con = sql.connect(db)
    with con:
        cur = con.cursor()
        user=message.from_user
        cur.execute("delete from soctypes where user=" +str(user.id))
        print(str(user.id), user.first_name, user.last_name, user.username, message.text)
        cur.execute("INSERT INTO soctypes VALUES ({}, '{}', '{}', '{}', '{}', 'None')".format(str(user.id), user.first_name, user.last_name, user.username, message.text))


    bot.reply_to(message, text, reply_markup=keyboard_hider)

@bot.message_handler(func=is_pitype)
def pianswer(message):
    if(not verify_chat(message)):
        return()
    keyboard_hider = types.ReplyKeyboardHide(selective=True)
    text='ok'

    con = sql.connect(db)
    with con:
        cur = con.cursor()
        user=message.from_user
        cur.execute("delete from pitypes where user=" +str(user.id))
        print(str(user.id), user.first_name, user.last_name, user.username, message.text)
        cur.execute("INSERT INTO pitypes VALUES ({}, '{}', '{}', '{}', '{}')".format(str(user.id), user.first_name, user.last_name, user.username, message.text))

    bot.reply_to(message, text, reply_markup=keyboard_hider)

if __name__ == '__main__':
    bot.polling(none_stop=True)
