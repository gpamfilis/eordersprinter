#!/usr/bin/env bash
cd eorders
cd eordersprinter
git fetch --all
git reset --hard origin/master
pip3 install -r requirements.txt
sudo -E python3 order_greeklish_temp.py
