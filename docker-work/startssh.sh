#!/bin/bash
sleep 1
mkdir -p /run/sshd
chmod 0755 /run/sshd
chown root:sys /run/sshd
/usr/sbin/sshd -D
bash