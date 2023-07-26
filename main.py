import telebot
from PIL import Image
from telebot import types # для указание типов

bot = telebot.TeleBot('6586120678:AAGZUQtr2zVw_fqigdhjfv0scrtkpcCD5oM')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    start_button = types.KeyboardButton('/start')
    help_button = types.KeyboardButton('/help')
    view_watermarks_button = types.KeyboardButton('/view_watermarks')
    markup.add(start_button, help_button, view_watermarks_button)
    bot.send_message(message.chat.id, 'Привет! Пришлите мне изображение или введите /help.', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/start - Запустить бот\n/view_watermarks - Просмотр доступных водяных знаков\nПришлите мне фотографию, чтобы добавить водяной знак!')


@bot.message_handler(commands=['view_watermarks'])
def view_watermarks(message):
    watermarks = ['1.png', '2.png']
    text = 'Доступные водяные знаки:\n'
    for i, watermark in enumerate(watermarks):
        text += f'{i + 1}. {watermark}\n'
        with open(f'img/{watermark}', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=f'Водяной знак {i + 1}')


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    # Download image
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('image.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, 'Выберите вид водяного знака (1,2):')

@bot.message_handler(func=lambda message: True)
def add_watermark(message):
    try:
        img = Image.open('image.jpg')
        wm = Image.open(f'img/{message.text}.png')

        # Resize image to fit watermark dimensions while maintaining proportions
        width_ratio = wm.width / img.width
        height_ratio = wm.height / img.height
        resize_ratio = max(width_ratio, height_ratio)
        new_width = int(img.width * resize_ratio)
        new_height = int(img.height * resize_ratio)
        img = img.resize((new_width, new_height))

        # Create new image and paste watermark
        result = Image.new("RGB", wm.size)
        result.paste(img, ((wm.width - img.width) // 2, (wm.height - img.height) // 2))
        result.paste(wm, (0, 0), wm)

        # Save and send result
        result.save('result.jpg')
        with open('result.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.reply_to(message, 'Извините, я не понимаю вас.')

bot.polling()