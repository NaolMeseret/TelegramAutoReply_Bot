from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import json
import os

# Replace with your Bot Token from BotFather
TOKEN = "8276805572:AAG7axIEjUVqJjIQvh3ijHUeIL1sxLsr3SY"

# Auto-reply message
AUTO_REPLY = """[AUTOMATED MESSAGE]

UPDATED ON January 17, 2026.

If you are requesting any kind of help, please be aware, I am taking very personal time, so I won't be responding to your message.

Thank you for understanding. Please reach out to other people that might help you.

In case you wrote a long message, please instead record an audio note 🙏

Be aware Naol didn't see this message yet. So please confirm by sending back "Yes".

[አውቶማቲክ መልእክት ነው] 
ረጅም መልእክት ከፃፉ እባኮትን ኦዲዮ ይላኩ 🙏

ናኦል ይህን መልእክት እስካሁን እንዳላየ ልብ ይበሉ። ስለዚህ እባክዎን "Yes" በመላክ ያረጋግጡ

Read this page please:

https://nohello.net/en/
"""

# File to store replied users and Yes confirmations
LOG_FILE = "replied_users.json"

# Load or initialize log
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        replied_users = json.load(f)
else:
    replied_users = {}

def save_log():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(replied_users, f, ensure_ascii=False, indent=4)

def auto_reply(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)  # store as string for JSON
    user_name = update.message.from_user.username or "NoUsername"
    message_text = update.message.text.strip()

    print(f"Received message from {user_name} ({user_id}): {message_text}")

    # If user hasn't received the auto-reply yet
    if user_id not in replied_users:
        update.message.reply_text(AUTO_REPLY)
        replied_users[user_id] = {"username": user_name, "replied": True, "confirmed_yes": False}
        save_log()
        print(f"Sent auto-reply to {user_name} ({user_id})")
        return

    # If user sends "Yes", mark confirmation
    if message_text.lower() == "yes":
        if not replied_users[user_id]["confirmed_yes"]:
            replied_users[user_id]["confirmed_yes"] = True
            save_log()
            update.message.reply_text("✅ Thank you for confirming!")
            print(f"{user_name} ({user_id}) confirmed Yes")
        else:
            print(f"{user_name} ({user_id}) already confirmed Yes")
    else:
        # Optional: ignore other messages or respond politely
        print(f"Ignored message from {user_name} ({user_id})")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_reply))
    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
