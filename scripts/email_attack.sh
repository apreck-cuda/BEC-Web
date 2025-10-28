#!/bin/bash
echo 'Simulating email attack...'
sleep 1
echo "Running python script to simulate the attack" 
echo "" | python3 -u scripts/replay_customers.py scripts/num2-all.zip
echo "Done!"