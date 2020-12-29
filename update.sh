# Checking rights.
if [[ $EUID -ne 0 ]]; then
    echo "The update must be run as root. Type in 'sudo bash $0' to run it as root."
	exit 1
fi

if [ $PWD = "/usr/share/tinycheck" ]; then
    echo "[+] Cloning the current repository to /tmp/"
    rm -rf /tmp/tinycheck/ &> /dev/null 
    cd /tmp/ && git clone https://github.com/KasperskyLab/tinycheck
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

    echo "[+] Copying the new TinyCheck version"
    cp -R app/ /usr/share/tinycheck/app/
    cp -R server/ /usr/share/tinycheck/server/
    cp -R analysis/ /usr/share/tinycheck/analysis/
    cp update.sh /usr/share/tinycheck/update.sh
    cp kiosk.sh /usr/share/tinycheck/kiosk.sh

    echo "[+] Retoring the backend's SSL configuration from /tmp/"
    mv /tmp/*.pem /usr/share/tinycheck/server/backend/

    echo "[+] Checking possible new Python dependencies"
    python3 -m pip install -r assets/requirements.txt

    echo "[+] Building new interfaces..."
    cd /usr/share/tinycheck/app/frontend/ && npm install && npm run build
    cd /usr/share/tinycheck/app/backend/ && npm install && npm run build

    echo "[+] Restarting services"
    service tinycheck-backend restart
    service tinycheck-frontend restart
    service tinycheck-watchers restart

    echo "[+] TinyCheck updated!"
fi