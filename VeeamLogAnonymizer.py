#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Julien Mousqueton"
__copyright__ = "Copyright 2023, Julien Mousqueton"
__version__ = "0.1"

# Import necessary modules
import re
import random
import string
import sys
import os
import argparse
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO
)

# Define custom logging functions
def stdlog(msg):
    '''Standard info logging'''
    logging.info(msg)

def dbglog(msg):
    '''Debug logging'''
    logging.debug(msg)

def errlog(msg):
    '''Error logging'''
    logging.error(msg)

def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def searchVBRName(log_file_path):
    pattern = r"HostName:\s*\[([^\]]+)\]"
    try:
        with open(log_file_path, "r") as log_file:
            log_content = log_file.read()

        matches = re.findall(pattern, log_content)

        if matches:
            return matches
        else:
            return None
    except FileNotFoundError:
        return f"Error: File '{log_file_path}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def replace_string_in_file(input, output, old_value, new_value):
    with open(input, 'r') as file:
        content = file.read()
    pattern = re.compile(re.escape(old_value), re.IGNORECASE)
    content = pattern.sub(lambda match: new_value if match.group(0).islower() else new_value.upper(), content)
    with open(output, 'w') as file:
        file.write(content)

def check_log_contains_line(input_file, line_to_check):
    with open(input_file, 'r') as file:
        for line in file:
            if line_to_check in line:
                return True
    return False

def process_IP(input_file, output_file):
    # Define a regular expression pattern to match IP addresses
    ip_pattern = r'\b(\d{1,3}\.\d{1,3})\.\d{1,3}\.\d{1,3}\b;'

    # Read the file
    with open(input_file, 'r') as file:
        content = file.read()

    # Find all IP addresses in the content using regex
    ip_addresses = re.findall(ip_pattern, content)

    # Replace the first two numbers with "*"
    for ip in ip_addresses:
        masked_ip = re.sub(r'(\d{1,3}\.\d{1,3})', r'**.**', ip)
        content = content.replace(ip, masked_ip)

    # Write the modified content back to the file
    with open(output_file, 'w') as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser(description="Replace server names in log files within a directory or an individual log file with random strings.")
    parser.add_argument("-i", "--input", dest="input_file", help="Input log file")
    parser.add_argument("-d", "--directory", dest="input_directory", help="Input directory containing log files")
    parser.add_argument("-o", "--output", dest="output_directory", required=True, help="Output directory for processed log files")
    parser.add_argument("--force", action="store_true", help="Force overwrite if output files exist")

    args = parser.parse_args()

    if args.input_file:
        input_files = [args.input_file]
    elif args.input_directory:
        input_directory = args.input_directory
        if not os.path.exists(input_directory):
            errlog('Error: Input directory ' + input_directory + ' does not exist.')
            sys.exit(1)
        input_files = [os.path.join(input_directory, filename) for filename in os.listdir(input_directory) if filename.endswith(".log")]
    else:
        errlog('Error: You must specify either -i or -d.')
        sys.exit(1)

    output_directory = args.output_directory
    ServerName = False

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for input_file in input_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_directory, filename)
        
        if os.path.exists(output_file) and not args.force:
            errlog(f'Error: Output file {output_file} already exists. Use --force to overwrite.')
            sys.exit(1)

        if check_log_contains_line(input_file, "Starting new log"):
            if not ServerName: 
                ServerName = str(searchVBRName(input_file)[0])
                RandomName = str(generate_random_string())
                stdlog('* ' + ServerName + ' -> ' + RandomName)
            stdlog('processing '+ input_file)   
            replace_string_in_file(input_file, output_file, ServerName, RandomName)
            process_IP(output_file,output_file)
            stdlog(input_file +' processed')
        else:
            errlog("Unknown log format")

        

if __name__ == "__main__":
    print(
    '''
.-.   .-.,---.  ,---.    .--.                   ,-.    .---.    ,--,              .--.  .-. .-. .---.  .-. .-..-.   .-.        ,-. _____  ,---.  ,---.    
 \ \ / / | .-'  | .-'   / /\ \ |\    /|         | |   / .-. ) .' .'              / /\ \ |  \| |/ .-. ) |  \| | \ \_/ )/|\    /||(|/___  / | .-'  | .-.\   
  \ V /  | `-.  | `-.  / /__\ \|(\  / |         | |   | | |(_)|  |  __          / /__\ \|   | || | |(_)|   | |  \   (_)|(\  / |(_)   / /) | `-.  | `-'/   
   ) /   | .-'  | .-'  |  __  |(_)\/  |         | |   | | | | \  \ ( _)         |  __  || |\  || | | | | |\  |   ) (   (_)\/  || |  / /(_)| .-'  |   (    
  (_)    |  `--.|  `--.| |  |)|| \  / |         | `--.\ `-' /  \  `-) )         | |  |)|| | |)|\ `-' / | | |)|   | |   | \  / || | / /___ |  `--.| |\ \   
         /( __.'/( __.'|_|  (_)| |\/| |         |( __.')---'   )\____/          |_|  (_)/(  (_) )---'  /(  (_)  /(_|   | |\/| |`-'(_____/ /( __.'|_| \)\  
        (__)   (__)            '-'  '-'         (_)   (_)     (__)                     (__)    (_)    (__)     (__)    '-'  '-'          (__) v 0.1  (__) 
    by Julien Mousqueton (@JMousqueton)
    '''
    )
    main()
