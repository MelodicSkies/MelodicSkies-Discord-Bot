from discord.ext.commands import Cog
from discord import File

import os
import json
from ..db import db

class Roles(Cog):
  def __init__(self, bot):
    self.bot = bot


  async def post_roles(self):
    channel = self.bot.get_channel(int(os.getenv('ROLE_CHANNEL_ID')))
    messages = await channel.history(limit = 1).flatten()
    if not messages:
      roles_file = open('assets/roles.json', 'r')

      config = json.load(roles_file)

      await channel.send(file = File('assets/images/roles.png', 'role.png'))
      COFFEE_EMOTE = '<:coffeecup:840451076410834975>'
      general_roles, location_roles, game_roles, hobby_roles, purchasable_roles = [f"*•.¸\n[{COFFEE_EMOTE}]\n"] * 5
      for section in config['roles'][0]['general']:
        general_roles += f"● <@&{section['role_id']}> - {section['role_description']}\n"
      await channel.send(general_roles)

      await channel.send(file = File('assets/images/location.png', 'location.png'))
      for section in config['roles'][0]['location']:
        location_roles += f"● <a:{section['emote_name']}:{section['emote_id']}>     <@&{section['role_id']}>\n"
        db.execute("INSERT OR IGNORE INTO roles (EmoteID, RoleID) VALUES (?, ?)", section['emote_id'], section['role_id'])
      message = await channel.send(location_roles)
      for section in config['roles'][0]['location']:
        await message.add_reaction(f"<a:{section['emote_name']}:{section['emote_id']}>")

      await channel.send(file = File('assets/images/games.png', 'games.png'))
      for section in config['roles'][0]['games']:
        game_roles += f"● <a:{section['emote_name']}:{section['emote_id']}>     <@&{section['role_id']}>\n"
        db.execute("INSERT OR IGNORE INTO roles (EmoteID, RoleID) VALUES (?, ?)", section['emote_id'], section['role_id'])
      message = await channel.send(game_roles)
      for section in config['roles'][0]['games']:
        await message.add_reaction(f"<a:{section['emote_name']}:{section['emote_id']}>")

      await channel.send(file = File('assets/images/hobbies.png', 'hobbies.png'))
      for section in config['roles'][0]['hobbies']:
        hobby_roles += f"● <a:{section['emote_name']}:{section['emote_id']}>     <@&{section['role_id']}>\n"
        db.execute("INSERT OR IGNORE INTO roles (EmoteID, RoleID) VALUES (?, ?)", section['emote_id'], section['role_id'])
      message = await channel.send(hobby_roles)
      for section in config['roles'][0]['hobbies']:
        await message.add_reaction(f"<a:{section['emote_name']}:{section['emote_id']}>")

      await channel.send(file = File('assets/images/purchasable.png', 'purchasable.png'))
      for section in config['roles'][0]['purchasable']:
        purchasable_roles += f"● <@&{section['role_id']}>\n"
      await channel.send(purchasable_roles)

  #test function
  """def update_roles(self):
    roles_file = open('assets/roles.json', 'r')

    config = json.load(roles_file)

    for section in config['roles'][0]['location']:
      db.execute("INSERT OR IGNORE INTO roles (EmoteID, RoleID) VALUES (?, ?)", section['emote_id'], section['role_id'])
      
    for section in config['roles'][0]['games']:
      db.execute("INSERT OR IGNORE INTO roles (EmoteID, RoleID) VALUES (?, ?)", section['emote_id'], section['role_id'])
      
    for section in config['roles'][0]['hobbies']:
      db.execute("INSERT OR IGNORE INTO roles (EmoteID, RoleID) VALUES (?, ?)", section['emote_id'], section['role_id'])"""

  def update_roles(self):
    role_message_ids = ['f']

    for id in role_message_ids:
      pass


  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      await self.post_roles()
      self.update_roles()
      self.bot.cogs_ready.ready_up('roles')
      

  @Cog.listener()
  async def on_raw_reaction_add(self, payload):
    member = self.bot.guild.get_member(payload.user_id)
    try:
      role_id = db.record("SELECT RoleID FROM roles WHERE EmoteID = ?", payload.emoji.id)[0]
      await member.add_roles(self.bot.guild.get_role(role_id))
    except:
      pass


  @Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    member = self.bot.guild.get_member(payload.user_id)
    try:
      role_id = db.record("SELECT RoleID FROM roles WHERE EmoteID = ?", payload.emoji.id)[0]
      await member.remove_roles(self.bot.guild.get_role(role_id))
    except:
      pass


def setup(bot):
  bot.add_cog(Roles(bot))