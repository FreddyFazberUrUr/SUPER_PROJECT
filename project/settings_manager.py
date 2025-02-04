import json
from CONSTS import SETTINGS_FILE, DEFAULT_MODEL

struct = {
    'user_id': {
        'model': DEFAULT_MODEL
    }
}


def load_settings():
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8-sig') as f:
            settings = json.load(f)
            return settings
    except json.JSONDecodeError:
        return {}


def dump_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

