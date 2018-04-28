#!/bin/sh
source /etc/profile
cd /data/web/battleship
python3 /data/web/battleship/fetch.py >> /data/web/log/cr.log 2>&1