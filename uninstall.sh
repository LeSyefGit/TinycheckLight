# Checking rights.
if [[ $EUID -ne 0 ]]; then
    echo "The update must be run as root. Type in 'sudo bash $0' to run it as root."
	exit 1
else

    echo "[+] Deleting TinyCheck folders"

    rm -rf /usr/share/tinycheck/

    echo "[+] Deleting TinyCheck services"

    systemctl disable tinycheck-frontend
    systemctl disable tinycheck-backend
    systemctl disable tinycheck-kiosk
    systemctl disable tinycheck-watchers

    rm /lib/systemd/system/tinycheck-frontend.service
    rm /lib/systemd/system/tinycheck-backend.service
    rm /lib/systemd/system/tinycheck-kiosk.service
    rm /lib/systemd/system/tinycheck-watchers.service

    echo "[+] Updating dnsmasq and dhcpcd configuration files"

    sed -i '/## TinyCheck configuration ##/,$d' /etc/dnsmasq.conf
    sed -i '/## TinyCheck configuration ##/,$d' /etc/dhcpcd.conf

    echo "[+] Deleting desktop icon"

    rm "/home/${SUDO_USER}/Desktop/tinycheck.desktop"

    echo "[+] TinyCheck uninstalled!"
fi