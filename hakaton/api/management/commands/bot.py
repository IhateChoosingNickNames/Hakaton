# token for bot 5316090505:AAH_de0luqf2EY3z9qVSknPOFuFfJ8uljCk

# Параметры для handler: 1) commands - непосредственно команды, 2) chat_types = ['supergroup'] или ['private']
# учет приватности чата 3) content_types = ['photo'], ['video'], ['text'], ['document'] - учет формата ввода 4)
# regexp = r'[0-9]+' - регулярное выражение 5) func = ... - какая-либо функция.

# 2 handler'а друг над другом - это "или". То есть либо один выполняется, либо другой.
# Если передавать именованные параметры, то это будет "и". И то, и другое.

# message_handler(filters) - обрабатывает сообщения
# edited_message_handler(filters) - обрабатывает отредактированные сообщения
# channel_post_handler(filters) - обрабатывает сообщения канала
# callback_query_handler(filters) - обрабатывает callback запросы

import telebot, time
from django.core.management import BaseCommand
from telebot import types
from api.views import get_recipe

bot = telebot.TeleBot('6076686900:AAF0h65v2-dTuUDgZs1y6747lceipM0lbOQ')

commands = ["/start", "/recipe", "/add"]

class Command(BaseCommand):
    help = "Команда для запуска бота"

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()

    @bot.message_handler(commands=['start'])
    def start(self):
        bot.delete_message(self.chat.id, self.message_id)
        bot.send_message(self.chat.id, f'Greetings, <tg-spoiler>Unknown User</tg-spoiler> !', parse_mode='HTML')

    @bot.message_handler(commands=['recipe'])
    def recipe(self):
        bot.delete_message(self.chat.id, self.message_id)

        params = self.text.replace('/recipe', '').lstrip().split()
        result = get_recipe(*params)
        bot.send_message(self.chat.id, f'{result[0]}', parse_mode='HTML')

    @bot.message_handler(commands=['add'])
    def add_recipe(self):
        bot.delete_message(self.chat.id, self.message_id)

        sent = bot.send_message(self.chat.id, f'Введите "категорию", "тип", "название", "рецепт":', parse_mode='HTML')
        bot.register_next_step_handler(sent, Command.smth)
        params = self.text.replace('/recipe', '').lstrip().split()

    def smth(self):
        params = self.text
        bot.send_message(self.chat.id, f'Рецепт успешно создан', parse_mode='HTML')

    @bot.message_handler(func=lambda x: x not in commands)
    def wrong(self):
        bot.reply_to(self, 'Введена некорретная команда.')