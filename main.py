import telebot
import constaints
import pars


bot = telebot.TeleBot(constaints.token)
upd = bot.get_updates()
last_upd = upd[-1]
message_from_user = last_upd.message


@bot.message_handler(commands=['start'])
def user_keyboard(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/start')
    user_markup.row('События сегодня', 'События завтра')
    bot.send_message(message.from_user.id, 'Hi', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def options(message):
    if message.text == 'События сегодня':
        today_data = pars.today()
        answer(message, today_data)
    elif message.text == 'События завтра':
        tomorrow_data = pars.tomorrow()
        answer(message, tomorrow_data)


def answer(message, get_data):
    if get_data is None:
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так. Попробуйте снова.')
    else:
        for event_info in get_data:
            bot.send_message(message.from_user.id, f"""
    <b>{event_info[1]}</b>

{event_info[2]}
Цена: {event_info[3]}
Начало события: {event_info[4]}
Место: {event_info[5]}

<a href='{event_info[-1]}'>Изображение</a>          
                    """, parse_mode='HTML', reply_markup=get_inline_keyboard(event_info[0]))


def get_inline_keyboard(event_info):
    inline = telebot.types.InlineKeyboardMarkup()
    keyboard = telebot.types.InlineKeyboardButton(text='Перейти на сайт', url=event_info)
    inline.add(keyboard)
    return inline


bot.polling(none_stop=True, interval=0)
