from telebot import types, TeleBot
from datetime import datetime
from threading import Thread
from loguru import logger
from SimpleQIWI import *
from config import *
import timedelta
import Bomber
import sqlite3
import random
import sys

class sql_db:
    def __init__(self, data_base: sqlite3.Connection):
        self.db = data_base

    def select_one(self, *args, **kwargs):
        return self._select(self.db.execute(*args, **kwargs).fetchone(), True)

    def select_all(self, *args, **kwargs):
        return self._select(self.db.execute(*args, **kwargs).fetchall())

    def select_all_first(self, *args, **kwargs):
        if out := self.select_all(*args, **kwargs):
            return [item for item in out]
        else:
            return

    @staticmethod
    def _select(info, first_item: bool = False):
        if info is None:
            return
        elif len(info) == 1 and info[0] is None:
            return
        elif first_item and len(info) == 1:
            return info[0]
        return info

    def exec(self, *args, **kwargs):
        out = self.db.execute(*args, **kwargs)
        self.db.commit()
        return out

    def execute(self, *args, **kwargs):
        return self.db.execute(*args, **kwargs)

    def commit(self):
        return self.db.commit()


db = sql_db(sqlite3.connect('data_base.db', check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES))
db.exec('CREATE TABLE IF NOT EXISTS users (id INT, is_premium INT, is_adm INT, free_try int, is_banned int, prem_data timeobj)')
logger.add('debug.log', level='DEBUG', rotation='100 MB')
bot = TeleBot(BOT_TOKEN, parse_mode='HTML')
logger.info('Start up system...')
phones_in_spam = list()
ids_in_spam = list()
lite_limit = [{'id': 0, 'time': datetime(2021, 8, 14, 13, 0, 36, 681128)}]

@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message, is_human=False):
    user_id = message.chat.id
    logger.info(f'User {user_id} - /start')
    if not db.select_one('SELECT * from users WHERE id = ?', (user_id,)):
        if is_human == 0:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            random_button = random.randrange(0, 3)
            for i in range(3):
                if i == random_button:
                    keyboard.add(types.InlineKeyboardButton(text='✅', callback_data='pass'))
                else:
                    keyboard.add(types.InlineKeyboardButton(text='❌', callback_data='deny'))
            bot.send_message(user_id, '<b>Подтвердите что вы не робот - нажмите ✅</b>', reply_markup=keyboard)
            return
        else:
            save_user(user_id)
    if is_banned(user_id):
        bot.send_message(user_id, '<b>Вы заблокированны в этом боту :( </b>')
        return
    if is_premium(user_id):
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton('SMS Бомбер(premium) 📨', callback_data='private_bomber'),
            types.InlineKeyboardButton('Call бомбер 📞', callback_data='call_bomber'),
            types.InlineKeyboardButton('Информация 🤔', callback_data='info'),
            types.InlineKeyboardButton('Статистика 📈', callback_data='stats'))
        bot.send_message(chat_id=user_id, text=f'<b>Добро пожаловать в главное меню!\nВаша подписка активна до: {datetime.strptime(db.select_one("SELECT prem_data FROM users WHERE id = ?", (user_id,)), "%Y-%m-%d %H:%M:%S.%f").strftime("%B %d, %Y")}</b>', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton('SMS Бомбер(lite) 📨', callback_data='free'),
            types.InlineKeyboardButton('Информация 🤔', callback_data='info'),
            types.InlineKeyboardButton('Получить premium 💣', callback_data='premium'),
            types.InlineKeyboardButton('Статистика 📈', callback_data='stats'))

        bot.send_message(chat_id=user_id, text='<b>Добро пожаловать в главное меню!</b>', reply_markup=keyboard)

@bot.message_handler(commands=['adm'])
def adm_panel(message):
    user_id = message.chat.id
    logger.info(f'User {user_id} - /adm')
    if db.select_one('SELECT is_adm FROM users WHERE id = ?', (user_id,)):
        keyboard = types.InlineKeyboardMarkup(row_width=2).add(
                             types.InlineKeyboardButton('Выдать доступ', callback_data='add_usr'),
                             types.InlineKeyboardButton('Забрать доступ', callback_data='dell_usr'),
                             types.InlineKeyboardButton('Рассылка', callback_data='mailing'),
                             types.InlineKeyboardButton('Вернутся в меню', callback_data='menu'),
                             types.InlineKeyboardButton('Отключить бота', callback_data='off'))
        bot.send_message(message.chat.id, 'Добро пожаловать в админ панель!', reply_markup=keyboard)
    else:
        bot.send_message(user_id, '<b>Вы не являетесь администратором данного бота!</b>')

