from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import subprocess
import json
import os
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Configuration
MINER_PATH = "/storage/emulated/0/xmrig-6.22.0/xmrig"
WALLET_ADDRESS = "4385pTGhmZUK5ZcAqekKXk8Z3UuSxezEUYmhA9j9Ckmy5eTFatTEFaJJnxgQCg48ef3opVwsFfhhX17FTCA2hM6UT17Rn9x"
BOT_TOKEN = "7435606545:AAGLUaOZ0ZlEekkRgCXPCbL9chmmVUSMppM"
MINING_POOL = "rtm.suprnova.cc:4273"
PAYMENT_HISTORY_FILE = "payment_history.json"

# Payment history initialization
if not os.path.isfile(PAYMENT_HISTORY_FILE):
    with open(PAYMENT_HISTORY_FILE, "w") as f:
        json.dump([], f)

async def start_mining(update: Update, context: CallbackContext):
    """Start mining."""
    logger.info('Starting mining process...')
    command = [
        MINER_PATH, 
        "-a", "gr",
        "-o", MINING_POOL,
        "--tls",
        "-u", WALLET_ADDRESS,
        "-p", "x"
    ]
    process = subprocess.Popen(command)
    context.chat_data['process'] = process
    await update.message.reply_text('Monero mining started!')
    logger.info('Mining process successfully started.')

async def stop_mining(update: Update, context: CallbackContext):
    """Stop mining."""
    process = context.chat_data.get('process')
    if process:
        process.terminate()
        await update.message.reply_text('Monero mining stopped!')
        logger.info('Mining process stopped.')
    else:
        await update.message.reply_text('Mining process not found.')
        logger.warning('Tried to stop mining, but no process was found.')

def main():
    """Main function to run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start_mining", start_mining))
    application.add_handler(CommandHandler("stop_mining", stop_mining))
    
    application.run_polling()

if __name__ == '__main__':
    main()

