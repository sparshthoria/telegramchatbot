import logging
import qrcode
from io import BytesIO
from aiogram import Bot, Dispatcher, executor, types
API_TOKEN = '7129555056:AAF12-GK2qnQS01ljXWzGUz_WS0GMhupGtc'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def generate_qr_code(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = BytesIO()
    bio.name = 'qr.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! Send me a link and I'll generate a QR code for you.")
@dp.message_handler()
async def echo(message: types.Message):
    if message.text.startswith('http://') or message.text.startswith('https://'):
        qr_image = generate_qr_code(message.text)
        await bot.send_photo(chat_id=message.chat.id, photo=qr_image, caption="Here is your QR code!")
    else:
        await message.answer("Please send a valid link starting with http:// or https://")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

    




















