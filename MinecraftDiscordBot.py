# minecraft_discord_bot.py
from __future__ import annotations

import asyncio
import os
import subprocess
from datetime import datetime
from pathlib import Path

import discord
import psutil
from discord.ext import commands, tasks
from dotenv import load_dotenv
from mcstatus import JavaServer

BOT_DIR = Path(__file__).resolve().parent
SERVER_ROOT = BOT_DIR.parent

print(">>> Loading .env")
load_dotenv(BOT_DIR / ".env")
print(">>> .env loaded")


def env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"[WARN] {name} is not an int: {raw!r}. Using {default}.")
        return default


def env_required_int(name: str) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        print(f"[ERROR] {name} is missing in .env")
        raise SystemExit(1)
    try:
        value = int(raw)
    except ValueError:
        print(f"[ERROR] {name} must be an integer: {raw!r}")
        raise SystemExit(1)
    if value <= 0:
        print(f"[ERROR] {name} must be greater than 0.")
        raise SystemExit(1)
    return value


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("[ERROR] DISCORD_TOKEN is missing in .env")
    raise SystemExit(1)

CHANNEL_ID = env_required_int("DISCORD_CHANNEL_ID")
LOG_CHANNEL_ID = env_int("BOT_LOG_CHANNEL_ID", 0)
RESTART_COMMAND = os.getenv("RESTART_COMMAND", "").strip()
RCON_PASSWORD = os.getenv("RCON_PASSWORD", "")
RCON_PORT = env_int("RCON_PORT", 25575)
RCON_HOST = os.getenv("RCON_HOST", "localhost")
MINECRAFT_PORT = env_int("MINECRAFT_PORT", 25565)
MINECRAFT_VER = os.getenv("MINECRAFT_VER", "Unknown")
MINECRAFT_IP = os.getenv("MINECRAFT_IP", "Unknown")
BLUEMAP_URL = os.getenv("BLUEMAP_URL", "").strip()
MODS_COMMAND = os.getenv("MODS_COMMAND", "").strip().lower()
CLIENT_MODS_DIRECTORY = os.getenv("CLIENT_MODS_DIRECTORY", "").strip()
MODS_URL = os.getenv("MODS_URL", "").strip()
MINECRAFT_TYPE = os.getenv("MINECRAFT_TYPE", "Unknown")

RESTART_LOCK = asyncio.Lock()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents, activity=discord.Game("Starting..."))


def resolve_client_mods_path() -> Path | None:
    if not CLIENT_MODS_DIRECTORY:
        return None
    p = Path(CLIENT_MODS_DIRECTORY)
    if p.suffix.lower() != ".zip":
        p = p.with_suffix(".zip")
    if not p.is_absolute():
        p = BOT_DIR / p
    return p


def resolve_restart_command() -> Path | None:
    if not RESTART_COMMAND:
        return None
    raw = RESTART_COMMAND.strip('"')
    p = Path(raw)
    if not p.is_absolute():
        p = SERVER_ROOT / p
    return p


@bot.tree.command(name="mods", description="Send client mods (file or URL)")
async def send_mods(interaction: discord.Interaction):
    try:
        if MODS_COMMAND in ["false", "off", "disabled", ""]:
            await interaction.response.send_message("/mods is disabled.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        if MODS_COMMAND == "direct":
            path = resolve_client_mods_path()
            if not path:
                await interaction.followup.send("CLIENT_MODS_DIRECTORY is not set in .env", ephemeral=True)
                return
            if not path.exists():
                await interaction.followup.send(f"Mods file not found: {path}", ephemeral=True)
                return
            await interaction.followup.send(
                content=f"Mods file: {path.name}",
                file=discord.File(str(path)),
                ephemeral=True,
            )
            return

        if MODS_COMMAND == "url":
            if not MODS_URL:
                await interaction.followup.send("MODS_URL is not set in .env", ephemeral=True)
                return
            await interaction.followup.send(f"Mods URL: {MODS_URL}", ephemeral=True)
            return

        await interaction.followup.send(f"Invalid MODS_COMMAND: {MODS_COMMAND!r}", ephemeral=True)
    except Exception as e:
        print(f"[ERROR /mods] {e}")
        try:
            await interaction.followup.send("An error occurred.", ephemeral=True)
        except Exception:
            pass


class ControlPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(
                label="Status",
                style=discord.ButtonStyle.secondary,
                custom_id="status_button",
            )
        )
        self.add_item(
            discord.ui.Button(
                label="Set Morning",
                style=discord.ButtonStyle.success,
                custom_id="morning_button",
            )
        )
        if BLUEMAP_URL:
            self.add_item(
                discord.ui.Button(
                    label="BlueMap",
                    url=BLUEMAP_URL,
                    style=discord.ButtonStyle.link,
                )
            )
        self.add_item(
            discord.ui.Button(
                label="Restart",
                style=discord.ButtonStyle.danger,
                custom_id="restart_button",
            )
        )


