#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Julien Mousqueton"
__copyright__ = "Copyright 2023, Julien Mousqueton"
__version__ = "0.2"

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
    

def find_texte_location(log_file_path):
    # Define a regular expression pattern to match "Location: [some texte]"
    pattern = r'Location:\s*\[(.*?)\]'
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

def get_object_from_location(location):
    components = location.split('\\')
    return components

def get_element_from_fqdn(fqdn):
    result = fqdn.split('.')
    return result   

def is_fqdn(string):
    # Regular expression patterns to match FQDN 
    fqdn_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(fqdn_pattern, string):
        return True
    else:
        return False
def is_IP(string):
    # Regular expression patterns to match  IP addresses
    ip_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'

    if re.match(ip_pattern, string):
        return True
    else:
        return False


def process_IP(input_file, output_file):
    # Define a regular expression pattern to match IP addresses
    ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b(?!])"

    # Read the file
    with open(input_file, 'r') as file:
        content = file.read()

    # Find all IP addresses in the content using regex
    ip_addresses = re.findall(ip_pattern, content)

    # Replace the first two numbers with "*"
    for ip in ip_addresses:
        #masked_ip = re.sub(r'(\d{1,3}\.\d{1,3})', r'**.**', ip)
        ip_address = ip.split(".")
        ip_address[0] = "**"
        ip_address[1] = "**"
        masked_ip = ".".join(ip_address)
        content = content.replace(ip, masked_ip)

    # Write the modified content back to the file
    with open(output_file, 'w') as file:
        file.write(content)
    
def find_SMTP_server(log_file_path):
    pattern = r"'SMTP Server '(.*?)'"
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


def find_username(log_file_path):
    pattern = r"UserName: '([^']+)'"
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
    

def find_email(log_file_path):
    pattern = r'(?<=Sending report to\s)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
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



def main():
    parser = argparse.ArgumentParser(description="Replace server names in log files within a directory or an individual log file with random strings.")
    parser.add_argument("-i", "--input", dest="input_file", help="Input log file")
    parser.add_argument("-d", "--directory", dest="input_directory", help="Input directory containing log files")
    parser.add_argument("-o", "--output", dest="output_directory", required=True, help="Output directory for processed log files")
    parser.add_argument("--force", action="store_true", help="Force overwrite if output files exist or force the creation of output directory")

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
    VeeamServer = False
    Location = False
    UserName = False
    Email = False
    SMTP = False 

    stdlog('Collecting information')
    for input_file in input_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_directory, filename)
        if os.path.exists(output_file) and not args.force:
            errlog(f'Error: Output file {output_file} already exists. Use --force to overwrite.')
            sys.exit(1)
        if not SMTP:
            SMTP = str(find_SMTP_server(input_file)[0])
            RandomSMTP = str(generate_random_string())
            stdlog('* SMTP Server : ' + SMTP + ' -> ' + RandomSMTP)
        if not VeeamServer: 
            VeeamServer = str(searchVBRName(input_file)[0])
            RandomVeeamServer = str(generate_random_string())
            stdlog('* Veeam Server : ' + VeeamServer + ' -> ' + RandomVeeamServer)
        if not UserName:
            UserName = str(find_username(input_file)[0])
            if '@' in UserName:
                RandomUserName = str(generate_random_string())+'@'+ str(generate_random_string())
            else:
                RandomUserName = str(generate_random_string())
            stdlog('* UserName : ' + UserName + ' -> ' + RandomUserName)
        if not Location:
            Location = str(find_texte_location(input_file)[0])
            RandomvCenter = str(generate_random_string())
            vCenter = str(get_object_from_location(Location)[0])
            if is_fqdn(vCenter):
                RandomDomain = str(generate_random_string())
                Domain = '.'.join(get_element_from_fqdn(vCenter)[1:])
                stdlog('* Domain : ' + Domain + ' -> ' +  RandomDomain)
                vCenter = get_element_from_fqdn(vCenter)[0]
            stdlog('* vCenter : '+ vCenter + ' -> ' +  RandomvCenter)
            Datacenter = str(get_object_from_location(Location)[1])
            RandomDatacenter= str(generate_random_string())
            stdlog('* Datacenter : ' + Datacenter + ' -> ' + RandomDatacenter)
            if len(Location) > 3:
                Cluster = str(get_object_from_location(Location)[2])
                RandomCluster = str(generate_random_string())
                stdlog('* Cluster : ' + Cluster + ' -> ' + RandomCluster)
        if not Email: 
            Email = str(find_email(input_file)[0])
            RandomEmail= str(generate_random_string()) + '@' + str(generate_random_string())
            stdlog('* Email : ' + Email + ' -> ' + RandomEmail)

    stdlog('Processing anonymizing ... ')
    for input_file in input_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_directory, filename)

        if not os.path.exists(output_directory) and args.force:
            os.makedirs(output_directory)
    
        stdlog('- Processing file  '+ input_file)
        # For UserName 
        replace_string_in_file(input_file,output_file, UserName, RandomUserName)
        # For Email 
        replace_string_in_file(output_file, output_file, Email, RandomEmail)
        # For Domain 
        if Domain: 
            replace_string_in_file(output_file, output_file, Domain, RandomDomain)
        # Remplace Veeam Server 
        replace_string_in_file(output_file, output_file, VeeamServer, RandomVeeamServer)
        # For SMTP
        replace_string_in_file(output_file, output_file, SMTP, RandomSMTP)
        # For vCenter 
        replace_string_in_file(output_file, output_file, vCenter, RandomvCenter)
        # For Datacenter 
        replace_string_in_file(output_file, output_file, Datacenter, RandomDatacenter)
        if RandomCluster: 
            # For Cluster 
            replace_string_in_file(output_file, output_file, Cluster, RandomCluster)
        # For IPs
        process_IP(output_file,output_file)
        stdlog('File ' + input_file + ' processed')
    stdlog('Anonymizng finised ')
        


if __name__ == "__main__":
    print(
    f'''
.-.   .-.,---.  ,---.    .--.                   ,-.    .---.    ,--,              .--.  .-. .-. .---.  .-. .-..-.   .-.        ,-. _____  ,---.  ,---.    
 \ \ / / | .-'  | .-'   / /\ \ |\    /|         | |   / .-. ) .' .'              / /\ \ |  \| |/ .-. ) |  \| | \ \_/ )/|\    /||(|/___  / | .-'  | .-.\   
  \ V /  | `-.  | `-.  / /__\ \|(\  / |         | |   | | |(_)|  |  __          / /__\ \|   | || | |(_)|   | |  \   (_)|(\  / |(_)   / /) | `-.  | `-'/   
   ) /   | .-'  | .-'  |  __  |(_)\/  |         | |   | | | | \  \ ( _)         |  __  || |\  || | | | | |\  |   ) (   (_)\/  || |  / /(_)| .-'  |   (    
  (_)    |  `--.|  `--.| |  |)|| \  / |         | `--.\ `-' /  \  `-) )         | |  |)|| | |)|\ `-' / | | |)|   | |   | \  / || | / /___ |  `--.| |\ \   
         /( __.'/( __.'|_|  (_)| |\/| |         |( __.')---'   )\____/          |_|  (_)/(  (_) )---'  /(  (_)  /(_|   | |\/| |`-'(_____/ /( __.'|_| \)\  
        (__)   (__)            '-'  '-'         (_)   (_)     (__)                     (__)    (_)    (__)     (__)    '-'  '-'          (__) v {__version__}  (__) 
    by Julien Mousqueton (@JMousqueton)
    '''
    )
    main()
