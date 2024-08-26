import telebot  
import random  

API_TOKEN = '7300215472:AAEq4VkTbyAzXXdPmiInA9tdj_eRLZDSAws'  # توکن ربات تلگرام خود را اینجا قرار دهید  
bot = telebot.TeleBot(API_TOKEN)  

active_chats = {}  # دیکشنری برای نگه‌داری اتاق‌های چت  
waiting_users = []  # لیست کاربران منتظر  

@bot.message_handler(commands=['start'])  
def start_chat(message):  
    bot.send_message(message.chat.id, "سلام! برای شروع چت با یک ناشناس بفرست /chat")  

@bot.message_handler(commands=['chat'])  
def join_chat(message):  
    user_id = message.chat.id  
    
    # بررسی اینکه کاربر در انتظار یا در چت است  
    if user_id in waiting_users:  
        bot.send_message(user_id, "شما در حال حاضر در انتظار یک کاربر دیگر هستید.")  
        return  

    if user_id in active_chats:  
        bot.send_message(user_id, "شما هم اکنون در چت هستید. برای خروج /exit را بزنید.")  
        return  
    
    waiting_users.append(user_id)  
    
    if len(waiting_users) >= 2:  
        # اتصال دو کاربر به یکدیگر  
        partner_id = waiting_users.pop(0)  
        chat_id = f"chat_{random.randint(1000, 9999)}"  # ایجاد شناسه اتاق چت  
        active_chats[chat_id] = (user_id, partner_id)  
        bot.send_message(user_id, f"شما با یک کاربر ناشناس متصل شدید. شناسه اتاق: {chat_id}")  
        bot.send_message(partner_id, f"شما با یک کاربر ناشناس متصل شدید. شناسه اتاق: {chat_id}")  
    else:  
        bot.send_message(user_id, "در حال انتظار برای یک کاربر دیگر برای چت...")  

@bot.message_handler(commands=['stop'])  
def stop_waiting(message):  
    user_id = message.chat.id  

    # حذف کاربر از لیست کاربران منتظر در صورت وجود  
    if user_id in waiting_users:  
        waiting_users.remove(user_id)  
        bot.send_message(user_id, "شما از انتظار خارج شدید.")  
    else:  
        bot.send_message(user_id, "شما در حال حاضر در انتظار نیستید.")  

@bot.message_handler(commands=['exit'])  
def leave_chat(message):  
    user_id = message.chat.id  

    # جستجوی اتاق چت کاربر  
    chat_id = next((cid for cid, users in active_chats.items() if user_id in users), None)  

    if chat_id is None:  
        bot.send_message(user_id, "شما در چتی نیستید.")  
        return  

    partner_id = active_chats[chat_id][0] if active_chats[chat_id][1] == user_id else active_chats[chat_id][1]  
    del active_chats[chat_id]  # حذف اتاق چت  

    bot.send_message(user_id, "شما از چت خارج شدید.")  
    bot.send_message(partner_id, "کاربر از چت خارج شد.")  

@bot.message_handler(func=lambda message: any(message.chat.id in users for users in active_chats.values()))  
def forward_message(message):  
    user_id = message.chat.id  

    # جستجوی اتاق چت کاربر  
    chat_id = next((cid for cid, users in active_chats.items() if user_id in users), None)  

    if chat_id:  
        partner_id = active_chats[chat_id][0] if active_chats[chat_id][1] == user_id else active_chats[chat_id][1]  
        if message.content_type == 'text':  
            bot.send_message(partner_id, message.text)  
        elif message.content_type in ['photo', 'gif']:  
            bot.forward_message(partner_id, user_id, message.message_id)  

bot.polling()