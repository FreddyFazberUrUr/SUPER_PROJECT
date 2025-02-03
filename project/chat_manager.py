from CONSTS import *
import sqlite3
import logging


def create_database():
    try:
        with sqlite3.connect(DB_FILE) as con:
            cur = con.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                role TEXT,
                tokens INTEGER)
            ''')
        logging.info(f"DATABASE CREATED")
    except Exception as e:
        logging.critical(e)
        return None


def get_history(user_id):
    messages = []
    try:
        with sqlite3.connect(DB_FILE) as con:
            cur = con.cursor()
            cur.execute('''
                SELECT message, role FROM history WHERE user_id=? ORDER BY id DESC LIMIT ?''',
                           (user_id, 3))

            data = cur.fetchall()

            if data and data[0]:
                for message in reversed(data):
                    messages.append({'content': message[0], 'role': message[1]})
            return messages
    except Exception as e:
        logging.critical(e)
        return messages


def add_message(user_id, data: [str, str, int]):
    try:
        with sqlite3.connect(DB_FILE) as con:
            cur = con.cursor()
            message, role, tokens = data
            cur.execute('''
                    INSERT INTO history (user_id, message, role, tokens) 
                    VALUES (?, ?, ?, ?)''',
                        (user_id, message, role, tokens)
                        )
            con.commit()
            logging.info(f"DATABASE: INSERT INTO messages "
                         f"VALUES ({user_id}, {message}, {role}, {tokens})")
    except Exception as e:
        logging.critical(e)
        return None


def count_tokens(user_id):
    try:
        with sqlite3.connect(DB_FILE) as con:
            cur = con.cursor()
            cur.execute(f'''SELECT SUM(tokens) FROM history WHERE user_id=?''', (user_id,))
            data = cur.fetchone()
            if data and data[0]:
                logging.info(f"DATABASE: {user_id} потратил {data[0]} токенов")
                return data[0]
            else:
                return 0
    except Exception as e:
        logging.critical(e)
        return 0


def reset_tokens():
    try:
        with sqlite3.connect(DB_FILE) as con:
            cur = con.cursor()
            cur.execute('''UPDATE history SET tokens = 0''')
            con.commit()
            logging.info('Токены сброшены')
    except Exception as e:
        logging.critical(e)


if __name__ == '__main__':
    reset_tokens()
    add_message(5948417394, ('la', 'assistant', 10000))