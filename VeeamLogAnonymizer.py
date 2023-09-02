#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Julien Mousqueton"
__copyright__ = "Copyright 2023, Julien Mousqueton"
__version__ = "0.5"

# Import necessary modules
import re
import random
import string
import sys
import os
import argparse
import logging
import json
import shutil

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

def anonymized_IPv4(ip):
    ip_address = ip.split(".")
    ip_address[0] = "**"
    ip_address[1] = "**"
    masked_ip = ".".join(ip_address)
    return masked_ip


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
        #ip_address = ip.split(".")
        #ip_address[0] = "**"
        #ip_address[1] = "**"
        #masked_ip = ".".join(ip_address)
        content = content.replace(ip, anonymized_IPv4(ip))

    # Write the modified content back to the file
    with open(output_file, 'w') as file:
        file.write(content)
    

def find_pattern(pattern_key,log_file_path,):
    try:
        with open("patterns.json", "r") as patterns_file:
            patterns_dict = json.load(patterns_file)
        
        pattern = patterns_dict.get(pattern_key)
        if not pattern:
            return f"Pattern key '{pattern_key}' not found in patterns.json."

        with open(log_file_path, "r") as log_file:
            log_content = log_file.read()

        matches = re.findall(pattern, log_content)
        matches = list(set(matches))

        if matches:
            return matches
        else:
            return None
    except FileNotFoundError:
        return f"Error: File '{log_file_path}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Anonymize your Veeam Backup & Replication logs.")
    parser.add_argument("-i", "--input", dest="input_file", help="Input log file")
    parser.add_argument("-d", "--directory", dest="input_directory", help="Input directory containing log files")
    parser.add_argument("-o", "--output", dest="output_directory", required=True, help="Output directory for processed log files")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite if output files exist or force the creation of output directory if not exists")
    parser.add_argument("-u","--users", action="store_true", help="Display the user mapping table")

    if not os.path.exists('patterns.json'):
        errlog("Error: patterns.json not found.")
        sys.exit(1)

    args = parser.parse_args()

    if args.input_file:
        input_files = [args.input_file]
    elif args.input_directory:
        input_directory = args.input_directory
        if not os.path.isdir(input_directory):
            errlog('Error : '+ input_directory +' is not a directory')
            sys.exit(1)
        if not os.path.exists(input_directory):
            errlog('Error: Input directory ' + input_directory + ' does not exist.')
            sys.exit(1)
        input_files = [os.path.join(input_directory, filename) for filename in os.listdir(input_directory) if filename.endswith(".log")]
    else:
        errlog('Error: You must specify either -i or -d.')
        sys.exit(1)
        
    output_directory = args.output_directory
    VeeamServer = False
    VeeamUserList = []
    tmpUser_set = set()
    Location = False
    vCenterUser = False
    Email = False
    SMTPServer = False 
    Domain = False
    vCenter= False
    Datacenter = False
    Cluster = False

    stdlog('Collecting information')
    for input_file in input_files:
        filename = os.path.basename(input_file)
        dbglog('*** ' +  filename)
        output_file = os.path.join(output_directory, filename)
        if os.path.exists(output_file) and not args.force:
            errlog(f'Error: Output file {output_file} already exists. Use -f or --force to overwrite.')
            sys.exit(1)
    
        if not SMTPServer:
            try:
                SMTPServer = str(find_pattern('SMTPServer',input_file)[0])
                if is_fqdn(SMTPServer):
                    RandomSMTP = str(generate_random_string())
                else:
                    RandomSMTP = anonymized_IPv4(SMTPServer)
            except:
                pass
        if not VeeamServer: 
            VeeamServer = str(find_pattern('VeeamServer',input_file)[0])
            RandomVeeamServer = str(generate_random_string())
        VeeamUsers = find_pattern('VeeamUser',input_file)
        try: 
            for VeeamUser in VeeamUsers:
                tmpUser = VeeamUser.split("\\")[1]
                tmpRandom = str(generate_random_string())
                if tmpUser in tmpUser_set:
                    continue
                tmpUser_set.add(tmpUser)  # Add the unique tmpUser value to the set
                element = (tmpUser, tmpRandom)
                VeeamUserList.append(element)
        except:
            pass
        if not vCenterUser:
            try:
                vCenterUser = str(find_pattern('vCenterUser',input_file)[0])
                if '@' in vCenterUser:
                    RandomvCenterUser = str(generate_random_string())+'@'+ str(generate_random_string())
                else:
                    RandomvCenterUser = str(generate_random_string())
            except:
                pass
        if not Location:
            try:
                Location = str(find_pattern('vCenter',input_file)[0])
                RandomvCenter = str(generate_random_string())
                vCenter = str(get_object_from_location(Location)[0])
                if is_fqdn(vCenter):
                    RandomDomain = str(generate_random_string())
                    Domain = '.'.join(get_element_from_fqdn(vCenter)[1:])
                    vCenter = get_element_from_fqdn(vCenter)[0]
                Datacenter = str(get_object_from_location(Location)[1])
                RandomDatacenter= str(generate_random_string())
                if len(Location) > 3:
                    Cluster = str(get_object_from_location(Location)[2])
                    RandomCluster = str(generate_random_string())
            except:
                pass
        if not Email:
            try:
                Email = str(find_pattern('Email',input_file)[0])
                RandomEmail= str(generate_random_string()) + '@' + str(generate_random_string())
            except:
                pass
    

    # Clean list 
    UniqueVeeamUsers =list(set(VeeamUserList))


    # Show the mapping 
    ## VEEAM
    try:
        stdlog('* Veeam Server : ' + VeeamServer + ' -> ' + RandomVeeamServer)
    except: 
        pass
    try:
        stdlog('* Domain : ' + Domain + ' -> ' +  RandomDomain)
    except: 
        pass
    try:
        stdlog('* SMTP Server : ' + SMTPServer + ' -> ' + RandomSMTP)
    except: 
        pass
    try:
        stdlog('* Email : ' + Email + ' -> ' + RandomEmail)
    except: 
        pass
    try:
        ## VMWARE
        stdlog('* vCenter : '+ vCenter + ' -> ' +  RandomvCenter) 
    except: 
        pass
    try:   
        stdlog('* vCenter User : ' + vCenterUser + ' -> ' + RandomvCenterUser)
    except: 
        pass
    try:
        stdlog('* Datacenter : ' + Datacenter + ' -> ' + RandomDatacenter)
    except: 
        pass
    try:
        stdlog('* Cluster : ' + Cluster + ' -> ' + RandomCluster)
    except: 
        pass


    if args.users:
        stdlog("**** ")
        stdlog("User Mapping Table :")
        try:
            for VeeamUser in UniqueVeeamUsers:
                _OriginalUser, _RandomUser = VeeamUser
                stdlog( _OriginalUser + ' -> ' + _RandomUser)
        except: 
            pass
        stdlog('****')
    

    stdlog('Processing anonymizing ... ')
    for input_file in input_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_directory, filename)

        if not os.path.exists(output_directory) and args.force:
            os.makedirs(output_directory)  
        file_size_bytes = os.path.getsize(input_file)
        file_size_megabytes = round(file_size_bytes / (1024 * 1024),2)
        stdlog('- Processing file  '+ filename + '(' + str(file_size_megabytes)+ ' Mb)')
        try:
            shutil.copy(input_file, output_file)
        except:
            errlog('Fatal Error processing ...')
            sys.exit(1)
        if vCenterUser:
            replace_string_in_file(output_file,output_file, vCenterUser, RandomvCenterUser)
            dbglog('    + anonymizing username')
        if Email: 
            replace_string_in_file(output_file, output_file, Email, RandomEmail)
            dbglog('    + anonymizing email address')
        if Domain: 
            replace_string_in_file(output_file, output_file, Domain, RandomDomain)
            dbglog('    + anonymizing domain name')
        if VeeamServer: 
            replace_string_in_file(output_file, output_file, VeeamServer, RandomVeeamServer)
            dbglog('    + anonymizing VeeamServer')
        if len(UniqueVeeamUsers) > 0: 
            for VeeamUser in UniqueVeeamUsers:
                _OriginalUser, _RandomUser = VeeamUser
                replace_string_in_file(output_file, output_file, _OriginalUser, _RandomUser)
                dbglog('    + anonymizing Veeam Users')
        if SMTPServer:
            replace_string_in_file(output_file, output_file, SMTPServer, RandomSMTP)
            dbglog('    + anonymizing SMTP Server')
        if vCenter: 
            replace_string_in_file(output_file, output_file, vCenter, RandomvCenter)
            dbglog('    + anonymizing vCenter Server')
        if Datacenter: 
            replace_string_in_file(output_file, output_file, Datacenter, RandomDatacenter)
            dbglog('    + anonymizing vCenter Datacenter')
        if Cluster: 
            # For Cluster 
            replace_string_in_file(output_file, output_file, Cluster, RandomCluster)
            dbglog('    + anonymizing vCenter Clusster')
        # For IPs
        dbglog('    + anonymizing IP Address')
        process_IP(output_file,output_file)
        dbglog('- File ' + input_file + ' processed')
    stdlog('Anonymizng finished ')



