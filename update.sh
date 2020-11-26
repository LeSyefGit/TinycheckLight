# Checking rights.
if [[ $EUID -ne 0 ]]; then
    echo "The update must be run as root. Type in 'sudo bash $0' to run it as root."
	exit 1
fi

# Clone the current repo. 
echo "[+] Cloning the current repository to /tmp/"
cd /tmp/ && git clone https://github.com/KasperskyLab/TinyCheck

# Deleteing the current folders.
echo "[+] Deleting the current TinyCheck folders"
rm -rf /usr/share/TinyCheck/app/
rm -rf /usr/share/TinyCheck/server/
rm -rf /usr/share/TinyCheck/analysis/

# Copying the folders.
echo "[+] Copying the new version"
cd /tmp/TinyCheck && cp -R app/ /usr/share/tinycheck/app/
cd /tmp/TinyCheck && cp -R server/ /usr/share/tinycheck/server/
cd /tmp/TinyCheck && cp -R analysis/ /usr/share/tinycheck/analysis/

# Installing possible new dependencies.
echo "[+] Checking new Python dependencies"
cd /tmp/TinyCheck && python3 -m pip install -r assets/requirements.txt

# Back to the VueJS projects and reinstalling all the stuff
echo "[+] Building new interfaces..."
cd /usr/share/TinyCheck/app/frontend/ && npm install && npm run build
cd /usr/share/TinyCheck/app/backend/ && npm install && npm run build
echo "[+] TinyCheck updated!"