# Checking rights.
if [[ $EUID -ne 0 ]]; then
    echo "The update must be run as root. Type in 'sudo bash $0' to run it as root."
	exit 1
fi

if [ $PWD = "/usr/share/tinycheck" ]; then
    echo "[+] Cloning the current repository to /tmp/"
    rm -rf /tmp/tinycheck/ &> /dev/null 
    cd /tmp/ && git clone --branch update-feature https://github.com/KasperskyLab/tinycheck
    cd /tmp/tinycheck && bash update.sh
elif [ $PWD = "/tmp/tinycheck" ]; then

    echo "[+] Saving current backend's SSL configuration in /tmp/"
    mv /usr/share/tinycheck/server/backend/*.pem /tmp/

    echo "[+] Deleting the current TinyCheck folders and files."
    rm -rf /usr/share/tinycheck/app/
    rm -rf /usr/share/tinycheck/server/
    rm -rf /usr/share/tinycheck/analysis/
    rm /usr/share/tinycheck/update.sh
    rm /usr/share/tinycheck/kiosk.sh
    rm /usr/share/tinycheck/uninstall.sh

    echo "[+] Copying the new TinyCheck version"
    cp -R app/ /usr/share/tinycheck/app/
    cp -R server/ /usr/share/tinycheck/server/
    cp -R analysis/ /usr/share/tinycheck/analysis/
    cp update.sh /usr/share/tinycheck/update.sh
    cp kiosk.sh /usr/share/tinycheck/kiosk.sh
    cp uninstall.sh /usr/share/tinycheck/uninstall.sh

    echo "[+] Retoring the backend's SSL configuration from /tmp/"
    mv /tmp/*.pem /usr/share/tinycheck/server/backend/

    echo "[+] Checking possible new Python dependencies"
    python3 -m pip install -r assets/requirements.txt

    echo "[+] Building new interfaces..."
    cd /usr/share/tinycheck/app/frontend/ && npm install && npm run build
    cd /usr/share/tinycheck/app/backend/ && npm install && npm run build

    echo "[+] Updating current configuration with new values."
    if ! grep -q reboot_option /usr/share/tinycheck/config.yaml; then
        sed -i 's/frontend:/frontend:\n  reboot_option: true/g' /usr/share/tinycheck/config.yaml
    fi

    if ! grep -q user_lang /usr/share/tinycheck/config.yaml; then
        sed -i 's/frontend:/frontend:\n  user_lang: en/g' /usr/share/tinycheck/config.yaml
    fi

    if ! grep -q shutdown_option /usr/share/tinycheck/config.yaml; then
        sed -i 's/frontend:/frontend:\n  shutdown_option: true/g' /usr/share/tinycheck/config.yaml
    fi

    if ! grep -q quit_option /usr/share/tinycheck/config.yaml; then
        sed -i 's/frontend:/frontend:\n  quit_option: true/g' /usr/share/tinycheck/config.yaml
    fi

    if ! grep -q active /usr/share/tinycheck/config.yaml; then
        sed -i 's/analysis:/analysis:\n  active: true/g' /usr/share/tinycheck/config.yaml
    fi

    if ! grep -q update /usr/share/tinycheck/config.yaml; then
        sed -i 's/frontend:/frontend:\n  update: true/g' /usr/share/tinycheck/config.yaml
    fi

    if ! grep -q "CN=R3,O=Let's Encrypt,C=US" /usr/share/tinycheck/config.yaml; then
        sed -i "s/free_issuers:/free_issuers:\n  - CN=R3,O=Let's Encrypt,C=US/g" /usr/share/tinycheck/config.yaml
    fi

    echo "[+] Restarting services"
    service tinycheck-backend restart
    service tinycheck-frontend restart
    service tinycheck-watchers restart

    echo "[+] Updating the TinyCheck version"
    cd /tmp/tinycheck && git tag | tail -n 1 | xargs echo -n > /usr/share/tinycheck/VERSION

    echo "[+] TinyCheck updated!"
fi