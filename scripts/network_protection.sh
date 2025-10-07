#!/bin/bash

HOST="172.16.0.5"
TARGET_URL="https://128.31.0.39"
USER="user"
PASS="password"

echo 'Executing network-based threat...'
sleep 1
echo "Running: curl $TARGET_URL on victim machine"

expect <<EOF
spawn ssh -o StrictHostKeyChecking=no $USER@$HOST "curl $TARGET_URL"
expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    "Password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}
EOF

echo 'Threat executed!'