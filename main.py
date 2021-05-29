from lib.bot import bot
from server import keep_alive

VERSION = '1.0.1'

keep_alive()
bot.run(VERSION)
