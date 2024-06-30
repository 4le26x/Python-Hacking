#!/usr/bin/env python3

import argparse
import signal
import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

# Program: Fast TCP Port Scanner
# Author: Alejandro Perez Hernandez
# Description: This program performs a fast TCP port scan on a specified target using multithreading to improve efficiency.
# The program handles clean exits and ensures all resources are freed properly. It uses the socket library to attempt
# connections on each port and determines if the port is open. This script is especially useful in network security assessments.


# Maintain a list of all open sockets to close them properly on program exit.
open_sockets = []

# Handle signal interruption to ensure all resources are properly freed on exit.
def def_handler(sig, frame):
    print(colored("\n[!] Exiting...", 'red'))
    for s in open_sockets:
        s.close()
    sys.exit(1)

# Register the custom signal handler to respond to interrupt signals.
signal.signal(signal.SIGINT, def_handler)

# Set up and parse command line arguments.
def get_arguments():
    parser = argparse.ArgumentParser(description="Fast TCP Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Specify the target IP or range to scan (e.g., 192.168.1.1)")
    parser.add_argument("-p", "--port", required=True, help="Define the port range to scan (e.g., 1-100)")
    return parser.parse_args()

# Create a socket with a specified timeout.
def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    open_sockets.append(s)
    return s

# Attempt to connect to a specified port on a host to determine if it's open.
def port_scanner(port, host):
    with create_socket() as s:
        try:
            s.connect((host, port))
            print(colored(f"\n[+] The port {port} is open", 'green'))
        except (socket.timeout, ConnectionError):
            # Handle connection errors quietly.
            pass

# Scan multiple ports on a target host concurrently to optimize the scanning speed.
def scan_ports(ports, target):
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda port: port_scanner(port, target), ports)

# Parse a string representing a range of ports into a list of integers.
def parse_ports(ports_str):
    if '-' in ports_str:
        start, end = map(int, ports_str.split('-'))
        return range(start, end + 1)
    elif ',' in ports_str:
        return map(int, ports_str.split(','))
    else:
        return [int(ports_str)]

# Initialize the port scanning process based on user input.
def main():
    args = get_arguments()
    target, ports = args.target, parse_ports(args.port)
    scan_ports(ports, target)

if __name__ == "__main__":
    main()

