#!/bin/bash
nohup python3 -m http.server 8080 > server.log 2>&1 &
sleep 2
ssh -o StrictHostKeyChecking=no -R 80:localhost:8080 serveo.net > serveo.log 2>&1 &
sleep 5
grep -o 'https://[-a-zA-Z0-9]*\.serveo.net' serveo.log | head -1
