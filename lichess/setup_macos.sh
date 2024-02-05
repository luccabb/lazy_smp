#!/bin/bash

source .env

# build binary
read -p "Do you want to build a new binary? (y/n) " answer
answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')
if [[ "$answer" == "y" || "$answer" == "yes" ]]; then
    python -m PyInstaller main.py --onefile
fi

# fetch opening book if not already downloaded
git lfs fetch --all

# copy files
cp dist/main ../lichess-bot/engines/main
mkdir -p ../lichess-bot/engines/opening_book
cp opening_book/cerebellum.bin ../lichess-bot/engines/opening_book/cerebellum.bin
bash .env
envsubst < lichess/config.yml > ../lichess-bot/config.yml
