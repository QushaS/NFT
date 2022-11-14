from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
from captcha.image import ImageCaptcha

from data import config

bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
# dp.filters_factory.bind(IsCaptcha, event_handlers=[dp.message_handlers, dp.callback_query_handlers])