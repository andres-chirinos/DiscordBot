from quart import (
    Quart,
    redirect,
    url_for,
    render_template,
    request,
    make_response,
    jsonify,
    session,
    flash,
    g,
)
from quart_discord import *
from logging.config import dictConfig
from dotenv import load_dotenv
from discord.ext import commands
from memory import *
import os, redis, asyncio, discord

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
load_dotenv(dotenv_path=".env")

# Memoria y cache interno
Cache = redis.from_url(
    url=os.getenv(
        "REDIS_URL",
        "redis://default:ouBdBv91Z7t60rEfd0VL@containers-us-west-192.railway.app:7660",
    ),
    decode_responses=True,
)
guild_id = int(Cache.hget("appdata", "guild_id"))

# Aplicación web
url = os.getenv("URI", "http://localhost/")


app = Quart(__name__, root_path="src")
app.secret_key = os.environ.get("DISCORD_CLIENT_SECRET")
app.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = url + "oauth/callback"


discord_session = DiscordOAuth2Session(app)
dynmap = Cache.hget("minecraft", "serverdynmap")


#@app.url_defaults
#def defaults(endpoint, values):
#    print("def", endpoint, values)


#@app.url_value_preprocessor
#def preprocessor(endpoint, values):
#    print("pre", endpoint, values)


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/oauth/<path:path>")
async def oauth(path):
    return await discord_session.create_session(
        scope=["role_connections.write", "identify"],
        prompt=True,
        data={"redirect": path},
    )


@app.route("/oauth/callback/")
async def callback():
    data = await discord_session.callback()
    await flash(message="Ha ingresado correctamente", category="info")
    return redirect(url + data["redirect"])


@app.route("/oauth/close/")
async def close():
    discord_session.revoke()
    return redirect(url_for(".index"))


@app.route("/verify/")
@requires_authorization
async def verify():
    token = await discord_session.get_authorization_token()
    user = await discord_session.fetch_user()
    body = await get_role_connection(user.id)
    await push_role_connection(token, body)
    return """Puedes volver a Discord ó haz click <a href="/profile/">aquí</a> para ir a tu profile."""


@app.route("/profile/", methods=["POST", "GET"])
@requires_authorization
async def profile():
    user = await discord_session.fetch_user()

    if request.method == "POST":
        form = await request.form
        if len(form["username"]) >= 3:
            await update_one(
                "master",
                str(user.id),
                {"type": "identification"},
                {"$set": {"platform_username": form["username"], "verified": False}},
            )
    data = await find_one("master", str(user.id), {"type": "identification"})
    if not data:
        await insert_one(
            "master",
            str(user.id),
            {
                "type": "identification",
                "platform_username": None,
                "verified": False,
                "rank": 0,
            },
        )
        data = await find_one("master", str(user.id), {"type": "identification"})

    return await render_template("user.html", user=user, data=data)


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    await flash(message="No esta autorizado", category="warning")
    return redirect(url_for(".oauth", path=request.path))


@app.errorhandler(RateLimited)
async def rate_limited(e):
    await flash(message="Estas siendo limitado", category="warning")
    return redirect(url_for(".profile"))


@app.errorhandler(AccessDenied)
async def access_denied(e):
    await flash(message="Acceso denegado", category="error")
    return redirect(url_for(".index"))


@app.errorhandler(HttpException)
async def http_exception(e):
    return await make_response(jsonify({"message": f"{e}"}), 302)


# Aplicacion Discord
class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial_extensions = [
            "cogs.webhook",
            "cogs.thread",
            "cogs.metadata",
            "cogs.message",
            "cogs.voice.voice",
            "cogs.minecraft",
            "cogs.listeners",
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(id=guild_id))

    async def close(self):
        await super().close()

    async def on_ready(self):
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(
                f"""[{str(Cache.hget('appdata', 'prefix'))}] {str(Cache.hget('appdata', 'desc'))}"""
            ),
        )

    async def on_command_error(self, context, exception):
        print(exception, context)

    async def on_error(self, event_method):
        return await super().on_error(event_method)


bot = MyBot(
    command_prefix=commands.when_mentioned_or(str(Cache.hget("appdata", "prefix"))),
    help_command=None,
    case_insensitive=True,
    description=str(Cache.hget("appdata", "desc")),
    intents=discord.Intents.all(),
    aplicaction_id=int(os.environ.get("DISCORD_CLIENT_ID")),
)


# website start bot and periodic reflesh it
@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await bot.login(os.environ.get('DISCORD_BOT_TOKEN'))
    loop.create_task(bot.connect(), name="Bot refresh")


if __name__ == "__main__":
    dictConfig(
        {
            "version": 1,
            "loggers": {
                "quart.app": {
                    "level": "INFO",
                    "formatter": " %(name)-8s - %(levelname)-8s - %(message)s",
                },
                "discord": {
                    "level": "INFO",
                    "formatter": " %(name)-8s - %(levelname)-8s - %(message)s",
                },
            },
        }
    )
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"), port=os.environ.get("PORT", "80"), debug=True
    )
