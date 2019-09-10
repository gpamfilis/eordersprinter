#!/usr/bin/env bash
git fetch --all
git reset --hard origin/master
pip3 install -r requirements.txt
sudo -E python3 order_greeklish_temp.py
