# BRAWLER
![BrawlerLogo](https://raw.githubusercontent.com/tamrinotte/brawler/main/app_images/Brawler.png)

A command line tool to brute force common web servers.

<br>

## INSTALLATION

1) Install dependencies

       sudo apt install tor -y

2) Download the installer

       curl -L https://github.com/tamrinotte/brawler/releases/download/hacking/brawler.deb -o brawler.deb

3) Start the installer

       sudo dpkg -i brawler.deb

4) Start cracking

       sudo brawler -u bandit0 -t bandit.labs.overthewire.org -p 2220 ssh /home/username/wordlist.txt /home/username/ssh_cracking_result.txt

<br>

## OPTIONS 

__-h, --help:__ Show the help message and exit

__-v, --version:__ Display app's version

__-u, --username:__ Enter username

__-t, --target:__  Enter target specification

__-p, --port:__ Enter port number

<br>

---

<br>

# BRAWLER
![BrawlerLogo](https://raw.githubusercontent.com/tamrinotte/brawler/main/app_images/Brawler.png)

Brawler yaygın web sunucularının şifrelerini kırmaya yarayan bir komut satırı uygulamasıdır

<br>

## YÜKLEME

1) Bağımlılıkları yükleyin

       sudo apt install tor -y

2) Yükleyiciyi indir

       curl -L https://github.com/tamrinotte/brawler/releases/download/hacking/brawler.deb -o brawler.deb

3) Yükleyiciyi başlat

       sudo dpkg -i brawler.deb

4) Şifre kırmaya başla

       sudo brawler -u bandit0 -t bandit.labs.overthewire.org -p 2220 ssh /home/username/wordlist.txt /home/username/ssh_cracking_result.txt

<br>

## ARGÜMANLAR 

__-h, --help:__ Yardım mesajını görüntüle

__-v, --version:__ Versiyonu görüntüle

__-u, --username:__ Kullanıcı adını gir

__-t, --target:__  Hedef ifadesini gir

__-p, --port:__ Port numarasını gir