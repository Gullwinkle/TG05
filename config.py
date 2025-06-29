import os
from dotenv import load_dotenv

load_dotenv('../.env')
TOKEN = os.getenv('BOT_TOKEN')
THE_CAT_API_KEY = os.getenv('CAT_API_KEY')
NASA_API_KEY = os.getenv('NASA_API_KEY')