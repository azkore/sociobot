import config
import subprocess
import telebot
from telebot import *

import sqlite3 as sql

bot = telebot.TeleBot(config.token)
db = config.db
#cur.execute("CREATE TABLE soctypes(User INT uniq, firstname text, lastname text, nick text, Type TEXT)")
soctypes=('дон','дюма', 'гюго', 'роб', 'гам', 'макс', 'жук', 'еся', 'нап','баль', 'джек', 'драй', 'штир', 'дост', 'гек', 'габ')
pitypes=('ЭЛВФ', 'ЭЛФВ', 'ЭВЛФ', 'ЭВФЛ', 'ЭФВЛ', 'ЭФЛВ', 'ЛЭФВ', 'ЛВФЭ', 'ЛВЭФ', 'ЛЭВФ', 'ЛФЭВ', 'ЛФВЭ', 'ВЛЭФ', 'ВЛФЭ', 'ВФЛЭ', 'ВФЭЛ', 'ВЭЛФ', 'ВЭФЛ', 'ФЭЛВ', 'ФЭВЛ', 'ФЛЭВ', 'ФЛВЭ', 'ФВЭЛ', 'ФВЛЭ')
titles=('Мя!',
        'Соционический хаос',
        'Трэш, Флуд, Две зануды',
        'Попки и бухло!',
        'Попки и бухло',
        'СГМ',
        'Сиськи, попки, бухло, сгм'
        'Соционика Головного Мозга',
        'Мечты Аушры',
        'Мя! Социохаос',
        'Зомби-чят ССС',
        )
mya=-1001053711520
myaux=-146621358
allowed_chats=(myaux, mya)

def plist(l):
    res=''
    for i in l:
        res=res + i + ", "
        
    return res.strip(', ')

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

def sort_titles():
    con = sql.connect(db)
    with con:
        cur = con.cursor()
        cur.execute("select title,count(*) from titles group by title order by count(*) desc ;");
        rows = cur.fetchall()
        res=[]
        for row in rows:
            res.append(row[0])
        print("res" + str(res))
    return res

def get_pop_title():
    con = sql.connect(db)
    with con:
        cur = con.cursor()
        cur.execute("select title,count(*) from titles group by title order by count(*) desc limit 1;");
        rows = cur.fetchall()
        res=rows[0][0]
        print("pop_title:" + str(res))
    return res

def get_old_pop_title():
    con = sql.connect(db)
    with con:
        cur = con.cursor()
        cur.execute("select title from titles where user=1;");
        rows = cur.fetchall()
        res=[]
        for row in rows:
            res.append(row[0])
        print("res" + str(res))
    return res

def update_title():
    con = sql.connect(db)
    with con:
        cur = con.cursor()
        cur.execute("update titles set firstname='Мя!' where user=1;");

def get_titles(title):
    con = sql.connect(db)
    with con:
        cur = con.cursor()
        print("select firstname, lastname, nick  from titles where title='{}'".format(title));
        cur.execute("select firstname, lastname, nick from titles where title='{}'".format(title));
        
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

    quadras=['α','ϐ','γ','δ']
    if soctype:
        members=get_soctype(soctype)
        print(str(members))
        res='(<b>'+str(len(members))+'</b>) '+ plist(members)
    else:
       i=0
       for type in soctypes:
           members=get_soctype(type)
           if(i%4==0):
               q=int(i/4)
               print(q)
               qtot=0
               res=res+"<b>• "+quadras[q]+"</b>\n"
           res=res+"    <b>{} ({})</b>: {}\n".format(type.upper(), str(len(members)), plist(members))
           
           i=i+1
           total=total+len(members)
           qtot=qtot+len(members)
           if(i%4==0):
               res=res.replace(quadras[q], quadras[q]+" ("+str((qtot))+")")
       res=res+'Всего: <b>{}</b>'.format(str(total)) 
    bot.reply_to(message, str(res),parse_mode='HTML')

