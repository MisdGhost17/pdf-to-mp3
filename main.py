from index import TOKEN
import fitz
import pyttsx3
import logging
from aiogram import Bot, Dispatcher, executor, types


#telegramm bot
API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

global text


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm MisdGhostBot!\n I can convert pdf files to mp3.\n '/start' to continue")

@dp.message_handler(commands=['start'])
async def please_send_file(message: types.Message):
    chat_id = message.chat.id

    await bot.send_message(chat_id, "Send me the file")

    @dp.message_handler(content_types=['document'])
    async def handle_docs_pdf(message):
        global text
        chat_id = message.chat.id

        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, "docs/test.pdf")

        await bot.send_message(chat_id, "Successfully, converting...")

        file1 = fitz.open('docs/test.pdf')

        for pageNumber, page in enumerate(file1.pages(), start=1):

            text = page.get_text()

            txt = open(f'test_Page_{pageNumber}.txt', 'a', encoding="utf-8")
            txt.writelines(text)
            txt.close()

        engine = pyttsx3.init()

        engine.save_to_file(text, 'docs/test1.mp3')

        engine.runAndWait()

        await bot.send_audio(chat_id, open('docs/test1.mp3', 'rb'))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)