def get_server_status() -> dict:
    try:
        server = JavaServer.lookup(f"{RCON_HOST}:{MINECRAFT_PORT}")
        status = server.status()
        if hasattr(status.players, "sample") and status.players.sample:
            players = ", ".join(player.name for player in status.players.sample)
        else:
            players = "No players listed"
        player_count = status.players.online
        return {"online": True, "players": players, "player_count": player_count}
    except Exception as e:
        print(f"[DEBUG] status error: {e}")
        return {"online": False, "players": None, "player_count": None}


def get_system_info() -> dict:
    memory = psutil.virtual_memory()
    cpu_percent = round(psutil.cpu_percent(interval=1) * 10, 1)
    return {
        "memory_percent": memory.percent,
        "memory_used": round(memory.used / (1024**3), 1),
        "memory_total": round(memory.total / (1024**3), 1),
        "cpu_percent": cpu_percent,
    }


async def log_to_channel(message: str):
    if LOG_CHANNEL_ID:
        channel = bot.get_channel(int(LOG_CHANNEL_ID))
        if channel:
            await channel.send(f"[BOTLOG] {message}")


@tasks.loop(seconds=60, reconnect=True)
async def update_status_loop():
    try:
        status = await asyncio.to_thread(get_server_status)
        if status.get("online"):
            count = int(status.get("player_count") or 0)
            name = f"{count} players online"
        else:
            name = "Offline"
        await bot.change_presence(activity=discord.Game(name=name))
        print(f"[LOOP] Presence: {name}")
    except Exception as e:
        print(f"[ERROR] update_status_loop: {e}")


@update_status_loop.before_loop
async def before_update_status_loop():
    await bot.wait_until_ready()
    try:
        status = await asyncio.to_thread(get_server_status)
        if status.get("online"):
            count = int(status.get("player_count") or 0)
            name = f"{count} players online"
        else:
            name = "Offline"
        await bot.change_presence(activity=discord.Game(name=name))
        print(f"[INIT] Presence: {name}")
    except Exception as e:
        print(f"[ERROR] before_update_status_loop: {e}")