@bot.message_handler(content_types=['text'])
def idkcommand(message: types.Message):
    user_id = message.chat.id
    if '/' in message.text:
        bot.send_message(user_id, '<b>Неизвестная команда, для запуска бота введите /start</b>')
    else:
        bot.send_message(user_id, '<b>Я вас не понял, для запуска бота введите /start</b>')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: types.CallbackQuery):
    message = call.message
    user_id = message.chat.id
    data = call.data
    message_id = message.message_id
    return_keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Вернуться в главное меню', callback_data='menu'))
    logger.info(f'User {user_id} - callbackdata={data}')
    if is_banned(user_id):
        bot.send_message(user_id, '<b>Вы заблокированны в этом боту :( </b>')
        return

    if data == 'stats':
        bot.edit_message_text(
            f'<b>Статистика отображается в реальном времени!\nПользователей‍: {str(db.select_one("SELECT COUNT(id) FROM users"))}</b>\n',
            user_id, message_id, reply_markup=return_keyboard)
        return

    elif data == 'mailing':
        bot.edit_message_text(text='Введите текст рассылки', chat_id=user_id, message_id=message_id)
        bot.register_next_step_handler(message, mailing_step1)
        return

    elif data == 'add_usr':
        bot.edit_message_text(text='Введите id пользователя, которому вы хотите выдать премиум доступ, и через пробел кол-во месяцев.', chat_id=user_id, message_id=message_id)
        bot.register_next_step_handler(message, add_usr)
        return

    elif data == 'dell_usr':
        bot.edit_message_text(text='Введите id пользователя, у которого вы хотите отнять премиум доступ', chat_id=user_id, message_id=message_id)
        bot.register_next_step_handler(message, dell_usr)
        return

    elif data == 'call_bomber':
        bot.edit_message_text(f'Вы в меню Call Bomber. Данный бомбер только для российских номеров!\nСейчас идут тестирование данного бомбера, при возникновений писать {OWNER_TAG} \nМаксимальное время спама 2880 минут\n\n'
                              'Введите номер без "+" в формате:\n'
                              '🇷🇺 79**********\n'
                              'И количество минут cпама.\n'
                              'Пример: 7800353555 60', user_id, message_id, reply_markup=return_keyboard)
        bot.register_next_step_handler(message, call_bomber)
        return

    elif data == 'menu':
        bot.clear_step_handler_by_chat_id(user_id)
        bot.delete_message(user_id, message_id)
        start_command_handler(message)
        return

    elif call.data == 'info':
        bot.edit_message_text(
            f'Владелец бота: {OWNER_TAG}\n\nПо вопросам сотрудничества обращаться в ЛС\n\nНаш канал: <b><a href="{CHANEL_LINK}">тык</a></b>\n\n',
            user_id, message_id, reply_markup=return_keyboard)
        return

    elif data == 'premium':
        payment_keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton('Перейти на страницу оплаты', url='qiwi.com/n/CODESAFETY'), types.InlineKeyboardButton('Проверить платеж', callback_data='check_payment'))
        bot.edit_message_text(f'<b>❗️ Для приобретения V.I.P. подписки на 1 месяц переведите {price} рублей с комментарием: {user_id}\n\n❗️ Возможна оплата на Яндекс.Деньги или BTC.\nДля этого напишите мне {OWNER_TAG}\n\nЕсли Вы перевели деньги с другим комментариями, то доступ вы не получите!\n\nПроблемы? Пиши 👉🏻 {OWNER_TAG}</b>', user_id, message_id,
                              reply_markup=payment_keyboard)

    elif data == 'private_bomber':
        bot.edit_message_text('Вы в V.I.P. версии бомбера. Максимальное время спама 2880 минут\n\n'
                              'Введите номер без "+" в формате:\n'
                              '🇺🇦 380*********\n'
                              '🇷🇺 79**********\n'
                              '🇰🇿 77*********\n'
                              'И количество минут cпама.\n'
                              'Пример: 7800353555 60', user_id, message_id, reply_markup=return_keyboard)
        bot.register_next_step_handler(message, private_bomber)

    elif data == 'check_payment':
        donat(message)
        return

    elif data == 'free':
        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, 'Вы в демо-версии бомбера. Доступное время спама : 5 минут \n\n'
                                  'Введите номер без "+" в формате:\n'
                                  '🇺🇦 380*********\n'
                                  '🇷🇺 79**********\n'
                                  '🇰🇿 77*********\n', reply_markup=return_keyboard)
        bot.register_next_step_handler(message, free_spam)
        return

    elif data == 'pass':
        bot.edit_message_text('Вы успешно прошли проверку!', user_id, message_id)
        start_command_handler(message, is_human=1)
        return

    elif data == 'deny':
        bot.edit_message_text('<b>Думаю, тут пахнет обманом \n/start для новой попытки</b>', user_id, message_id)
        return
    elif data == 'off':
        logger.critical('Отключен...')
        bot.stop_polling()
        sys.exit()

    else:
        if data in phones_in_spam:
            try:
                phones_in_spam.remove(data)
            except Exception:
                pass
            try:
                ids_in_spam.remove(user_id)
            except Exception:
                pass

            bot.edit_message_text(f'Спам на номер {data} останавливается...', message_id=message_id, chat_id=user_id,
                                  reply_markup=return_keyboard)
            return
        else:
            bot.edit_message_text(f'Спам на номер {data} уже был остановлен...', message_id=message_id, chat_id=user_id,
                                  reply_markup=return_keyboard)
        return

