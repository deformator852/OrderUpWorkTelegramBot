import aiohttp
from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()

API_ID = 0
API_HASH = ""
#Data from USER API

PROXY_URL = "socks5://user:password@proxy_ip:proxy_port"
PROXY_AUTH = aiohttp.BasicAuth(login="login",password="password")

TOKEN = ""
#Token for BOT API
bot = Bot(token=TOKEN,proxy=PROXY_URL,proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot,storage=storage)

