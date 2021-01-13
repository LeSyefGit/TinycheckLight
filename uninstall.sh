
delete_folder(){
    echo "[+] Deleting TinyCheck folders"
    rm -rf /usr/share/tinycheck/
}

delete_services(){
    echo "[+] Deleting TinyCheck services"

    systemctl disable tinycheck-frontend
    systemctl disable tinycheck-backend
    systemctl disable tinycheck-kiosk
    systemctl disable tinycheck-watchers

    rm /lib/systemd/system/tinycheck-frontend.service
    rm /lib/systemd/system/tinycheck-backend.service
    rm /lib/systemd/system/tinycheck-kiosk.service
    rm /lib/systemd/system/tinycheck-watchers.service
}

updating_config_files(){
    echo "[+] Updating dnsmasq and dhcpcd configuration files"
    sed -i '/## TinyCheck configuration ##/,$d' /etc/dnsmasq.conf
    sed -i '/## TinyCheck configuration ##/,$d' /etc/dhcpcd.conf
}

deleting_icon(){
    echo "[+] Deleting desktop icon"
    rm "/home/${SUDO_USER}/Desktop/tinycheck.desktop"
}

delete_packages(){
    pkgs=("hostapd"
          "zeek"
          "tshark"
          "dnsutils"
          "suricata"
          "unclutter"
          "sqlite3"
          "nodejs")
    
    echo -n "[?] Do you want to remove the installed packages? [Y/n] "
    read answer
    if [[ "$answer" =~ ^([yY][eE][sS]|[yY])$ ]]
    then
        for pkg in "${pkgs[@]}"
        do 
            apt -y remove $pkg && apt -y purge $pkg
        done
    fi
    apt autoremove &> /dev/null 
}

update_hostname(){
   echo -n "[?] Please provide a new hostname: "
   read hostname
   echo "$hostname" > /etc/hostname
   sed -i "s/tinycheck/$hostname/g" /etc/hosts
}

reboot_box() {
    echo -e "\e[92m[+] TinyCheck uninstalled, let's reboot.\e[39m"
    sleep 5
    reboot
}

# Checking rights.
if [[ $EUID -ne 0 ]]; then
    echo "The update must be run as root. Type in 'sudo bash $0' to run it as root."
	exit 1
else
    delete_folder
    delete_services
    updating_config_files
    deleting_icon
    update_hostname
    delete_packages
    reboot_box
fi