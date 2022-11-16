import telebot
import img2pdf
import config


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    global mess
    if message.text == '/start':
        if message.from_user.last_name is None:
            mess = f'Привет , {message.from_user.first_name}'
        elif message.from_user.first_name is None:
            mess = f'Привет , {message.from_user.last_name}'
        else:
            mess = f'Привет , {message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.chat.id, mess)
@bot.message_handler(content_types=['photo'])
def get_user_photo(message: telebot.types.Message):
    raw = message.photo[2].file_id
    name = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    file = open('file.pdf', 'wb')
    file.write(img2pdf.convert(name))
    file.close()
    chat_id = message.chat.id
    pdfFile = open('file.pdf', 'rb')
    bot.send_document(chat_id, pdfFile)


bot.polling(none_stop=True)