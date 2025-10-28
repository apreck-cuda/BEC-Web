#!/bin/bash
echo 'Simulating Accoutn take over attack...'
sleep 1
echo "Running powershell script to simulate the attack" 
echo "" | python3 -u scripts/replay_customers.py scripts/num2-all.zip
echo "Done!"