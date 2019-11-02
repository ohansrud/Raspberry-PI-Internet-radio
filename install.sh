#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"

SYSTEMD_UNIT="internet_radio"
cp ${SYSTEMD_UNIT}.service /etc/systemd/system/
cp -avr src /usr/local/sbin/${SYSTEMD_UNIT}

systemctl daemon-reload
systemctl enable ${SYSTEMD_UNIT}.service
systemctl restart ${SYSTEMD_UNIT}.service