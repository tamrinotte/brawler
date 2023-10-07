#!/usr/bin/bash

# Purge the app
echo "Purging brawler..."
sudo apt purge --autoremove brawler -y

# Creating a variable called username by getting the active user's username
username=${SUDO_USER:-${USER}}

# Delete the old files if they are exist
echo "Deleting the dist folder..."
if [[ -d dist/ ]]; then
    rm -rf dist/
fi

echo "Deleting the build folder..."
if [[ -d build/ ]]; then
    rm -rf build/
fi 

echo "Deleting the package folder..."
if [[ -d package/ ]]; then
    rm -rf package/
fi

echo "Deleting the installer..."
if [[ -f brawler.deb ]]; then
    rm brawler.deb
fi 

# Create the executable file
echo 'Creating the executable file...'
pyinstaller --onefile brawler.py --name="brawler"

# Create a directory hierarchy to package your application
echo 'Creating the directory hierarchy...'
mkdir -p package/usr/bin

# Copy required files and folders into the package
echo 'Copying the executable file into package/usr/bin'
cp -r dist/brawler package/usr/bin

# Set the permissions and file ownerships
echo 'Setting the file permissions and ownerships'
chmod 755 -R package/
chown $username:$username -R package/

# Create the installer
echo 'Creating the installer...'
fpm -C package -s dir -t deb -n "brawler" -v 0.1.0 -p brawler.deb --after-install post_install_script.sh

# Start the installer
sudo dpkg -i brawler.deb