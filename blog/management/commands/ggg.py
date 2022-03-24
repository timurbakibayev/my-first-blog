from django.contrib.auth.models import User

from blog.models import Post
from django.core.management.base import BaseCommand, CommandError
import telebot
import datetime

bot = telebot.TeleBot("5191041993:AAEGBJmBS_6VKtaTi27I3eHVsSuju-iuiEg")


status = ""
news_text = ""
news_subj = ""


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global status, news_subj, news_text
    if message.text == "/list":
        bot.reply_to(message, "Вот все ваши новости:")
        for post in Post.objects.all():
            bot.send_message(message.chat.id, f"{post}, ссылка: /details_{post.id}")
    elif message.text[:8] == "/details":
        command_, id_ = message.text.split("_")
        id_ = int(id_)
        post = Post.objects.get(pk=id_)
        bot.send_message(message.chat.id, post.text)
    elif message.text == "/new":
        bot.reply_to(message, "Напишите свою новость")
        status = "new"
    elif status == "new":
        news_text = message.text
        bot.send_message(message.chat.id, "ok, теперь напишите заголовок")
        status = "subj"
    elif status == "subj":
        news_subj = message.text
        bot.send_message(message.chat.id, "ok, спасибо")
        user = User.objects.all().first()
        Post.objects.create(
            author=user,
            title=news_subj,
            text=news_text,
            created_date=datetime.datetime.now(),
            published_date=datetime.datetime.now(),
        )
        bot.send_message(message.chat.id, "Пост создан")
    else:
        bot.reply_to(message, f"Вы написали {message.text}")


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Bot started")
        bot.infinity_polling()
