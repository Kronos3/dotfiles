#!/bin/bash

git clone https://github.com/adi1090x/rofi.git ~/git/dotfiles/rofi
cd ~/git/dotfiles/rofi
./setup.sh

systemctl --user start pulseaudio
systemctl --user enable pulseaudio

