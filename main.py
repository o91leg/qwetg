import requests
from flask import Flask, request
from config import BOT_TOKEN, ADMIN_ID

app = Flask(__name__)

# Замени на твой токен, который ты получил от @BotFather
BOT_TOKEN = "BOT_TOKEN"
# Замени на ID админа (твой ID), которому будут пересылаться файлы
ADMIN_ID = "ADMIN_ID"

# Обработчик для команды /start
def start(update, context):
    chat_id = update['message']['chat']['id']
    message = "Привет! Я бот, который может принимать и пересылать фото и видео."
    send_message(chat_id, message)

# Обработчик для принятия фото и видео
def handle_media(update, context):
    chat_id = update['message']['chat']['id']
    media_type = update['message']['photo'] if 'photo' in update['message'] else update['message']['video']
    file_id = media_type[-1]['file_id']
    forward_media(chat_id, file_id)

# Отправка сообщения
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=data)

# Пересылка медиа файлов админу
def forward_media(chat_id, file_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/forwardMessage'
    data = {'chat_id': ADMIN_ID, 'from_chat_id': chat_id, 'message_id': file_id}
    requests.post(url, json=data)

# Обработка входящих обновлений
@app.route('/', methods=['POST'])
def handle_update():
    update = request.json
    if 'message' in update and 'chat' in update['message']:
        chat_id = update['message']['chat']['id']
        if 'text' in update['message'] and update['message']['text'] == '/start':
            start(update, {})
        elif 'photo' in update['message'] or 'video' in update['message']:
            handle_media(update, {})
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)