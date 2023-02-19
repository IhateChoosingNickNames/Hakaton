import datetime

import telebot
from django.core.management import BaseCommand
from telebot import types

from recipes.exceptions import WrongInputError
from recipes.views import get_recipe, add_recipe, get_random_recipe, get_types, get_categories
from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv("TG_BOT")
bot = telebot.TeleBot(SECRET_KEY)


commands = ["/get_recipe", "/add_recipe", "/menu", "/greet", "/get_random_recipe"]
recipe = {"params": None}
TIME_OUT = {"last_time_called": None, "delay": datetime.timedelta(seconds=30)}


class Command(BaseCommand):
    """Команда для запуска бота."""

    help = "Команда для запуска бота python manage.py bot"

    def handle(self, *args, **options):
        """Инциализация бота."""
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()

    @bot.message_handler(commands=['greet'])
    def greet(self):
        """Фунция приветствия."""
        bot.delete_message(self.chat.id, self.message_id)
        bot.send_message(self.chat.id, f'Greetings, <tg-spoiler>Unknown User</tg-spoiler> !', parse_mode='HTML')

    @bot.message_handler(commands=["get_random_recipe"])
    def get_random_recipe(self):
        bot.delete_message(self.chat.id, self.message_id)
        rnd_recipe = get_random_recipe()
        bot.send_message(self.chat.id, f'***Рандомный рецепт - {rnd_recipe.title}.***', parse_mode='MARKDOWN')
        bot.send_message(self.chat.id, f'{rnd_recipe.text}', parse_mode='HTML')

    @bot.message_handler(commands=['get_recipe'])
    def get_recipe(self, show=True):
        """Функция получения рецентов."""
        bot.delete_message(self.chat.id, self.message_id)
        params = self.text.replace('/get_recipe', '').lstrip()

        if params != "":
            try:
                parsed = parse_input(params)
            except WrongInputError:
                bot.send_message(self.chat.id, "Введены некорретные данные")
            else:
                result = get_recipe(parsed)
                if result:
                    for index, elem in enumerate(result):
                        bot.send_message(self.chat.id, f'***{index + 1}. Название рецепта: {elem.title}***', parse_mode='MARKDOWN')
                        bot.send_message(self.chat.id, f'{elem.text}', parse_mode='HTML')
                else:
                    bot.send_message(self.chat.id, f'К сожалению, у нас пока нет рецепта с такими параметрами, попробуйте ввести другие параметры', parse_mode='HTML')
        else:
            sent = bot.send_message(self.chat.id, f'Укажите <b>категорию</b>(обязательно), <b>тип</b>(опционально), <b>количество</b>(опционально) через звездочку. Пример: <b>супы*сырный суп*5</b>', parse_mode='HTML')

            show_available_cats_and_types(self)

            bot.register_next_step_handler(sent, Command.get_recipe)

    @bot.message_handler(commands=['add_recipe'])
    def add_recipe(self):
        """Функция добавления рецентов."""
        bot.delete_message(self.chat.id, self.message_id)
        sent = bot.send_message(self.chat.id, f'Введите <b>категорию</b>, <b>тип</b>, <b>название</b> через звездочку. Все поля обязательные. Пример: <b>супы*сырный суп*название супа</b>', parse_mode='HTML')
        show_available_cats_and_types(self)
        bot.register_next_step_handler(sent, Command.params_maker)

    def params_maker(self):
        """Функция получения параметров для рецепта."""
        recipe["params"] = self.text
        sent = bot.send_message(self.chat.id, f'Введите рецепт:', parse_mode='HTML')
        bot.register_next_step_handler(sent, Command.recipe_maker)

    def recipe_maker(self):
        """Функция создания рецентов."""

        try:
            parsed = parse_input(recipe["params"])
        except WrongInputError:
            bot.send_message(self.chat.id, "Введены некорретные данные")
        else:
            parsed["text"] = self.text

            try:
                res = add_recipe(parsed)
                bot.send_message(self.chat.id, f'Рецепт успешно создан!', parse_mode='HTML')
            except WrongInputError:
                bot.send_message(self.chat.id, f'Введены некорретные данные.', parse_mode='HTML')

    @bot.message_handler(commands=['menu'])
    def menu(self):
        """Функция получения списка доступных команд."""
        bot.delete_message(self.chat.id, self.message_id)
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        kb.add(*[types.KeyboardButton(text=elem) for elem in commands])
        bot.send_message(self.chat.id, 'Доступные команды:', reply_markup=kb)

    @bot.message_handler(func=lambda x: x not in commands)
    def wrong(self):
        """Функция ответа на некорретно введенную команду."""
        bot.reply_to(self, 'Введена некорретная команда.')

def parse_input(data):
    data = data.split("*")
    result = {"category": None, "type_": None, "amount": None, "title": None}

    try:
        tmp = int(data[-1])
    except ValueError:
        pass
    else:
        result["amount"] = tmp
        del data[-1]

    if not data:
        raise WrongInputError

    result["category"] = data[0]
    del data[0]

    if data:
        result["type_"] = data[0]
        del data[0]

    if data:
        result["title"] = data[0]
        del data[0]

    return result


def show_available_cats_and_types(self):
    if TIME_OUT["last_time_called"] is not None and datetime.datetime.now() - TIME_OUT["last_time_called"] < TIME_OUT["delay"]:
        return None

    TIME_OUT["last_time_called"] = datetime.datetime.now()

    cats = get_categories()
    recipe_types = get_types()

    bot.send_message(self.chat.id, f'<b>Список доступных категорий</b>:',
                     parse_mode='HTML')
    for index, elem in enumerate(cats):
        bot.send_message(self.chat.id, f'{index + 1}. <i>{elem.title}</i>',
                         parse_mode='HTML')

    bot.send_message(self.chat.id, f'<b>Список доступных типов</b>:',
                     parse_mode='HTML')
    for index, elem in enumerate(recipe_types):
        bot.send_message(self.chat.id, f'{index + 1}. <i>{elem.title}</i>',
                         parse_mode='HTML')