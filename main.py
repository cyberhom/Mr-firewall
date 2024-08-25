import telebot  
from telebot import types  
import random  

API_TOKEN = '7300215472:AAEq4VkTbyAzXXdPmiInA9tdj_eRLZDSAws'  # توکن ربات تلگرام خود را اینجا قرار دهید  
bot = telebot.TeleBot(API_TOKEN)  

active_chats = {}  
chat_pairs = {}  

@bot.message_handler(commands=['start'])  
def start_chat(message):  
    bot.send_message(message.chat.id, "سلام! برای شروع چت با یک ناشناس بفرست /chat")  

@bot.message_handler(commands=['chat'])  
def join_chat(message):  
    user_id = message.chat.id  

    if user_id in active_chats:  
        bot.send_message(user_id, "شما هم اکنون در چت هستید. برای خروج /exit را بزنید.")  
        return  

    # پیدا کردن یک کاربر دیگر برای چت  
    if len(chat_pairs) > 0:  
        partner_id = chat_pairs.popitem()[1]  
        active_chats[user_id] = partner_id  
        active_chats[partner_id] = user_id  
        bot.send_message(user_id, "شما با یک کاربر ناشناس متصل شدید.")  
        bot.send_message(partner_id, "شما با یک کاربر ناشناس متصل شدید.")  
    else:  
        chat_pairs[user_id] = user_id  # ذخیره کاربر در لیست برای انتظار  
        bot.send_message(user_id, "در حال انتظار برای یک کاربر دیگر برای چت...")  

@bot.message_handler(commands=['exit'])  
def leave_chat(message):  
    user_id = message.chat.id  

    if user_id not in active_chats:  
        bot.send_message(user_id, "شما در چتی نیستید.")  
        return  

    partner_id = active_chats[user_id]  
    del active_chats[partner_id]  # حذف کاربر دیگر  
    del active_chats[user_id]     # حذف کاربر فعلی  

    bot.send_message(user_id, "شما از چت خارج شدید.")  
    bot.send_message(partner_id, "کاربر از چت خارج شد.")  

@bot.message_handler(commands=['show'])  
def show_partner(message):  
    user_id = message.chat.id  

    if user_id not in active_chats:  
        bot.send_message(user_id, "شما در چتی نیستید.")  
    else:  
        partner_id = active_chats[user_id]  
        bot.send_message(user_id, "شما در حال چت با یک کاربر ناشناس هستید.")  

@bot.message_handler(func=lambda message: message.chat.id in active_chats)  
def forward_message(message):  
    user_id = message.chat.id  
    partner_id = active_chats[user_id]  

    if partner_id:  
        # اگر پیام حاوی مدیا باشد، آن را ارسال کن  
        if message.content_type == 'text':  
            bot.send_message(partner_id, message.text)  
        elif message.content_type == 'photo':  
            bot.forward_message(partner_id, user_id, message.message_id)  
        elif message.content_type == 'gif':  # برای GIF ها  
            bot.forward_message(partner_id, user_id, message.message_id)  
        # دیگر انواع رسانه‌ها را می‌توانید اضافه کنید اگر نیاز دارید  

bot.polling()