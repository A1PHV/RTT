import Word2Vec
import telebot
from telebot import types
import os

badwordfile = open("badwords").readlines()
bot = telebot.TeleBot('5752360265:AAGynQkWK2msj2CTMK3WU0_D0YxRp07bWPw')
lemm_message = []
bad_words = []
koeffter = 0
Neuronet = Word2Vec.Neuro()
Neuronet.ML()

def cnt(msg):
    count = 0
    for i in msg:
        try:
            if Neuronet.ret_similarity(i)[0] in badwordfile:
                bad_words.append(i[0])
                count += 1
        except:
            count += 0.5
    return count

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Проверить сообщение на опасность!")
    btn2 = types.KeyboardButton("Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Здравствуйте, чем я могу вам помочь?".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Проверить сообщение на опасность!"):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("Отправить пересланное сообщение")
        btn4 = types.KeyboardButton("Отправить сообщение")
        markup1.add(btn3, btn4)
        bot.send_message(message.chat.id, text="В каком виде будет отправлено сообщение?".format(message.from_user), reply_markup=markup1)
    elif (message.text == "Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Какая цель в твоей работе?")
        btn2 = types.KeyboardButton("Как анализировать текст?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "Какая цель в твоей работе?"):
        bot.send_message(message.chat.id,  text = "Я высокотехнологичная машина, которую научили понимать опасность в сообщениях! Можете отправить мне файл с текстом или само сообщение в другом разделе, и я подскажу вам, грозит ли опасность.")

    elif (message.text == "Отправить сообщение") or (message.text == "Отправить пересланное сообщение"):
        bot.send_message(message.chat.id,  text = "Все готово к приему сообщения. Чтобы вернуться обратно, напишите: 'Главное меню'.", reply_markup=types.ReplyKeyboardRemove())

    elif message.text == "Как анализировать текст?":
        bot.send_message(message.chat.id, text="Все очень просто: вернитсь в главное меню и нажмите на кнопочку 'Проверить сообщение на опасность!', далее выберите нужный вам способ.")

    elif (message.text == "Вернуться в главное меню") or (message.text == "Главное меню") or (message.text == "Гм"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Проверить сообщение на опасность!")
        button2 = types.KeyboardButton("Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="Я проанализирую это!")
        lemm_message = Neuronet.lemmatize(str(message))
        koeffter = (cnt(lemm_message) / len(message.text)) * 100
        bot.send_message(message.chat.id, text="В тексте были найдены такие слова как:\n")
        for word in bad_words:
            bot.send_message(message.chat.id, text=word)
        bot.send_message(message.chat.id, text="Процент угрозы или возможности противоправных действий по моему алгоритму таков:\n")
        if koeffter >= 75:
            bot.send_message(message.chat.id, text="Сообщение имеет максимальный уровень угрозы. Надеемся, что мы смогли вам помочь и вы сможете быстро отреагировать на опасность.\n"
                                                   "Продолжите отправлять сообщения или напишите 'Главное меню'")
        elif koeffter < 75 and koeffter >= 50:
            bot.send_message(message.chat.id, text="Сообщение имеет средний уровень угрозы. Надеемся, что мы смогли вам помочь и вы сможете быстро отреагировать на опасность.\n"
                                                   "Продолжите отправлять сообщения или напишите 'Главное меню'")
        elif koeffter < 50 and koeffter >= 25:
            bot.send_message(message.chat.id, text="Сообщение имеет низкий уровень угрозы. Надеемся, что мы смогли вам помочь и вы сможете быстро отреагировать на опасность.\n"
                                                   "Продолжите отправлять сообщения или напишите 'Главное меню'")
        elif koeffter < 25:
            bot.send_message(message.chat.id, text="Сообщение имеет безопасный уровень угрозы. Надеемся, что мы смогли вам помочь и вы сможете быстро отреагировать на опасность.\n"
                                                   "Продолжите отправлять сообщения или напишите 'Главное меню'")
        koeffter = 0

bot.polling(none_stop=True)