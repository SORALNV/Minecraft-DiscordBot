# Minecraft Discord Bot

Minecraft サーバーを Discord から確認・操作する Bot です。

## ディレクトリ構成
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
    <CLIENT_MODS>.zip   (MODS_COMMAND=direct の場合)
```

## インストール
```bat
cd /d <server_root>\bots
python -m pip install -r requirements.txt
```

## `.env` の作成方法A（エディター不要）
`setup_env.bat` を実行すると、対話形式で `.env` を作成・更新できます。

```bat
cd /d <server_root>\bots
setup_env.bat
```

### `setup_env.bat` の入力項目
| キー | 説明 |
|---|---|
| `DISCORD_TOKEN` | Discord Bot のトークン（必須） |
| `DISCORD_CHANNEL_ID` | コントロールパネルを送るチャンネルID |
| `BOT_LOG_CHANNEL_ID` | Botログ送信用チャンネルID（`0` で無効） |
| `RCON_HOST` | RCON 接続先ホスト |
| `RCON_PORT` | RCON ポート |
| `RCON_PASSWORD` | `server.properties` の `rcon.password` |
| `RESTART_COMMAND` | サーバー起動用 `.bat` のパス（絶対パス or サーバールート基準の相対パス） |
| `MINECRAFT_PORT` | 表示・監視に使う Minecraft ポート |
| `MINECRAFT_TYPE` | サーバー種別（例: Forge/Fabric/Vanilla） |
| `MINECRAFT_VER` | サーバーバージョン（例: `1.20.1`） |
| `MINECRAFT_IP` | 表示用アドレス |
| `MODS_COMMAND` | `/mods` の動作モード（`false` / `direct` / `url`） |
| `CLIENT_MODS` | `MODS_COMMAND=direct` のときのみ使用。`bots` 配下の ZIP 名（拡張子なし可） |
| `MODS_URL` | `MODS_COMMAND=url` のときのみ使用。配布URL |
| `BLUEMAP_URL` | BlueMap ボタンのリンク先。空欄なら BlueMap ボタン非表示 |

補足:
- `setup_env.bat` は最後に `.env` を直接更新します（`.env.bak` は作成しません）。
- `/mods` はモード選択に応じて入力項目が切り替わります。

## `.env` の作成方法B（エディターを使う）
`.env.sample` をコピーして `.env` に名前変更し、値を編集して使います。

```bat
cd /d <server_root>\bots
copy .env.sample .env
```

PowerShell の場合:

```powershell
Copy-Item .env.sample .env
```

## RCON 設定（サーバー側）
`server.properties` で以下を設定してください。

- `enable-rcon=true`
- `rcon.port` と `rcon.password` を `.env` と一致させる

## 起動
```bat
cd /d <server_root>\bots
start_bot.bat
```

`.env` が無い場合、`start_bot.bat` は `setup_env.bat` を自動で起動します。

## `/mods` direct モードの ZIP 配置
`.env` が `CLIENT_MODS=client_mods` の場合、以下に ZIP を置きます。

```text
<server_root>/bots/client_mods.zip
```