if __name__ == "__main__":
    print(
    f'''
.-.   .-.,---.  ,---.    .--.                   ,-.    .---.    ,--,              .--.  .-. .-. .---.  .-. .-..-.   .-.        ,-. _____  ,---.  ,---.    
 \ \ / / | .-'  | .-'   / /\ \ |\    /|         | |   / .-. ) .' .'              / /\ \ |  \| |/ .-. ) |  \| | \ \_/ )/|\    /||(|/___  / | .-'  | .-.\   
  \ V /  | `-.  | `-.  / /__\ \|(\  / |         | |   | | |(_)|  |  __          / /__\ \|   | || | |(_)|   | |  \   (_)|(\  / |(_)   / /) | `-.  | `-'/   
   ) /   | .-'  | .-'  |  __  |(_)\/  |         | |   | | | | \  \ ( _)         |  __  || |\  || | | | | |\  |   ) (   (_)\/  || |  / /(_)| .-'  |   (    
   (_)   |  `--.|  `--.| |  |)|| \  / |         | `--.\ `-' /  \  `-) )         | |  |)|| | |)|\ `-' / | | |)|   | |   | \  / || | / /___ |  `--.| |\ \   
         /( __.'/( __.'|_|  (_)| |\/| |         |( __.')---'   )\____/          |_|  (_)/(  (_) )---'  /(  (_)  /(_|   | |\/| |`-'(_____/ /( __.'|_| \)\  
        (__)   (__)            '-'  '-'         (_)   (_)     (__)                     (__)    (_)    (__)     (__)    '-'  '-'          (__) v {__version__}  (__) 
    by Julien Mousqueton (@JMousqueton)
    '''
    )
    main()
