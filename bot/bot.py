import telebot
from datetime import datetime
from bot.utils import str_contains_url
from bot.user import User
from bot.chat import Chat
from bot.config import delay, max_message_length

class Bot:
    def __init__(self, token):
        bot = telebot.TeleBot(token)
        self.bot = bot
        self.chats = {}

        @bot.message_handler(content_types=['text', 'photo', 'document'])
        def send_text(message):
            chat_id = message.chat.id
            is_old_user = self.check_user(message.from_user, chat_id)
            if (is_old_user):
                return
            has_photo = message.photo is not None
            has_url = message.text is not None and str_contains_url(message.text.lower())
            is_so_long =  message.text is not None and len(message.text) > max_message_length

            if (has_photo or has_url or is_so_long):
                bot.delete_message(chat_id, message.message_id)
                # bot.send_message(chat_id, '-1')

        @bot.message_handler(content_types=['new_chat_members'])
        def new_use_joined(message):
            for user in message.new_chat_members:
                self.check_user(user, message.chat.id)

    def check_user(self, user, chat_id):
        if (chat_id in self.chats):
            users = self.chats[chat_id].users
        else:
            chat = Chat()
            self.chats[chat_id] = chat
            users = chat.users
        if user.id in users:
            saved_user = users[user.id]
            now = datetime.now()
            return now - saved_user.join_date > delay
        else:
            users[user.id] = User(datetime.now(), user.id, user.username, user.first_name, user.last_name, user.language_code, user.is_bot)

    def start(self):
        self.bot.polling()