def donat(message):
    chat_id = message.chat.id
    message_id = message.message_id
    payment_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton('Перейти на страницу оплаты', url='qiwi.com/n/CODESAFETY'),
        types.InlineKeyboardButton('Проверить платеж', callback_data='check_payment'))

    bot.edit_message_text(f'<b>Проверяем платеж, ожидайте{random.choice(list("🐶🐱🐭🐹🐰🦊🐻🐻‍❄️🐼🐨🐯🦁🐧🐔🐦🐤🐥🐥🦅"))}</b>', chat_id, message_id, reply_markup=payment_keyboard)

    i = 0
    for el in QApi(tokenusr, phoneusr).payments['data']:
        comment = el['comment']
        if comment == str(chat_id) and el['sum']['amount'] >= price:
            db.exec("UPDATE users SET prem_data = ?, is_premium = 1 WHERE id = ?", (datetime.strftime(datetime.now() + timedelta.Timedelta(days=30), "%Y-%m-%d %H:%M:%S.%f"), chat_id,))
            bot.edit_message_text('✅ Платеж найден! Пропишите /start для обновление данных', chat_id, message_id)
            return
        if (i := i + 1) >= 10:
            break
    bot.edit_message_text(f'🛑 Оплата не была найдена!\n\n Проблемы с оплатой? Отпиши {OWNER_TAG}', chat_id, message_id, reply_markup=payment_keyboard)

def mailing_step1(message):
    user_id = message.chat.id
    text = message.text
    keyboard = types.ReplyKeyboardMarkup().add(types.KeyboardButton(text='Пропустить'))
    bot.send_message(user_id, 'Теперь введите данные кнопки в формате:\n*ТЫК* t.me/hentai', reply_markup=keyboard)
    bot.register_next_step_handler(message, mailing_step2, text)


def mailing_step2(message, mailing_text):
    user_id = message.chat.id
    text = message.text
    if not text == 'Пропустить':
        button_url = text.split(' ')[-1:][0]
        button_text = text[:-len(button_url)]
        mailing_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text=button_text, url=button_url))
        keyboard = types.ReplyKeyboardMarkup().add(types.KeyboardButton(text='Пропустить'))
        bot.send_message(user_id, 'Теперь введите ссылку на фотографию', reply_markup=keyboard)
    else:
        mailing_keyboard = False
        keyboard = types.ReplyKeyboardMarkup().add(types.KeyboardButton(text='Пропустить'), types.KeyboardButton(text='Отменить'))
        bot.send_message(user_id, 'Теперь введите ссылку на фотографию', reply_markup=keyboard)
    bot.register_next_step_handler(message, mailing_step3, mailing_text, mailing_keyboard)


