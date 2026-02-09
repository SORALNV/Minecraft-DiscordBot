[English](./README.en.md) | [日本語](./README.md)

# Minecraft Discord Bot

Discord から Minecraft サーバーを操作・監視する Bot です。

言語:
- English: `README.md`
- 日本語: `README.ja.md`

## BOTの機能
- スラッシュコマンド `/control`（管理者のみ）: Minecraft のコントロールパネルを投稿します。
- スラッシュコマンド `/mods`: `MODS_COMMAND` の設定で動作が切り替わります。
- `MODS_COMMAND=false`: `/mods` を無効化します。
- `MODS_COMMAND=direct`: `bots/<CLIENT_MODS>.zip` を送信します。
- `MODS_COMMAND=url`: `MODS_URL` を送信します。
- コントロールパネル `Status` ボタン: サーバーのオンライン状態、プレイヤー一覧、CPU使用率、メモリ使用率を表示します。
- コントロールパネル `Set Morning` ボタン: RCON で `/time set 300t` と `/weather clear` を実行します。
- コントロールパネル `Restart` ボタン: 事前チェック、確認UI、同時実行ロック、RCON `/stop`、`RESTART_COMMAND` 実行の順で安全に再起動します。
- コントロールパネル `BlueMap` ボタン: `BLUEMAP_URL` が設定されている場合のみ表示します。
- Bot のプレゼンスは60秒ごとに更新され、プレイヤー数または `Offline` を表示します。
- `BOT_LOG_CHANNEL_ID` が設定されている場合、操作ログを送信します。
- `.env` が無い場合は `start_bot.bat` から `setup_env.bat` を自動起動します。

## 機能確認マトリクス
| 機能 | かんたんな確認方法 | 必要な `.env` キー |
|---|---|---|
| `/control` コマンド | 管理者で `/control` を実行し、パネル投稿を確認 | `DISCORD_TOKEN`, `DISCORD_CHANNEL_ID` |
| `Status` ボタン | `Status` を押し、サーバー・プレイヤー・システム情報を確認 | `RCON_HOST`, `MINECRAFT_PORT` |
| `Set Morning` ボタン | `Set Morning` を押し、時間と天候の変更を確認 | `RCON_HOST`, `RCON_PORT`, `RCON_PASSWORD` |
| `Restart` ボタン | プレイヤー0人で `Restart` 実行、再起動を確認 | `RCON_HOST`, `RCON_PORT`, `RCON_PASSWORD`, `RESTART_COMMAND` |
| `/mods` 無効モード | `MODS_COMMAND=false` で `/mods` 実行、無効メッセージを確認 | `MODS_COMMAND` |
| `/mods` direct モード | `MODS_COMMAND=direct` と `CLIENT_MODS` 設定、ZIP配置後に `/mods` 実行 | `MODS_COMMAND`, `CLIENT_MODS` |
| `/mods` url モード | `MODS_COMMAND=url` と `MODS_URL` 設定後に `/mods` 実行 | `MODS_COMMAND`, `MODS_URL` |
| BlueMap ボタン | `BLUEMAP_URL` を設定し `/control` 実行、BlueMap ボタン表示を確認 | `BLUEMAP_URL` |
| 操作ログ送信 | `BOT_LOG_CHANNEL_ID` 設定後に操作し、ログ投稿を確認 | `BOT_LOG_CHANNEL_ID` |

## クイック確認手順
1. `setup_env.bat` を実行し、確認したい機能に必要な値を設定します。
2. `start_bot.bat` で Bot を起動します。
3. Discord で管理者として `/control` を実行します。
4. `Status` を押して、サーバー状態を取得できることを確認します。
5. 上のマトリクスに沿って、1機能ずつ確認します。

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
