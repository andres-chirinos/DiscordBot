import discord
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime

async def passport(interaction: discord.Interaction, user: discord.Member, nick:str, gender:str, place:str):
    passport = Image.open('cogs/register/passport.png')
    #Image
    asset = user.avatar.with_size(128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((170,200))
    passport.paste(pfp, (35,420))

    #Text
    FontA = ImageFont.truetype('cogs/register/minecraft_font.ttf', 30)
    Fonta = ImageFont.truetype('cogs/register/minecraft_font.ttf', 24)
    Textpass = ImageDraw.Draw(passport) 
    format = '%Y-%m-%d'
    Textpass.text((145, 120), f'{datetime.utcnow().strftime(format)}', font=Fonta, fill =(81, 111, 22))
    Textpass.text((40, 370), f'{nick}', font=FontA, fill =(0, 0, 0))
    Textpass.text((290, 420), f'{user.created_at.strftime(format)}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((290, 450), f'{gender}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((290, 490), f'{place}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((290, 520), f'{user.joined_at.strftime(format)}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((280, 580), f'{interaction.guild.name}', font=FontA, fill =(0, 0, 0))
    Textpass.text((35, 635), f'{user.id}', font=Fonta, fill =(0, 0, 0))

    passport.save('cogs/register/register.png')
    return discord.File('cogs/register/register.png')

async def diplomaticpermit(interaction: discord.Interaction, user: discord.Member, nick:str, country:str):
    diplomaticpermit = Image.open('cogs/register/diplomaticpermit.png')

    #Text
    FontA = ImageFont.truetype('cogs/register/minecraft_font.ttf', 14)
    Fonta = ImageFont.truetype('cogs/register/minecraft_font.ttf', 10)
    Textpass = ImageDraw.Draw(diplomaticpermit) 

    Textpass.text((80, 5), f'{interaction.guild.name}', font=FontA, fill =(0, 0, 0))
    Textpass.text((200, 155), f'{interaction.guild.name}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((80, 185), f'{nick}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((105, 200), f'{user.id}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((40, 300), f'{country}', font=FontA, fill =(0, 0, 0))
    format = '%Y-%m-%d'
    Textpass.text((45, 340), f'{datetime.utcnow().strftime(format)}', font=Fonta, fill =(81, 111, 22))

    diplomaticpermit.save('cogs/register/register.png')
    return discord.File('cogs/register/register.png')

async def entrypermit(interaction: discord.Interaction, user: discord.Member, nick:str, purpose:str, place:str):
    entrypermit = Image.open('cogs/register/entrypermit.png')

    #Text
    FontA = ImageFont.truetype('cogs/register/minecraft_font.ttf', 30)
    Fonta = ImageFont.truetype('cogs/register/minecraft_font.ttf', 24)
    Textpass = ImageDraw.Draw(entrypermit) 

    Textpass.text((100, 20), f'{interaction.guild.name}', font=FontA, fill =(0, 0, 0))
    Textpass.text((185, 135), f'{interaction.guild.name}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((30, 165), f'{nick}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((30, 240), f'{user.id}', font=Fonta, fill =(0, 0, 0))
    Textpass.text((105, 275), f'{purpose}', font=Fonta, fill =(0, 0, 0))
    format = '%Y-%m-%d'
    Textpass.text((105, 335), f'{datetime.utcnow().strftime(format)}', font=Fonta, fill =(81, 111, 22))

    entrypermit.save('cogs/register/register.png')
    return discord.File('cogs/register/register.png')