def mailing_step3(message, mailing_text, mailing_keyboard):
    user_id = message.chat.id
    text = message.text
    if text == 'Пропустить':
        photo = False
    elif text == 'Отменить':
        bot.send_message(user_id, 'Рассылка отменена')
        return
    else:
        photo = text
    Thread(target=mailing_step4, args=(message, mailing_text, mailing_keyboard, photo,), daemon=False).start()

def mailing_step4(message, mailing_text, mailing_keyboard, photo):
    user_id = message.chat.id
    users = db.select_all_first("SELECT id FROM users")
    true_mailing = 0
    false_mailing = 0
    try:
        if photo and mailing_keyboard:
            bot.send_photo(user_id, photo, mailing_text, reply_markup=mailing_keyboard)
        if photo and not mailing_keyboard:
            bot.send_photo(user_id, photo, mailing_text)
        if not photo and mailing_keyboard:
            bot.send_message(user_id, mailing_text, reply_markup=mailing_keyboard)
        if not photo and not mailing_keyboard:
            bot.send_message(user_id, mailing_text)
    except Exception as Error:
        logger.critical(Error)
        bot.send_message(user_id, f'Ошибка при рассылке. Текст рассылки: {Error}')

    bot.send_message(user_id, 'Удаление клавиатуры', reply_markup=types.ReplyKeyboardRemove())

    if mailing_text and photo and mailing_keyboard:
        for uid in users:
            try:
                bot.send_photo(uid[0], photo, mailing_text, reply_markup=mailing_keyboard)
                true_mailing += 1
            except:
                false_mailing += 1
    elif mailing_text and mailing_keyboard and not photo:
        for uid in users:
            try:
                bot.send_message(uid[0], mailing_text, reply_markup=mailing_keyboard)
                true_mailing += 1
            except:
                false_mailing += 1
    elif mailing_text and photo and not mailing_keyboard:
        for uid in users:
            try:
                bot.send_photo(uid[0], photo, mailing_text)
                true_mailing += 1
            except:
                false_mailing += 1
    elif mailing_text and not photo and not mailing_keyboard:
        for uid in users:
            try:
                bot.send_message(uid[0], mailing_text)
                true_mailing += 1
            except:
                false_mailing += 1

    bot.send_message(message.chat.id, f"Разослано успешно: {true_mailing}\nНЕуспешно: {false_mailing}")


def dell_usr(message):
    user_id = message.chat.id
    text = message.text
    if is_admin(user_id):
        if text.isdigit():
            db.exec("UPDATE users SET is_premium = 0 WHERE id = ?", (int(text),))
            save_user(user_id)
            bot.send_message(int(text), 'У вас отжали доступ')
            bot.send_message(user_id, f'Пользователь {text} потерял доступ')
        else:
            bot.send_message(user_id, 'Это не chat id!')
    else:
        bot.send_message(user_id, 'Вы не являетесь администратором!')


def add_usr(message, is_buy=0):
    user_id = message.chat.id
    text = message.text
    if is_admin(user_id):
        if text.split(' ')[0].isdigit():
            try:
                save_user(int(text.split(' ')[0]))
                db.exec("UPDATE users SET prem_data = ?, is_premium = 1 WHERE id = ?", (datetime.strftime(datetime.now()+timedelta.Timedelta(days=int(text.split(' ')[1])*30), "%Y-%m-%d %H:%M:%S.%f"), int(text.split(" ")[0]),))
                bot.send_message(int(text.split(" ")[0]), f'Вы получили премиум доступ к данному боту на {text.split(" ")[1]} месяц(а)!')
                bot.send_message(user_id, f'Пользователь {text} получил доступ')
            except Exception as Error:
                logger.critical(Error)
                bot.send_message(user_id, f'Ошибка! \n{Error}')
        else:
            bot.send_message(user_id, 'Это не chat id!')
    else:
        bot.send_message(user_id, 'Вы не являетесь администратором!')