@bot.message_handler(commands=['titles'])
def show_titles(message):
    if(not (message.chat.id == myaux)):
        return

    res=""
    for title in sort_titles():
        members=get_titles(title)
        res=res + title + '(<b>' + str(len(members)) + '</b>): ' + plist(members) + '\n'
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

        res={}
        for row in rows:
            #res=res+"{}: {}".format(row[0], row[1])

            try:
                res[row[0]]
            except:
                res[row[0]]={}
            res[row[0]]['soc']=row[1]
            res[row[0]]['pi']=''

        req=("select firstname, type from pitypes"
             " where lower(firstname) like lower ('%{}%')"
             " or lower(lastname) like lower ('%{}%')"
             " or lower(nick) like lower ('%{}%')").format(match,match,match)
        print(req);
        cur.execute(req);
        rows = cur.fetchall()

        for row in rows:
            try:
                res[row[0]]
            except:
                res[row[0]]={}
            res[row[0]]['pi']=row[1]
            try:
                res[row[0]]['soc']
            except:
                res[row[0]]['soc']=''
            res[row[0]]['pi']=row[1]

        res_str=''
        if(not res):
            res_str="no info"
        else:
            for user in res:
                res_str=res_str+("<b>{}</b>: {} {}, ".format(user,res[user]['soc'],res[user]['pi']))

        print(str(res))
        bot.reply_to(message, res_str.strip(" ,"), parse_mode='HTML')


@bot.message_handler(commands=['show','whois'])
def show(message):
    try:
        match=message.text.split(' ')[1]
    except IndexError:
        match=''
    if((not match) or (match in soctypes)):
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
    p=map(lambda x: '>'+str(x), pitypes)
    markup.add(*p)

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
    s=map(lambda x: '>'+str(x), soctypes)
    markup.add(*s)
    if((arg=="all") and (message.from_user.username=='azcore')):
        markup = types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=False, selective=False)
        markup.add(*soctypes)
        bot.send_message(message.chat.id, "Вы кто такие все?", reply_markup=markup)
    elif(message.reply_to_message):
        bot.reply_to(message.reply_to_message, "Кто ты по тиму, " + message.reply_to_message.from_user.first_name + '?', reply_markup=markup)
    elif(arg):
        bot.send_message(message.chat.id, "Кто ты по тиму, " + arg  + '?', reply_markup=markup)
    else:
        bot.reply_to(message, "Кто ты по тиму, " + message.from_user.first_name + '?', reply_markup=markup)

def is_soctype(arg):
    if(arg.text and (arg.text[1:] in soctypes)):
        return True
    #else:
    #    print(arg)

def is_pitype(arg):
    if(arg.text and (arg.text[1:] in pitypes)):
        return True

def is_title(arg):
    if(arg.text and ((arg.text in titles) or (arg.text[0]=='-' and arg.text[1:] in titles))):
        return True

@bot.message_handler(commands=['title'])
def title_poll(message):
    if(not (message.chat.id == myaux)):
        return

    try:
        arg=message.text.split(' ')[1]
    except IndexError:
        arg=''

    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=False, selective=True)
    markup.add(*(reversed(titles)))
    poll="Проголосуй за название чата, {} (варианты пролистываются, голосовать можно за несколько вариантов по очереди, новые варианты принимаются)."

    if((arg=="all") and (message.from_user.username=='azcore')):
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=False, selective=False)
        markup.add(*titles)
        bot.send_message(message.chat.id, poll, reply_markup=markup)
    elif(message.reply_to_message):
        bot.reply_to(message.reply_to_message, poll.format(message.reply_to_message.from_user.first_name), reply_markup=markup)
    elif(arg):
        bot.send_message(message.chat.id, poll.format(arg), reply_markup=markup)
    else:
        bot.reply_to(message, poll.format(message.from_user.first_name), reply_markup=markup)

