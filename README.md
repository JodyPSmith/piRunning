# PiRunning
Work in progress - Raspberry Pi based python server to control Nordic track T 6.5 SI. Controller board "MC1648DLS ZE0824 Rev"

## install & command list
 - Prep a micro SD card with "Raspberry Pi OS Lite x64"
 - Login over ssh with username and password from set up
 - sudo su -
 - passwd root
 - enter new password twice
 - apt-get update
 - apt install python3-gpiozero vim
 - cd /opt 
 - git clone https://github.com/JodyPSmith/piRunning

## python setup
 - python -m venv .venv
 - python -m pip install --upgrade pip
 - source .venv/bin/activate (source ./.vanv/Scripts/activate on windows )
 - pip install "fastapi[standard]" gpiozero websockets
 - source .venv/bin/activate
 - fastapi run --port 80 server.py

## Svelte setup
 - npx sv create svelteFrontend
 - select minimal, no typescript, prettier & eslint plugin
 - npm run dev -- --open
 - npm i -D @sveltejs/adapter-static (used to allow static server of files from build folder)
 - svelte.config settings: adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: '200.html',
			precompress: false,
			strict: true
		})
 - add new file called +layout.js with "export const prerender = true;" one line of code
 - npm run build to build static files
