from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.utils import get
from discord import Intents

from asyncio import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from glob import glob

from datetime import datetime, timedelta
import os
import random
from ..db import db

PREFIX = '!'
OWNER_IDS = [int(os.getenv('OWNER_ID'))]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
intents = Intents.all()
intents.members = True


class Ready(object):
  def __init__(self):
    for cog in COGS:
      setattr(self, cog, False)

  def ready_up(self, cog):
    setattr(self, cog, True)


  def all_ready(self):
    return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
  def __init__(self):
    self.PREFIX = PREFIX
    self.ready = False
    self.guild = None
    self.cogs_ready = Ready()
    self.scheduler = AsyncIOScheduler()

    super().__init__(command_prefix = PREFIX, case_insensitive = True, owner_ids = OWNER_IDS, intents = intents)


  def setup(self):
    for cog in COGS:
      self.load_extension(f"lib.cogs.{cog}")


  def run(self, version):
    self.VERSION = version
    self.TOKEN = os.getenv('TOKEN')

    self.setup()

    super().run(self.TOKEN, reconnect = True)

    
  async def update_db(self):
    role_ids = [384846475915558926, 839696963909845003, 839697082910769192, 839697250929737759]
    basic_roles = [self.guild.get_role(role) for role in role_ids]
  
    for member in self.guild.members:
      if not member.bot:
        try:
          db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)
          await member.add_roles(*basic_roles)
          
        except:
          pass

    #db.multiexec("INSERT OR IGNORE INTO users (UserID) VALUES (?)", ((member.id,) for member in self.guild.members if not member.bot))

    inactive = []
    db_members = db.column("SELECT UserID FROM users")
    for id in db_members:
      if not self.guild.get_member(id):
        inactive.append(id)

    if inactive:     
      db.multiexec("UPDATE users SET Active = ? WHERE UserID = ?", ((0, id,) for id in inactive))
  
  
  async def process_commands(self, message):
    ctx = await self.get_context(message, cls = Context)

    if ctx.command is not None:
      await self.invoke(ctx)


  async def on_connect(self):
    print("Bot Connected")


  async def on_disconnect(self):
    print("Bot Disconnected")


  async def on_ready(self):
    if not self.ready:
      self.guild = self.get_guild(int(os.getenv('GUILD_ID')))

      #auto updates SQL database at 0:00:00 every day
      self.scheduler.add_job(self.update_db, CronTrigger(day_of_week = '*', hour = 0, minute = 0, second = 0))
      self.scheduler.start()

      await self.update_db()

      while not self.cogs_ready.all_ready():
        await sleep(0.5)

      self.ready = True
      #print("bot ready")
    
    else:
      print("Bot Reconnected\n")


  async def on_message(self, message):
    await self.process_commands(message)


bot = Bot()
