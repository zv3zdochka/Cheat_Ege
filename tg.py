import telegram

TOKEN = "7145495129:AAGDH5TuFBDsZs-NeMlJ6Mv9hkY4UXsWIhQ"
bot = telegram.Bot(token=TOKEN)
# ссылка_канала - это придуманная вами ссылка
# Telegram-канала (t.me/ссылка_канала)
chanell = '@ссылка_канала'

text="Первое сообщение!"
send = bot.send_message(chat_id=chanell, text=text)
print(f'Номер отправленного сообщения: {send.message_id}')