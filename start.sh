#!/usr/bin/env bash

chmod 777 ./server
chmod 777 ./client
mkdir venv
cd ./venv || exit
python3 -m venv .
source bin/activate
cd ../
pip install -r requirements.txt
cd ./client || exit
yarn install
cd ../
chmod 777 ./start-server.sh
chmod 777 ./start-client.sh
./start-server.sh &
./start-client.sh
