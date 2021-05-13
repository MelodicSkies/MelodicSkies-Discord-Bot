from discord.ext.commands import Cog, command, has_permissions

from ..db import db


#for debugging only
class Test(Cog):
  def __init__(self, bot):
    self.bot = bot

  @command(name = 'test')
  async def test(self, ctx):
    Kappaccino = '<:coffeecup:840451076410834975>'
    xp, currency = db.record("SELECT XP, Currency FROM users WHERE UserID = ?", ctx.author.id)
    
    await ctx.send(f"{ctx.author.name} has {xp} xp \n{ctx.author.name} has {currency} {Kappaccino}s")


  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("test")


def setup(bot):
  bot.add_cog(Test(bot))