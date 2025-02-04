from dotenv import load_dotenv
import os

load_dotenv('creds/.env')

# НЕЙРОСЕТЬ
DEFAULT_SYSTEM_PROMPT = '''
Отвечай коротко и ясно
'''
MATH_SYSTEM_PROMPT = '''

'''
FRIEND_SYSTEM_PROMPT = '''

'''

SYSTEM_PROMPTS = {'По умолчанию': DEFAULT_SYSTEM_PROMPT,
                  'Учитель математики': MATH_SYSTEM_PROMPT,
                  'Друг': FRIEND_SYSTEM_PROMPT}

DEFAULT_MODEL = 'gpt-4o-mini'
MAX_TOKENS_IN_MESSAGE = 1000
MAX_TOKENS_PER_DAY = 3000
MODELS = ['gpt-4o-mini', 'gpt-4o', 'gpt-4-turbo', 'o1-mini']

# ПОЛЬЗОВАТЕЛИ
MAX_USERS = 100
COUNT_LAST_MSG = 4
TRANSLATE = {'model': "Модель нейросети",
             'Модель нейросети': 'model',
             'system_prompt': 'Системный промпт',
             'Системный промпт': 'system_prompt'}
VALUES = {'Модель нейросети': MODELS,
          'Системный промпт': SYSTEM_PROMPTS}

# ФАЙЛЫ
HOME_DIR = '..'
LOGS = f'{HOME_DIR}/logs.log'
DB_FILE = f'{HOME_DIR}/database.db'
SETTINGS_FILE = f'{HOME_DIR}/settings.json'

# API & URL
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
BASE_URL = 'https://bothub.chat/api/v2/openai/v1/chat/completions'
API_WEATHER_KEY = os.getenv('API_WEATHER_KEY')
API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')
