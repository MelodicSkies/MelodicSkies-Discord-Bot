from discord.ext.commands import Cog, command
from discord.utils import get

from datetime import datetime, timedelta
import random
import os
from multiprocessing import Process
from asyncio import sleep

from ..db import db

class Userstats(Cog):
  def __init__(self, bot):
    self.bot = bot

  
  async def process_user_stats(self, message):
    self.guild = self.bot.get_guild(int(os.getenv('GUILD_ID')))
    xp_timelock, currency_timelock = db.record("SELECT XPLock, CurrencyLock FROM users WHERE UserID = ?", message.author.id)

    #debug
    print(f'message id: {message.id}')
    p1 = Process(target = self.update_xp(message, xp_timelock))
    p1.start()
    p2 = Process(target = self.update_currency(message, currency_timelock))
    p2.start()
    p1.join()
    p2.join()

  
  def update_xp(self, message, xp_timelock):
    xp = random.randint(15,25)

    if datetime.utcnow() > datetime.fromisoformat(xp_timelock):

      #debug
      print(f'{message.author.name} \nxp to be added: {xp}')
      print(f'current xp: {db.record("SELECT XP FROM users WHERE UserID = ?", message.author.id)[0]}')


      db.execute("UPDATE users SET XP = XP + ?, XPLock = ? WHERE UserID = ?", xp, (datetime.utcnow() + timedelta(seconds = 60)).isoformat(), message.author.id)

      #debug
      print(f'new xp: {db.record("SELECT XP FROM users WHERE UserID = ?", message.author.id)[0]}\n------------------------------------------\n')
    else:

      #debug
      print(f'{message.author.name}')
      print (f'current xp: {db.record("SELECT XP FROM users WHERE UserID = ?", message.author.id)[0]}\n------------------------------------------\n')


  def update_currency(self, message, currency_timelock):

    sub_multiplier = {
      "Twitch Subscriber: Tier 1" : 1.5,
      "Twitch Subscriber: Tier 2" : 2,
      "Twitch Subscriber: Tier 3" : 3
    }
    CURRENCY = 2

    if datetime.utcnow() > datetime.fromisoformat(currency_timelock):
      for key in sub_multiplier:
        role = get(self.guild.roles, name = key)
        if role in message.author.roles:
          currency = sub_multiplier[key] * CURRENCY
          db.execute("UPDATE users SET Currency = Currency + ?, CurrencyLock = ? WHERE UserID = ?", currency, (datetime.utcnow() + timedelta(seconds = 300)).isoformat(), message.author.id)
    
    else:
      pass


  @command(name = "stats")
  async def stats(self, ctx):
    Kappaccino = '<:coffeecup:840451076410834975>'
    await sleep(0.1)
    xp, currency = db.record("SELECT XP, Currency FROM users WHERE UserID = ?", ctx.author.id)
    
    await ctx.send(f"{ctx.author.name} has {xp} xp \n{ctx.author.name} has {currency} {Kappaccino}s")


  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("userstats")


  @Cog.listener()
  async def on_message(self, message):
    if not message.author.bot:
      await self.process_user_stats(message)



def setup(bot):
  bot.add_cog(Userstats(bot))