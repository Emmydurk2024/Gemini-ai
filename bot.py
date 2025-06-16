import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7888207579:AAHkbsi0j1I6qAXR_oSlpN0y8eYX_Wi9jUE"
API_KEY = "AIzaSyBupsnMpxBrDzVYH7WhAal4i3XY9M4c_6g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me any message and I'll answer using Gemini AI.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    params = {"key": API_KEY}
    json_data = {
        "contents": [
            {"parts": [{"text": user_text}]}
        ]
    }

    response = requests.post(url, params=params, json=json_data)

    if response.status_code == 200:
        try:
            reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            reply = "Sorry, I couldn't understand the response."
    else:
        reply = f"Error from API: {response.status_code}"

    await update.message.reply_text(reply)

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
