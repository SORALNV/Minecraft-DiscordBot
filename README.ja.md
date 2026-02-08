# Minecraft Discord Bot

Discord から Minecraft サーバーを操作・監視する Bot です。

言語:
- English: `README.md`
- 日本語: `README.ja.md`

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

#### 1) Discord
| キー | 説明 |
|---|---|
| `DISCORD_TOKEN` | Discord Bot トークン（必須） |
| `DISCORD_CHANNEL_ID` | コントロールパネルを投稿するチャンネルID |
| `BOT_LOG_CHANNEL_ID` | Bot ログ出力先チャンネルID（`0` で無効） |

#### 2) RCON と再起動
| キー | 説明 |
|---|---|
| `RCON_HOST` | RCON 接続先ホスト |
| `RCON_PORT` | RCON ポート |
| `RCON_PASSWORD` | `server.properties` の `rcon.password` |
| `RESTART_COMMAND` | サーバー起動用 `.bat` のパス（絶対パス / サーバールート基準の相対パス） |

#### 3) Minecraft 表示情報
| キー | 説明 |
|---|---|
| `MINECRAFT_PORT` | ステータス取得に使うゲームポート |
| `MINECRAFT_TYPE` | サーバー種別（例: Forge / Fabric / Vanilla） |
| `MINECRAFT_VER` | サーバーバージョン（例: `1.20.1`） |
| `MINECRAFT_IP` | コントロールパネルに表示するアドレス |

#### 4) `/mods` コマンド
| キー | 説明 |
|---|---|
| `MODS_COMMAND` | `/mods` のモード: `false` / `direct` / `url` |
| `CLIENT_MODS` | `MODS_COMMAND=direct` のときのみ使用。`bots` フォルダ内 ZIP 名 |
| `MODS_URL` | `MODS_COMMAND=url` のときのみ使用。配布URL |

`/mods` モードの挙動:
- `false`: `/mods` を無効化
- `direct`: ローカル ZIP を送信
- `url`: URL テキストを送信

#### 5) BlueMap
| キー | 説明 |
|---|---|
| `BLUEMAP_URL` | BlueMap のリンクURL。空欄ならボタン非表示 |

補足:
- `setup_env.bat` は `.env` を直接更新します（`.env.bak` は作成しません）。
- `/mods` の質問項目は選択モードに応じて切り替わります。

## `.env` の作成方法B（エディターを使う）
`.env.sample` を `.env` にコピーして名前を変更し、値を編集します。

```bat
cd /d <server_root>\bots
copy .env.sample .env
```

PowerShell:

```powershell
Copy-Item .env.sample .env
```

## RCON のサーバー側設定
`server.properties` に以下を設定してください。

- `enable-rcon=true`
- `rcon.port` と `rcon.password` を `.env` と一致させる

## 起動
```bat
cd /d <server_root>\bots
start_bot.bat
```

`.env` が存在しない場合、`start_bot.bat` が `setup_env.bat` を自動起動します。

## `/mods` direct モード時の ZIP 配置
`.env` が `CLIENT_MODS=client_mods` の場合、次の場所に配置します。

```text
<server_root>/bots/client_mods.zip
```
