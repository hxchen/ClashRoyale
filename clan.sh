#!/bin/sh
source /etc/profile
cd /data/web/battleship
python3 /data/web/battleship/clan.py >> /data/web/log/clan.log 2>&1