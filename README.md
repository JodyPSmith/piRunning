# PiRunning
Work in progress - Raspberry Pi based python server to control Nordic track T 6.5 SI. Controller board "MC1648DLS ZE0824 Rev"

## install & command list
 - Prep a micro SD card with "Raspberry Pi OS Lite x64"
 - Login over ssh with username and password from set up
 > sudo su -
 > passwd root
 - enter new password twice
 > apt-get update
 > apt install python3-gpiozero vim
 > cd /opt 
 > git clone https://github.com/JodyPSmith/piRunning

## python setup
 > python -m pip install --upgrade pip
 > python -m venv .venv
 > source .venv/bin/activate
 > pip install "fastapi[standard]"
 > pip install gpiozero
 > source .venv/bin/activate
 > fastapi run server.py