def start_spam(message, end_data, target, spam_type):
    user_id = message.chat.id
    if spam_type == 'lite':
        free_try = db.select_one('SELECT free_try FROM users WHERE id = ?', (user_id, ))
        if free_try >= 3:
            bot.send_message(user_id, '<b>К сожелению, вы использовали лимит бесплатного бомбера. Приобретите подписку для дальнейшего использования бота.</b>')
            return
        else:
            db.exec('UPDATE users SET free_try = ? WHERE id = ?', (free_try+1, user_id,))
    ids_in_spam.append(user_id)
    phones_in_spam.append(target)
    keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='STOP ❌', callback_data=target))
    bot.send_message(message.chat.id, f'<b>Жертва : </b><i>{target}\n</i><b>Остановится в </b><i>{str(end_data)[:-7]}</i>\nСпам запущен!', reply_markup=keyboard)
    logger.info(f'User {user_id}, Target {target}. TimeStamp {datetime.now()}, Start spam')
    if target.isdigit():
        if target[:1] == '7':
            if spam_type == 'lite':
                while datetime.now() <= end_data and target in phones_in_spam:
                    Bomber.Bomber(target).start_lite()
            else:
                while datetime.now() <= end_data and target in phones_in_spam:
                    Bomber.Bomber(target).start()
    else:
        bot.send_message(user_id, f'<b>Произошла ошибка при запуске потока, повторите попытку или обратитесь к нам: {OWNER_TAG}')
    try:
        ids_in_spam.remove(user_id)
    except:
        pass
    try:
        phones_in_spam.remove(target)
    except:
        pass
    logger.info(f'User {user_id}, Target {target}. TimeStamp {datetime.now()}, Spam was stopped')
    bot.send_message(user_id, f'Спам на {target} был остановлен')

def pformat(phone: str, mask: str, mask_symbol: str = "*") -> str:
    formatted_phone: str = ""
    for symbol in mask:
        if symbol == mask_symbol:
            formatted_phone += phone[0]
            phone = phone[(len(phone) - 1) * -1:]
        else:
            formatted_phone += symbol
    return formatted_phone

def call_spam(message, end_data, target):
    user_id = message.chat.id
    if not target[:2] == '79':
        bot.send_message(user_id, 'Это не российский номер!')
        return
    ids_in_spam.append(user_id)
    phones_in_spam.append(target)
    keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='STOP ❌', callback_data=target))
    bot.send_message(message.chat.id, f'<b>Жертва : </b><i>{target}\n</i><b>Остановится в </b><i>{str(end_data)[:-7]}</i>\nСпам запущен!', reply_markup=keyboard)
    logger.info(f'Target {target}. Spam was started...')
    if target.isdigit():
        while datetime.now() <= end_data and target in phones_in_spam:
            Bomber.Bomber(target).start_call()
    try:
        ids_in_spam.remove(user_id)
    except:
        pass
    try:
        phones_in_spam.remove(target)
    except:
        pass
    logger.info(f'Target {target}. Spam was stopped...')
    bot.send_message(user_id, f'Спам на {target} был остановлен')


def call_bomber(message):
    user_id = message.chat.id
    text = message.text
    return_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Вернуться в главное меню', callback_data='menu'))
    try:
        data = text.split(' ')
        if len(data) == 2:
            phone = phone_format(data[0])
            timer = int(data[1])
        else:
            bot.send_message(user_id, 'Возможно вы забыли указать время спама', reply_markup=return_keyboard)
            return
    except:
        bot.send_message(user_id, 'Я вас не понял', reply_markup=return_keyboard)
        return

    if is_premium(user_id):
        if phone not in phones_in_spam:
            if ids_in_spam.count(user_id) <= 5:
                if phone.isdigit() and 11 <= len(phone) <= 13:
                    if timer <= 2881:
                        Thread(target=call_spam, args=(message, datetime.now() + timedelta.Timedelta(minutes=timer), phone)).start()
                    else:
                        bot.send_message(user_id, '🛑 Максимальное время спама 2880 минут!', reply_markup=return_keyboard)
                else:
                    bot.send_message(user_id, '🛑 Неверный номер', reply_markup=return_keyboard)
            else:
                bot.send_message(user_id, '🛑 Запрещенно больше 5 сессий спама!', reply_markup=return_keyboard)
        else:
            bot.send_message(message.chat.id, '🛑 На данный номер уже запущен спам.', reply_markup=return_keyboard)
    else:
        bot.send_message(message.chat.id, '🛑 Произошла ошибка при проверке премиума', reply_markup=return_keyboard)

