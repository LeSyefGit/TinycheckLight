#!/bin/bash

# This small script is started by the service tinycheck-kiosk
# in order to launch TinyCheck frontend in kiosk mode. 

xset s noblank
xset s off
xset -dpms

if grep 'hide_mouse: true' /usr/share/tinycheck/config.yaml; then
    unclutter -idle 0 &
fi

if grep 'kiosk_mode: true' /usr/share/tinycheck/config.yaml; then
    sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
    sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

    /usr/bin/chromium-browser  http://127.0.0.1 --start-fullscreen --kiosk --incognito --noerrdialogs --disable-translate --no-first-run --fast --fast-start --disable-infobars --disable-features=TranslateUI &
fi