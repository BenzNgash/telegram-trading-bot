# Telegram Trading Bot with LangChain and Hugging Face

This project is a **Telegram Bot** that helps traders manage and track their trades. It allows users to upload images of their trades and input trade details (such as Profit, TP, SL, Currency). The bot processes the trade details and saves the data, along with the image, in a CSV file. The bot uses **LangChain** for processing natural language inputs and **Hugging Face** for NLP-based tasks.

## Features

- Upload and save images of trade setups.
- Extract and parse trade details (Pair, Profit, TP, SL, Currency) from text using NLP models.
- Store trade data and images locally in CSV format for easy tracking.
- 24/7 availability with the bot running on **Render**.

## Tech Stack

- **Python**
- **LangChain**: For language model handling.
- **Hugging Face**: For using pre-trained NLP models.
- **Telegram Bot API**: For communication between the bot and users.
- **Pandas**: For storing and managing trade data in CSV format.
- **Pillow**: For image handling (saving and processing images).
- **Render**: For hosting the bot 24/7.

## Setup

To run the bot locally or deploy it to a cloud service like Render, follow the steps below.

### Prerequisites

- Python 3.10 or later
- A **Telegram Bot API token** (Create a bot via [BotFather](https://core.telegram.org/bots#botfather) on Telegram)
- A **Hugging Face API token** (You can get it from [Hugging Face](https://huggingface.co/))
- **Kaggle Secrets** for storing your API tokens securely

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/telegram-trading-bot.git
   cd telegram-trading-bot
