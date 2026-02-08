# Minecraft DiscordBot

directory

   
<img width="302" height="580" alt="image" src="https://github.com/user-attachments/assets/91fffff6-f0d0-43e9-90e7-cde7db35fb66" />



この `bots/` フォルダを、サーバールート配下に置いて使います。
ルートフォルダ名（MinecraftServer等）は変わってもOKで、`bots/` の親を「ルート」として扱います。

## 期待する配置
```
<server_root>/
  bluemap/ (optional)
  config/
  crash-reports/
  defaultconfigs/
  journeymap/
  libraries/
  logs/
  mods/
  world/
  bots/
    botprogram.py
    .env
    requirements.txt
    start_bot.bat
    <CLIENT_MODS>.zip   (MODS_COMMAND=direct のとき)
```

## セットアップ
1) 依存関係のインストール
```bat
cd /d <server_root>\bots
python -m pip install -r requirements.txt
```

2) `.env` を編集
最低限：
- DISCORD_TOKEN
- DISCORD_CHANNEL_ID
- RCON_HOST / RCON_PORT / RCON_PASSWORD
- RESTART_COMMAND（サーバー起動batのパス）

3) サーバー側でRCON有効化（server.properties）
- enable-rcon=true
- rcon.port / rcon.password を `.env` と一致

## 起動
`bots/start_bot.bat` を実行してください。
（このbatは必ずカレントを bots/ にするので `.env` が読み込まれます。）

## MOD zip（directの場合）
`CLIENT_MODS=client_mods` なら、`bots/client_mods.zip` を置きます。
