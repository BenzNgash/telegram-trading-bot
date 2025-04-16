# ✅ Install LangChain and Hugging Face support
!pip install -q langchain langchainhub langchain-community
!pip install -q transformers accelerate bitsandbytes huggingface_hub
!pip install python-telegram-bot --upgrade

# ✅ Import libraries
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from huggingface_hub import login
import os
import json
import pandas as pd
from PIL import Image
from datetime import datetime
import telebot
from kaggle_secrets import UserSecretsClient
from transformers import pipeline

# ✅ Hugging Face API login (replace with your token securely)
user_secrets = UserSecretsClient()
hf_token = user_secrets.get_secret("Hugging")
bot_token = user_secrets.get_secret("bot")  # Add this in your Kaggle secrets
login(token=hf_token)

# ✅ Telegram Bot Setup
bot = telebot.TeleBot(bot_token)

# ✅ Setup Hugging Face LLM via Transformers
extract_pipeline = pipeline(
    "text2text-generation",
    model="declare-lab/flan-alpaca-large",  # free and lightweight for Kaggle
    max_length=512
)

# ✅ Folder setup
base_dir = "/kaggle/working/trades"
image_dir = os.path.join(base_dir, "images")
os.makedirs(image_dir, exist_ok=True)
csv_path = os.path.join(base_dir, "trades.csv")

# ✅ Helper: Parse trade info
def extract_trade_info(text):
    prompt = f"Extract the following fields from this text: Pair, Profit, TP, SL, Currency.\n\nText:\n{text}\n\nReturn as JSON."
    result = extract_pipeline(prompt)[0]["generated_text"]
    try:
        return json.loads(result)
    except:
        lines = [line.strip() for line in result.splitlines() if ":" in line]
        return {line.split(":")[0].strip(): line.split(":")[1].strip() for line in lines}

# ✅ Handle trade image upload
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    try:
        print("📷 Photo received!")

        # Get the file
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"{image_dir}/trade_{timestamp}.png"

        with open(image_path, 'wb') as f:
            f.write(downloaded_file)

        bot.reply_to(message, "✅ Image received. Now send the trade message.")
        message.chat.image_path = image_path  # Temporary store (for illustration)
        print(f"✅ Image saved to {image_path}")

    except Exception as e:
        print("❌ Error saving image:", e)
        bot.reply_to(message, "❌ Failed to save image.")

# ✅ Handle trade message
@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        print("📨 Message received:", message.text)
        trade_data = extract_trade_info(message.text)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trade_data["timestamp"] = timestamp

        # Attach the latest image if exists
        latest_image = None
        files = sorted(os.listdir(image_dir), reverse=True)
        if files:
            latest_image = os.path.join(image_dir, files[0])
            trade_data["image_path"] = latest_image

        # Save to CSV
        df = pd.DataFrame([trade_data])
        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path)
            df = pd.concat([df_existing, df], ignore_index=True)
        df.to_csv(csv_path, index=False)

        bot.reply_to(message, f"✅ Trade saved:\n{json.dumps(trade_data, indent=2)}")
        print("✅ Trade data saved")

    except Exception as e:
        print("❌ Error processing text:", e)
        bot.reply_to(message, "❌ Failed to parse and save trade.")

# ✅ Start bot
print("🤖 Bot is running...")

import threading
def run_bot():
    bot.infinity_polling()

thread = threading.Thread(target=run_bot)
thread.start()
