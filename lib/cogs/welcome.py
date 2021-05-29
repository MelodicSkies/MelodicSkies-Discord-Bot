from discord.ext.commands import Cog
from discord import File
from PIL import Image, ImageDraw, ImageFont
import os
import io
from ..db import db

class Welcome(Cog):
  def __init__(self, bot):
    self.bot = bot


  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("welcome")


  @Cog.listener()
  async def on_member_join(self, member):
    
    if not member.bot:
      try: 
        db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)

      except:
        db.execute("UPDATE users SET Active = ? WHERE UserID = ?", 1, member.id)


    role_ids = [384846475915558926, 839696963909845003, 839697082910769192, 839697250929737759]
    basic_roles = [member.guild.get_role(role) for role in role_ids]
    await member.add_roles(*basic_roles)


    channel = self.bot.get_channel(int(os.getenv('WELCOME_CHANNEL_ID')))
    print("images")
    image = Image.open('assets/images/welcome banner background.png')

    IMAGE_WIDTH, IMAGE_HEIGHT = image.size

    image.resize(image.size, resample = 2)
    alert = ImageDraw.Draw(image)
  
    text = f'{member.name} #{member.discriminator}'
    font = ImageFont.truetype('fonts/Italianno-Regular.ttf', 100)

    text_width, text_height = alert.textsize(text, font = font)
    x = (IMAGE_WIDTH - text_width - 15)
    y = (IMAGE_HEIGHT - 78) + ((78 - text_height) // 2) - 15

    alert.text((x,y), text, font = font, fill = (255, 255, 255, 255))
  
    AVATAR_SIZE = 512
    avatar = member.avatar_url_as(format = 'jpg', size = AVATAR_SIZE)

    

    avatar_buffer = io.BytesIO()
    await avatar.save(avatar_buffer)
    avatar_buffer.seek(0)

    

    avatar_jpg = Image.open(avatar_buffer)
    AVATAR_WIDTH, AVATAR_HEIGHT = avatar_jpg.size


    avatar_jpg = avatar_jpg.resize((512,512), Image.ANTIALIAS)
    print(f'{AVATAR_WIDTH} x {AVATAR_HEIGHT}')

    circle_mask = Image.new('L', (AVATAR_SIZE, AVATAR_SIZE))
    circle_draw = ImageDraw.Draw(circle_mask)
    circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill = 255)
    x = (IMAGE_WIDTH - AVATAR_SIZE) // 2
    y = 365

    image.paste(avatar_jpg, (int(x),int(y)), circle_mask)

    buffer_output = io.BytesIO()
    image.save(buffer_output, format = 'PNG')
    buffer_output.seek(0)

    await channel.send(file = File(buffer_output, 'welcome.png'))




  @Cog.listener()
  async def on_member_remove(self, member):
    db.execute("UPDATE users SET Active = ? WHERE UserID = ?", 0, member.id)

def setup(bot):
  bot.add_cog(Welcome(bot))