# Minecraft Discord Bot

Minecraft server control bot for Discord.

## Directory Layout
```text
<server_root>/
  bluemap/ (optional)
  config/
  crash-reports/
  defaultconfigs/
  logs/
  mods/
  world/
  bots/
    MinecraftDiscordBot.py
    start_bot.bat
    setup_env.bat
    .env.sample
    .env
    requirements.txt
    <CLIENT_MODS>.zip   (when MODS_COMMAND=direct)
```

## Install
```bat
cd /d <server_root>\bots
python -m pip install -r requirements.txt
```

## `.env` Method A (No Editor)
Run `setup_env.bat` to create or update `.env` interactively.

```bat
cd /d <server_root>\bots
setup_env.bat
```

### `setup_env.bat` Input Fields

#### 1) Discord
| Key | Description |
|---|---|
| `DISCORD_TOKEN` | Discord bot token (required) |
| `DISCORD_CHANNEL_ID` | Channel ID where control panel is posted |
| `BOT_LOG_CHANNEL_ID` | Bot log channel ID (`0` to disable) |

#### 2) RCON and Restart
| Key | Description |
|---|---|
| `RCON_HOST` | RCON host |
| `RCON_PORT` | RCON port |
| `RCON_PASSWORD` | RCON password from `server.properties` |
| `RESTART_COMMAND` | Path to server start `.bat` (absolute path or relative from server root) |

#### 3) Minecraft Info Display
| Key | Description |
|---|---|
| `MINECRAFT_PORT` | Minecraft game port for status lookup |
| `MINECRAFT_TYPE` | Server type (example: Forge / Fabric / Vanilla) |
| `MINECRAFT_VER` | Server version (example: `1.20.1`) |
| `MINECRAFT_IP` | Address shown in control panel |

#### 4) `/mods` Command
| Key | Description |
|---|---|
| `MODS_COMMAND` | `/mods` mode: `false` / `direct` / `url` |
| `CLIENT_MODS` | Used only when `MODS_COMMAND=direct`; zip name in `bots` folder |
| `MODS_URL` | Used only when `MODS_COMMAND=url`; download URL |

`/mods` mode behavior:
- `false`: disable `/mods`
- `direct`: send local zip file
- `url`: send URL text

#### 5) BlueMap
| Key | Description |
|---|---|
| `BLUEMAP_URL` | BlueMap link URL; button is hidden when empty |

Notes:
- `setup_env.bat` updates `.env` directly (does not create `.env.bak`).
- `/mods` input questions change based on selected mode.

## `.env` Method B (Use an Editor)
Copy `.env.sample` to `.env`, rename it, then edit values.

```bat
cd /d <server_root>\bots
copy .env.sample .env
```

PowerShell:

```powershell
Copy-Item .env.sample .env
```

## RCON Server Settings
Set the following in `server.properties`:

- `enable-rcon=true`
- `rcon.port` and `rcon.password` must match `.env`

## Start Bot
```bat
cd /d <server_root>\bots
start_bot.bat
```

If `.env` does not exist, `start_bot.bat` starts `setup_env.bat` automatically.

## `/mods` Direct Mode Zip Location
If `.env` has `CLIENT_MODS=client_mods`, place this file:

```text
<server_root>/bots/client_mods.zip
```