@bot.message_handler(func=is_title)
def answer_title(message):
    if(not verify_chat(message)):
        return()
    keyboard_hider = types.ReplyKeyboardHide(selective=True)
    text='ok'
    title=message.text

    delete=0
    if(title[0]=='-'):
        delete=1
        title=title[1:]

    con = sql.connect(db)
    with con:
        cur = con.cursor()
        user=message.from_user
        print(str(user.id), user.first_name, user.last_name, user.username, title)
        cur.execute("delete from titles where user={} and title='{}'".format(str(user.id), title))
        if(not delete):
            cur.execute("INSERT INTO titles VALUES ({}, '{}', '{}', '{}', '{}')".format(str(user.id), user.first_name, user.last_name, user.username, title))

    bot.reply_to(message, text, reply_markup=keyboard_hider)
    new_title=get_pop_title()
    myachat=bot.get_chat(mya)
    old_title=myachat.title
    if(not (new_title==old_title)):
        bot.send_message(myachat.id, "У нас новое название чата: {} -> {}\n Голосовать за названия можно тут: https://telegram.me/joinchat/EAIp5Ai9Q64iuZ7AK_UnkA".format(old_title, new_title))
        bot.send_message(message.chat.id, "У нас новое название основного чата: {} -> {}".format(old_title, new_title))
        subprocess.call(["telegram-cli", "-DCWe", "rename_channel {} {}".format("channel#1053711520", new_title)])
        print("rename_channel {} {}".format(old_title, new_title))


@bot.message_handler(func=is_soctype)
def answer(message):
    if(not verify_chat(message)):
        return(n)
    soctype=message.text[1:]
    keyboard_hider = types.ReplyKeyboardHide(selective=True)
    text='ok'
    if(soctype.startswith('дон')):
         text='Малаца, так держать!'
    if(soctype.startswith('еся')):
         text='Маленькая есечка, уииии!'
    if(soctype.startswith('гек')):
         text='Опасайся злобной блуд!'
    if(soctype.startswith('гек') and message.from_user.username=='BlaBla7'):
         text='Опасайся злобной блуд! А. ты ж и есть злобная блуд...'
    if(message.from_user.first_name=='gr'):
        if(soctype.startswith('еся')):
            text=text+' Правду говорить легко и приятно!'
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
        print(str(user.id), user.first_name, user.last_name, user.username, soctype)
        cur.execute("INSERT INTO soctypes VALUES ({}, '{}', '{}', '{}', '{}', 'None')".format(str(user.id), user.first_name, user.last_name, user.username, soctype))


    bot.reply_to(message, text, reply_markup=keyboard_hider)

@bot.message_handler(func=is_pitype)
def pianswer(message):
    if(not verify_chat(message)):
        return()
    keyboard_hider = types.ReplyKeyboardHide(selective=True)
    text='ok'
    pitype=message.text[1:]

    con = sql.connect(db)
    with con:
        cur = con.cursor()
        user=message.from_user
        cur.execute("delete from pitypes where user=" +str(user.id))
        print(str(user.id), user.first_name, user.last_name, user.username, pitype)
        cur.execute("INSERT INTO pitypes VALUES ({}, '{}', '{}', '{}', '{}')".format(str(user.id), user.first_name, user.last_name, user.username, pitype))

    bot.reply_to(message, text, reply_markup=keyboard_hider)


@bot.message_handler(content_types=['sticker'])
def stick(message):
    print(message.sticker)

@bot.message_handler(regexp='!.*')
def mystick(message):
    stickers={
            '!попкорн': 'BQADAgADvA8AAp7OCwABDNdhX3eVtr4C',
            '!ойвсё': 'BQADAgADtCMAAlOx9wNFyM-lafn4dQI',
            '!плак': 'BQADAgADWwAD49KZAsojCYhAOXP-Ag',
            }
    stickername=message.text
    if(stickername in stickers):
        bot.send_sticker(message.chat.id, stickers[stickername])

@bot.message_handler(content_types=['left_chat_member'])
def userleft(message):
    print("Left: {}".format(message.left_chat_member.__dict__))

@bot.message_handler(content_types=['new_chat_member'])
def userjoined(message):
    print("Joined: {}".format(message.new_chat_member.__dict__))

if __name__ == '__main__':
    bot.polling(none_stop=True)
