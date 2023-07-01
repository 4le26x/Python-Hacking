#!/usr/bin/env python3
import subprocess
import argparse
import re
import sys


# Program: MAC Address Charger
# Author: Alejandro Perez Hernandez
# Description: The following program will change the MAC address of a network interface using the ifconfig command.
# This program is part of one the projects from the Udemy course called Python & Ethical Hacking From Scratch.
# Some of the improvements that I made are the addition of input validation and make some corrections to be compatible with python 3.

# This function will get the user's arguments
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface', help='Interface to change its MAC address')
    parser.add_argument('-m', '--mac', dest='new_mac_addr', help='New MAC Address')
    return parser.parse_args()


# This function will change the MAC address of the specified interface
def change_mac(interface, new_mac_addr):
    print(f'[+] Changing MAC address for {interface} to {new_mac_addr}')
    subprocess.run(['ifconfig', interface, 'down'], check=True)
    subprocess.run(['ifconfig', interface, 'hw', 'ether', new_mac_addr], check=True)
    subprocess.run(['ifconfig', interface, 'up'], check=True)


# This function will retrieve the current MAC address of the specified interface
def get_current_mac(interface):
    ifconfig_result = subprocess.run(['ifconfig', interface], capture_output=True, text=True, check=True)
    mac_address_search_result = re.search(r"(\w\w:){5}\w\w", ifconfig_result.stdout)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("Failed to read MAC Address.")
        sys.exit(1)


# This will validate the format of the MAC address
def validate_mac_address(mac_address):
    if not re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac_address):
        print("Invalid MAC address format.")
        sys.exit(1)


# This will validate the interface and MAC address arguments
def validate_arguments(options):
    if not options.interface:
        print("Please specify an interface, use --help for more info")
        sys.exit(1)
    if not options.new_mac_addr:
        print("Please specify a MAC Address, use --help for more info")
        sys.exit(1)
    validate_mac_address(options.new_mac_addr)


def main():
    options = get_arguments()
    validate_arguments(options)

    current_mac = get_current_mac(options.interface)
    print(f"Current MAC: {current_mac}")

    change_mac(options.interface, options.new_mac_addr)

    current_mac = get_current_mac(options.interface)

    # This will verify if the MAC address was successfully changed
    if current_mac == options.new_mac_addr:
        print(f"[+] MAC address was successfully changed to {current_mac}")
    else:
        print(f"[-] MAC address did not change: {current_mac}")


if __name__ == '__main__':
    main()
