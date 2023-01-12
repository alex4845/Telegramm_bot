import telebot
from telebot import types

bot = telebot.TeleBot('5917858144:AAHRyeAdLmAfuDsuZAAv5jUXs4U9cG3sa34')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Если ты хочешь участвовать в Open Call"
                                               " в Художественном Комбинате, то тебе необходимо зарегистрироваться."
                                               " Отправь 'да', если хочешь начать процесс регистрации")
    elif message.text == "да":
        bot.send_message(message.from_user.id, "Как твое имя?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Ну пока...")

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, f"Какая у тебя фамилия, {message.text}?")
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    age = message.text
    try:
        age = int(message.text)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Вы записаны. Мы вас известим дополнительно')
        print(name, surname, age)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Передумал?')


bot.polling(none_stop=True, interval=0)