@bot.event
async def on_ready():
    print(f"[INFO] Bot connected as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"[INFO] Synced {len(synced)} commands: {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"[WARN] Command sync failed: {e}")


@bot.tree.command(name="control", description="Send the control panel")
async def control_panel_command(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Admin only.", ephemeral=True)
        return

    embed = discord.Embed(title="Minecraft Control", color=discord.Color.blue())
    embed.add_field(name="MinecraftType", value=MINECRAFT_TYPE, inline=False)
    embed.add_field(name="MinecraftVer", value=MINECRAFT_VER, inline=False)
    embed.add_field(name="IP Address", value=MINECRAFT_IP, inline=False)

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed, view=ControlPanelView())
    else:
        print("[ERROR] CHANNEL_ID is invalid or not found")

    if not update_status_loop.is_running():
        update_status_loop.start()


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    cid = interaction.data.get("custom_id")

    if cid == "status_button":
        await interaction.response.defer(ephemeral=True)
        status = get_server_status()
        sysinfo = get_system_info()
        embed = discord.Embed(title="Server Status", color=discord.Color.green())
        if status["online"]:
            embed.add_field(name="Players Online", value=f"{status['player_count']}", inline=False)
            embed.add_field(name="Players", value=status["players"], inline=False)
        else:
            embed.add_field(name="Server", value="Offline", inline=False)
        embed.add_field(name="CPU", value=f"{sysinfo['cpu_percent']}%", inline=False)
        embed.add_field(
            name="Memory",
            value=f"{sysinfo['memory_percent']}% ({sysinfo['memory_used']} / {sysinfo['memory_total']} GB)",
            inline=False,
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    if cid == "morning_button":
        await interaction.response.defer(ephemeral=True)
        try:
            import mcrcon

            with mcrcon.MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as rcon:
                rcon.command("/time set 300t")
                rcon.command("/weather clear")
            await interaction.followup.send("Set to morning and clear weather.", ephemeral=True)
            user = interaction.user
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await log_to_channel(f"Morning set by {user.name} at {timestamp}")
        except Exception as e:
            await interaction.followup.send("Failed to send RCON command.", ephemeral=True)
            await log_to_channel(f"Morning command failed: {e}")
        return

    if cid == "restart_button":
        status = get_server_status()
        if not status.get("online"):
            await interaction.response.send_message("Server is offline.", ephemeral=True)
            return
        if status.get("player_count", 0) > 0:
            await interaction.response.send_message("Players are online. Try later.", ephemeral=True)
            return

        view = discord.ui.View(timeout=30)

        confirm_btn = discord.ui.Button(
            label="Confirm Restart",
            style=discord.ButtonStyle.danger,
            custom_id="restart_confirm",
        )
        cancel_btn = discord.ui.Button(
            label="Cancel",
            style=discord.ButtonStyle.secondary,
            custom_id="restart_cancel",
        )

        async def disable_view_and_edit(i: discord.Interaction, content: str):
            for item in view.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
            await i.edit_original_response(content=content, view=view)

        async def confirm_callback(i: discord.Interaction):
            await i.response.defer(ephemeral=True)

            if RESTART_LOCK.locked():
                await disable_view_and_edit(i, "Restart already in progress.")
                return

            st = get_server_status()
            if not st.get("online"):
                await disable_view_and_edit(i, "Server is already offline.")
                return
            if st.get("player_count", 0) > 0:
                await disable_view_and_edit(i, "Players are online. Try later.")
                return

            async with RESTART_LOCK:
                try:
                    import mcrcon

                    with mcrcon.MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as rcon:
                        rcon.command("/stop")
                    await asyncio.sleep(5)

                    bat_path = resolve_restart_command()
                    if not bat_path:
                        raise RuntimeError("RESTART_COMMAND is not set")

                    CREATE_NEW_CONSOLE = 0x00000010
                    subprocess.Popen(
                        ["cmd", "/c", "start", "", str(bat_path)],
                        cwd=str(bat_path.parent),
                        creationflags=CREATE_NEW_CONSOLE,
                    )

                    await disable_view_and_edit(i, "Restarted the server.")
                    await log_to_channel(f"/restart by {i.user} ({i.user.id})")
                except Exception as e:
                    await disable_view_and_edit(i, "Restart failed.")
                    await log_to_channel(f"/restart failed: {e!r} by {i.user} ({i.user.id})")

        async def cancel_callback(i: discord.Interaction):
            await i.response.defer(ephemeral=True)
            await disable_view_and_edit(i, "Cancelled.")

        confirm_btn.callback = confirm_callback
        cancel_btn.callback = cancel_callback
        view.add_item(confirm_btn)
        view.add_item(cancel_btn)

        async def on_timeout():
            for item in view.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
            try:
                await msg.edit(content="Timed out.", view=view)
            except Exception:
                pass

        view.on_timeout = on_timeout

        await interaction.response.send_message("Confirm server restart?", view=view, ephemeral=True)
        msg = await interaction.original_response()


try:
    print(">>> bot.run()")
    bot.run(TOKEN)
except Exception as e:
    print(f"[ERROR] BOT failed: {e}")
