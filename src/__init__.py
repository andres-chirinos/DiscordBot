from quart import Quart, redirect, url_for, render_template, flash, request, send_from_directory, make_response, jsonify, session
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from logging.config import dictConfig
from dotenv import load_dotenv
from discord.ext import commands
from metadata import *
import requests, json, os, redis, pymongo, asyncio, discord

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
load_dotenv(dotenv_path='.env')

#Memoria y cache interno
Cache = redis.from_url(url=os.getenv('REDIS_URL', "redis://default:ouBdBv91Z7t60rEfd0VL@containers-us-west-192.railway.app:7660"), decode_responses=True)
Memoria = pymongo.MongoClient(os.getenv('MONGO_URL', "mongodb://mongo:QoodY7GX6kzhHebGIo2Q@containers-us-west-94.railway.app:7993"))
guild_id = int(Cache.hget('appdata', 'guild_id'))

#print(register(Cache.hget('appdata', 'metadata')))

#Aplicación web
app = Quart(__name__, root_path='src')
app.secret_key = os.environ.get('CLIENT_SECRET')
discord_session = DiscordOAuth2Session(app, client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'), redirect_uri=os.environ.get('REDIRECT_URL', "http://localhost/ingresar/callback"), bot_token=os.environ.get('TOKEN'))

#Informativas
@app.route("/")
async def index():
    if session:
        return await render_template('index.html', user = await discord_session.fetch_user())
    return await render_template('index.html')

@app.route("/mapa/")
async def map():
    dynmap = Cache.hget('minecraft', 'serverdynmap')
    if session:
        return await render_template('map.html', dynmap = dynmap, user = await discord_session.fetch_user())
    return await render_template('map.html', dynmap = dynmap)

#Manejo de cuenta
@app.route("/ingresar/")
async def ingresar():
    if await discord_session.get_authorization_token():
        return redirect(url_for(".perfil"))
    else:
        return await discord_session.create_session(scope=['role_connections.write', 'identify'])

@app.route("/ingresar/callback/")
async def callback():
    await discord_session.callback()
    #await discord_session.save_authorization_token(await discord_session.get_authorization_token())
    return redirect(url_for(".perfil"))

@app.route("/salir/")
async def salir():
    discord_session.revoke()
    return redirect(url_for(".index"))

@app.route("/verificar/")
@requires_authorization
async def verificar():
    tokens = await discord_session.get_authorization_token()
    user = await discord_session.fetch_user()
    data = await get_role_connection(tokens['access_token'], Memoria, user.id)
    await push_role_connection(tokens['access_token'], body = data)
    return redirect(url_for(".perfil"))

@app.route("/perfil/", methods=['POST', 'GET'])
@requires_authorization
async def perfil():
    tokens = await discord_session.get_authorization_token()
    user = await discord_session.fetch_user()
    data = await get_role_connection(tokens['access_token'], Memoria, user.id)

    if request.method == 'POST':
        form = await request.form
        username = form['username']
        if len(username)>0 and username!=data['platform_username']:
            data['platform_username'] = username
            data['metadata'] = changedatabase(Memoria, user.id, data = { 'verified': False } )
        await push_role_connection(tokens['access_token'], body = data) 
    
    return await render_template('user.html', user = user, data = data)

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for(".ingresar"))

@app.errorhandler(Exception)
async def errorhandler(e):
    return await make_response(jsonify({"message": f'{e}'}),302)

#Aplicacion Discord
class MyBot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.initial_extensions = [
            'cogs.webhook',
            'cogs.thread',
            'cogs.utils',
            'cogs.message',
            'cogs.voice.voice',
            'cogs.minecraft',
            'cogs.listeners',
        ]
    
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild = discord.Object(id = guild_id)) 

    async def close(self):
        await super().close()

    async def on_ready(self):
        await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"""[{str(Cache.hget('appdata', 'prefix'))}] {str(Cache.hget('appdata', 'desc'))}"""))

    async def on_command_error(self, context, exception):
        print(exception, context)

    async def on_error(self, event_method):
        return await super().on_error(event_method)

bot = MyBot(command_prefix = commands.when_mentioned_or(str(Cache.hget('appdata', 'prefix'))), help_command = None, case_insensitive = True, description = str(Cache.hget('appdata', 'desc')), intents = discord.Intents.all(), aplicaction_id = int(os.environ.get('CLIENT_ID')))

#website start bot and periodic reflesh it
@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await bot.login(os.environ.get('TOKEN')) 
    loop.create_task(bot.connect(), name = 'Bot refresh')

if __name__ == "__main__":
    dictConfig({
        'version': 1,
        'loggers': {
            'quart.app': {
                'level': 'INFO',
                'formatter' : ' %(name)-8s - %(levelname)-8s - %(message)s',
            },
            'discord':{
                'level': 'INFO',
                'formatter' : ' %(name)-8s - %(levelname)-8s - %(message)s',
            }
        },
    })
    app.run(host=os.environ.get('HOST', None),port=os.environ.get('PORT', '80'), debug=True)