def private_bomber(message):
    user_id = message.chat.id
    text = message.text
    return_keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Вернуться в главное меню', callback_data='menu'))
    try:
        data = text.split(' ')
        if len(data) == 2:
            phone = phone_format(data[0])
            timer = int(data[1])
        else:
            bot.send_message(user_id, 'Возможно вы забыли указать время спама', reply_markup=return_keyboard)
            return
    except:
        bot.send_message(user_id, 'Я вас не понял!', reply_markup=return_keyboard)
        return

    if is_premium(user_id):
        if phone not in phones_in_spam:
            if ids_in_spam.count(user_id) <= 5:
                if phone.isdigit() and 11 <= len(phone) <= 13:
                    if timer <= 2881:
                        Thread(target=start_spam, args=(message, datetime.now() + timedelta.Timedelta(minutes=timer), phone, 'premium',)).start()
                    else:
                        bot.send_message(user_id, '🛑 Максимальное время спама 2880 минут!', reply_markup=return_keyboard)
                else:
                    bot.send_message(user_id, '🛑 Неверный номер', reply_markup=return_keyboard)
            else:
                bot.send_message(user_id, '🛑 Запрещенно больше 5 сессий спама!', reply_markup=return_keyboard)
        else:
            bot.send_message(message.chat.id, '🛑 На данный номер уже запущен спам.', reply_markup=return_keyboard)
    else:
        bot.send_message(message.chat.id, '🛑 Произошла ошибка при проверке премиума', reply_markup=return_keyboard)


def free_spam(message):
    user_id = message.chat.id
    text = message.text
    return_keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Вернуться в главное меню', callback_data='menu'))
    phone = phone_format(text)
    if phone.isdigit() and 11 <= len(text) <= 13:
        if user_id not in ids_in_spam:
            if phone not in phones_in_spam:
                lite_limit.append({'id': user_id, 'time': datetime.now()+timedelta.Timedelta(hours=1)})
                Thread(target=start_spam,
                       args=(message, datetime.now() + timedelta.Timedelta(minutes=5), phone, 'lite',)).start()
            else:
                bot.send_message(message.chat.id, '🛑 На данный номер уже запущен спам.',
                                 reply_markup=return_keyboard)
        else:
            bot.send_message(message.chat.id, '🛑 Вы уже имеете активную атаку!', reply_markup=return_keyboard)
    else:
        bot.send_message(user_id, '🛑 Неверный номер', reply_markup=return_keyboard)


def phone_format(phone):
    formatted = [elem for elem in phone if elem.isdigit()]
    phone = ''
    for elem in formatted:
        phone += elem
    if phone[:1] == '8':
        return '7' + phone[1:]
    return phone

def is_banned(user_id):
    return db.select_one('SELECT id FROM users WHERE id = ? and is_banned = 1', (user_id,))

def is_admin(user_id):
    return db.select_one('SELECT id FROM users WHERE id = ? and is_adm = 1', (user_id,))

def is_premium(user_id):
    if db.select_one('SELECT is_premium FROM users WHERE id = ?', (user_id,)) == 1:
        if not datetime.strptime(db.select_one('SELECT prem_data FROM users WHERE id = ?', (user_id,)), "%Y-%m-%d %H:%M:%S.%f") <= datetime.now():
            return True
        else:
            db.exec('UPDATE users SET is_premium = 0 WHERE id = ?', (user_id,))
            bot.send_message(user_id, '<b>Ваша премиальная подписка закончилась</b>')
            return False
    else:
        return False

def save_user(user_id):
    if not db.select_one('SELECT * FROM users WHERE id = ?', (user_id,)):
        db.exec('INSERT INTO users VALUES (?, 0, 0, 0, 0, 0)', (user_id,))


if __name__ == '__main__':
    start_time = datetime.now()
    logger.success(f'Киви успешно подключен! Баланс киви = {QApi(tokenusr, phoneusr).balance[0]}RUB')
    logger.success(f'Bot was successfully started, startup time : {start_time.strftime("%Y-%m-%d %H:%M:%S")}')
    bot.infinity_polling()
