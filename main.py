from lib.bot import bot
from server import keep_alive

VERSION = '1.0.0'

keep_alive()
bot.run(VERSION)
