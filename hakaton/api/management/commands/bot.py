import telebot
from django.core.management import BaseCommand
from telebot import types
from api.views import get_recipe, add_recipe
from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv("TG_BOT")
bot = telebot.TeleBot(SECRET_KEY)

commands = ["/get_recipe", "/add_recipe", "/menu", "/greet"]
recipe = {"params": None, "text": None}

class Command(BaseCommand):
    """Команда для запуска бота."""

    help = "Команда для запуска бота python manage.py bot"

    def handle(self, *args, **options):
        """Инциализация бота."""
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()

    @bot.message_handler(commands=['greet'])
    def start(self):
        """Фунция приветствия."""
        bot.delete_message(self.chat.id, self.message_id)
        bot.send_message(self.chat.id, f'Greetings, <tg-spoiler>Unknown User</tg-spoiler> !', parse_mode='HTML')

    @bot.message_handler(commands=['get_recipe'])
    def recipe(self):
        """Функция получения рецентов."""
        bot.delete_message(self.chat.id, self.message_id)
        params = self.text.replace('/get_recipe', '').lstrip()

        if params != "":
            result = get_recipe(*params.split())
            # print(result)
            for elem in result:
                bot.send_message(self.chat.id, f'{elem.text}', parse_mode='HTML')
        else:
            sent = bot.send_message(self.chat.id, f'Укажите "категорию(обязательно)", "тип(опционально)", "название()" через пробел', parse_mode='HTML')
            bot.register_next_step_handler(sent, Command.recipe)

    @bot.message_handler(commands=['add_recipe'])
    def add_recipe(self):
        """Функция добавления рецентов."""
        bot.delete_message(self.chat.id, self.message_id)
        sent = bot.send_message(self.chat.id, f'Введите "категорию", "тип", "название" через пробел', parse_mode='HTML')
        bot.register_next_step_handler(sent, Command.params_maker)

    def params_maker(self):
        """Функция получения параметров для рецепта."""
        recipe["params"] = self.text.split()
        sent = bot.send_message(self.chat.id, f'Введите рецепт:', parse_mode='HTML')
        bot.register_next_step_handler(sent, Command.recipe_maker)

    def recipe_maker(self):
        """Функция создания рецентов."""
        recipe["text"] = self.text
        res = add_recipe(*recipe["params"], recipe["text"])
        if res == 200:
            bot.send_message(self.chat.id, f'Рецепт успешно создан!', parse_mode='HTML')
        else:
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
