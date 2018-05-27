#!/bin/sh
source /etc/profile
cd /data/web/battleship
python3 /data/web/battleship/war.py >> /data/web/log/war.log 2>&1