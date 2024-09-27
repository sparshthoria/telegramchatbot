import logging
from io import BytesIO
from aiogram import Bot, Dispatcher, executor, types
import google.generativeai as genai

API_TOKEN = '7238328741:AAHzUvNh0ikDfhJuVs3PU88427wRFON3esc'
GEMINI_API_KEY = 'AIzaSyDT6y0w0wu1QN3lLtvn-YJz-jLalo6kz8A'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# Initialize Gemini GPT model for text
genai.configure(api_key=GEMINI_API_KEY)
text_model = genai.GenerativeModel('gemini-1.5-flash')
# Initialize Gemini GPT model for vision
generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 32,
    "max_output_tokens": 1024,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
vision_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
def query_gemini_gpt(prompt):
    response = text_model.generate_content(prompt)
    return response.text
def describe_image_with_gemini(image_bytes):
    prompt_parts = [
        "Recognize the image and describe the image",
        "Image: ",
        {
            "mime_type": "image/jpeg",
            "data": image_bytes.read()
        },
    ]
    response = vision_model.generate_content(prompt_parts)
    return response.text
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! Ask me anything and I'll respond using the Gemini GPT API. You can also send me an image, and I'll describe it for you.")
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    photo_bytes = BytesIO()
    await photo.download(destination_file=photo_bytes)
    photo_bytes.seek(0)
    image_description = describe_image_with_gemini(photo_bytes)
    await message.reply(f"Image Description: {image_description}")
@dp.message_handler()
async def handle_message(message: types.Message):
    user_question = message.text
    gpt_response = query_gemini_gpt(user_question)
    await message.reply(gpt_response)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)







