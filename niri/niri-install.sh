sudo pacman -Suy && sudo pacman -S --needed --noconfirm git base-devel
git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si
cat apps.lst | tr '\n' ' ' | xargs yay -S --needed --noconfirm --asdeps
