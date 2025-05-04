cat apps.lst | tr '\n' ' ' | xargs yay -S --needed --noconfirm --asdeps
