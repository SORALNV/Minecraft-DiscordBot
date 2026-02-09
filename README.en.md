[English](./README.en.md) | [日本語](./README.md)


# Minecraft Discord Bot

Minecraft server control bot for Discord.

Languages:
- English: `README.md`
- Japanese: `README.ja.md`

## Bot Features
- Slash command `/control` (admin only): posts the Minecraft control panel message.
- Slash command `/mods`: behavior is selected by `MODS_COMMAND`.
- `/mods=false`: command is disabled.
- `/mods=direct`: sends `bots/<CLIENT_MODS_DIRECTORY>.zip`.
- `/mods=url`: sends `MODS_URL`.
- Control panel button `Status`: shows online/offline, player list, CPU usage, memory usage.
- Control panel button `Set Morning`: sends RCON commands `/time set 300t` and `/weather clear`.
- Control panel button `Restart`: safe restart flow with checks, confirmation UI, lock protection, RCON `/stop`, then `RESTART_COMMAND`.
- Control panel button `BlueMap`: shown only when `BLUEMAP_URL` is set.
- Bot presence updates every 60 seconds to player count or `Offline`.
- Optional bot logs are sent to `BOT_LOG_CHANNEL_ID`.
- `start_bot.bat` auto-starts `setup_env.bat` when `.env` is missing.

## Feature Check Matrix
| Feature | Quick verification | Required `.env` keys |
|---|---|---|
| `/control` command | Run `/control` as admin and confirm panel message is posted | `DISCORD_TOKEN`, `DISCORD_CHANNEL_ID` |
| `Status` button | Press `Status` and confirm server/player/system info appears | `RCON_HOST`, `MINECRAFT_PORT` |
| `Set Morning` button | Press `Set Morning` and confirm time/weather changed | `RCON_HOST`, `RCON_PORT`, `RCON_PASSWORD` |
| `Restart` button | Press `Restart` with zero players, confirm server restarts | `RCON_HOST`, `RCON_PORT`, `RCON_PASSWORD`, `RESTART_COMMAND` |
| `/mods` disabled mode | Set `MODS_COMMAND=false`, run `/mods`, confirm disabled message | `MODS_COMMAND` |
| `/mods` direct mode | Set `MODS_COMMAND=direct`, set `CLIENT_MODS_DIRECTORY`, place zip, run `/mods` | `MODS_COMMAND`, `CLIENT_MODS_DIRECTORY` |
| `/mods` URL mode | Set `MODS_COMMAND=url`, set `MODS_URL`, run `/mods` | `MODS_COMMAND`, `MODS_URL` |
| BlueMap button | Set `BLUEMAP_URL`, run `/control`, confirm BlueMap button is shown | `BLUEMAP_URL` |
| Bot operation logs | Set `BOT_LOG_CHANNEL_ID`, perform button action, confirm log message | `BOT_LOG_CHANNEL_ID` |

## Quick Verification Steps
1. Run `setup_env.bat` and set required values for the feature you want to test.
2. Start bot with `start_bot.bat`.
3. Run `/control` in Discord as admin.
4. Press `Status` and confirm server status can be read.
5. Test one feature at a time using the matrix above.

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
    <CLIENT_MODS_DIRECTORY>.zip   (when MODS_COMMAND=direct)
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
| `DISCORD_CHANNEL_ID` | Channel ID where control panel is posted (required, must be greater than 0) |
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
| `CLIENT_MODS_DIRECTORY` | Used only when `MODS_COMMAND=direct`; zip name or path in `bots` folder |
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
If `.env` has `CLIENT_MODS_DIRECTORY=client_mods`, place this file:

```text
<server_root>/bots/client_mods.zip
```
