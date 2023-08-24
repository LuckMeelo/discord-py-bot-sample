import os
from src.bot import Bot
from dotenv import load_dotenv

def main():
    # load .env variables
    load_dotenv()
    # Create an instance of Bot and run it
    bot = Bot()
    bot.run(os.getenv('DISCORD_BOT_TOKEN', None))

if __name__ == '__main__':
    main()
