import telebot 
from telebot import types 
from django.core.management.base import BaseCommand
from django.conf import settings
from bot.models import Profile, Message, Video

def bot_mailing(ids, m_message, image):
    newids = []
    bot = telebot.TeleBot(token=settings.TOKEN)
    print(m_message)
    print(str(image))
    for i in ids:
        newids.append(i.external_id)
    for i in newids:
        try:
            if image != '':
                bot.send_photo(i, photo=open(fr'C:\Users\levni\Desktop\real_porno_bot\mysite\media\{str(image)}', 'rb'),
                            caption=m_message)
            else:
                bot.send_message(i, m_message)
        except Exception as e:
            print(e)


class User():
    def __init__(self, count):
        self.count = count
        self.id = ''

        

counts = {}

bot = telebot.TeleBot(token=settings.TOKEN, threaded=False)

class Command(BaseCommand):
    def handle(self, *args, **options):

        @bot.message_handler(commands=['start'])
        def start_message(message):
            try:
                l = Video.objects.all()
                p, _ = Profile.objects.get_or_create(external_id=message.chat.id, defaults={'name': message.from_user.first_name})
                counts[message.chat.id] = User(len(Video.objects.all())-1)
                msg = send_video(counts[message.chat.id].count, message.chat.id, first=True)
                counts[message.chat.id].id = str(msg)
            except Exception as e:  
                print(e)

        @bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):
            if call.data == '>':
                counts[call.message.chat.id].count = int(counts[call.message.chat.id].count) - 1
            elif call.data == '<':
                counts[call.message.chat.id].count = int(counts[call.message.chat.id].count) + 1

            send_video(check_count(counts[call.message.chat.id].count, call.message.chat.id), call.message.chat.id)


        bot.infinity_polling(none_stop=True)


def check_count(count, chat_id):
    if int(count) > len(Video.objects.all())-1:
        counts[chat_id].count = 0
    elif int(count) < 0:
        counts[chat_id].count = len(Video.objects.all())-1
    return counts[chat_id].count


def send_video(video_id, chat_id, first=False):
    counts[chat_id].count = video_id
    all_video = Video.objects.all()
    video = all_video[video_id]
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Ссылка на фул', url=f'{video.url_video}')
    btn2 = types.InlineKeyboardButton('⬅', callback_data='<')
    btn3 = types.InlineKeyboardButton('➡', callback_data='>')
    markup.row(btn1).row(btn2,btn3)
    if first:
        msg = bot.send_document(chat_id, open(fr'C:\Users\levni\Desktop\real_porno_bot\mysite\media\{str(video.video)}', 'rb'), caption=f'{video.name}\n\n{video.discription}', reply_markup=markup)
        return msg.message_id
    else:
        bot.edit_message_media(media=types.InputMediaVideo(media=open(fr'C:\Users\levni\Desktop\real_porno_bot\mysite\media\{str(video.video)}', 'rb')), chat_id=chat_id, message_id=counts[chat_id].id, reply_markup=markup)
        bot.edit_message_caption(caption=f'{video.name}\n\n{video.discription}', chat_id=chat_id, message_id=counts[chat_id].id, reply_markup=markup)

