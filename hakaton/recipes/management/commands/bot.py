import datetime
import json

import requests
import telebot
from django.core.management import BaseCommand
from telebot import types

from hakaton import settings
from recipes.exceptions import WrongInputError
from recipes.views import get_recipe, add_recipe, get_random_recipe, get_types, get_categories, get_my_recipes
from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv("TG_BOT")
bot = telebot.TeleBot(SECRET_KEY)


commands = ["/get_recipe", "/add_recipe", "/menu", "/start", "/get_random_recipe", "/my_recipes"]
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

    @bot.message_handler(commands=['my_recipes'])
    def my_recipes(self):
        """Фунция приветствия."""
        bot.delete_message(self.chat.id, self.message_id)
        result = get_my_recipes(self.from_user.username)
        bot.send_message(self.chat.id, f'Вывожу посты пользователя {self.from_user.first_name}!', parse_mode='HTML')
        show_result(result, self)

    @bot.message_handler(commands=['start'])
    def start(self):
        """Фунция приветствия."""
        bot.delete_message(self.chat.id, self.message_id)
        bot.send_message(self.chat.id, f'Приветствую, {self.from_user.first_name}!', parse_mode='HTML')
        msg = bot.send_message(self.chat.id, f'Для продолжения работы введите: /menu', parse_mode='HTML')


    @bot.message_handler(commands=["get_random_recipe"])
    def get_random_recipe(self):
        bot.delete_message(self.chat.id, self.message_id)
        rnd_recipe = get_random_recipe()
        bot.send_message(self.chat.id, f'***Рандомный рецепт - {rnd_recipe.title}.***', parse_mode='MARKDOWN')
        bot.send_message(self.chat.id, f'Автор рецепта: <i>{rnd_recipe.author.last_name} {rnd_recipe.author.first_name}</i>, никнейм - <b>{rnd_recipe.author.username}</b>', parse_mode='HTML')
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
                show_result(result, self)
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
        sent = bot.send_message(self.chat.id, f'Загрузите картинку:', parse_mode='HTML')
        bot.register_next_step_handler(sent, Command.get_photo)

    def get_photo(self):
        url = f"https://api.telegram.org/bot{SECRET_KEY}/getFile?file_id={self.photo[-1].file_id}"

        res = requests.get(url)

        file_path = json.loads(res.content)["result"]["file_path"]

        template = f"https://api.telegram.org/file/bot{SECRET_KEY}/{file_path}"

        res = requests.get(template)

        with open("tmp.png", "wb") as file:
            file.write(res.content)

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
            parsed["author"] = validate_author_fields({"username": self.from_user.username, "first_name": self.from_user.first_name, "last_name": self.from_user.last_name})
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


def validate_author_fields(initital_data):
    validated_data = {}
    for key, value in initital_data.items():
        if value is not None:
            validated_data[key] = value
    return validated_data


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


def show_result(result, self):
    if result:
        for index, elem in enumerate(result):
            bot.send_message(self.chat.id,
                             f'***{index + 1}. Название рецепта: {elem.title}***',
                             parse_mode='MARKDOWN')
            bot.send_message(self.chat.id,
                             f'Автор рецепта: <i>{elem.author.last_name} {elem.author.first_name}</i>, никнейм - <b>{elem.author.username}</b>',
                             parse_mode='HTML')
            bot.send_message(self.chat.id, f'Рецепт: {elem.text}', parse_mode='HTML')
            if elem.image:
                with open(settings.BASE_DIR + elem.image.url, "rb") as file:
                    bot.send_photo(self.chat.id, file, "И вот так оно выглядит")
    else:
        bot.send_message(self.chat.id,
                         f'К сожалению, у нас пока нет рецепта с такими параметрами, попробуйте ввести другие параметры',
                         parse_mode='HTML')