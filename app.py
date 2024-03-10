import telebot
import requests

bot = telebot.TeleBot('SEU TOKEN BOT')
API = 'SUA API DO OPENAI'
user_messages = {}

def get_response(question):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API}'
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': question,
        'temperature': 0.1,
        'max_tokens': 4040
    }
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['text']

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    if message.text.startswith('/perg'):
        user_messages[chat_id] = [message.text]
        response = get_response(' '.join(user_messages[chat_id]))
        bot.send_chat_action(chat_id, 'typing')
        bot.reply_to(message, response)

bot.polling()
print('Bot iniciado...')
