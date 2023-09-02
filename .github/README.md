![](/.github/logo.png)

# Veeam Log Anonymizer 
## __A tool to anonimyze your Veeam logs__

VeeamLogAnonymizeris python scrypt to anonimyze your log 

This script is still as an early stage of development. DO NOT USE.

## Features

Veeam Log Anonymizer, anonymizes : 

- Veeam Server name 
- Usernames 
- IPs address 
- SMTP Server     
- vCenter Username 
- Domain
- vCenter Server
- vCenter Datacenter
- vCenter Cluster
- Email

## Installation

**UNDER CONSTRUCTION**

## Usage 

```bash
python3 VeeamLogAnonymizer.py --help

.-.   .-.,---.  ,---.    .--.                   ,-.    .---.    ,--,              .--.  .-. .-. .---.  .-. .-..-.   .-.        ,-. _____  ,---.  ,---.    
 \ \ / / | .-'  | .-'   / /\ \ |\    /|         | |   / .-. ) .' .'              / /\ \ |  \| |/ .-. ) |  \| | \ \_/ )/|\    /||(|/___  / | .-'  | .-.\   
  \ V /  | `-.  | `-.  / /__\ \|(\  / |         | |   | | |(_)|  |  __          / /__\ \|   | || | |(_)|   | |  \   (_)|(\  / |(_)   / /) | `-.  | `-'/   
   ) /   | .-'  | .-'  |  __  |(_)\/  |         | |   | | | | \  \ ( _)         |  __  || |\  || | | | | |\  |   ) (   (_)\/  || |  / /(_)| .-'  |   (    
  (_)    |  `--.|  `--.| |  |)|| \  / |         | `--.\ `-' /  \  `-) )         | |  |)|| | |)|\ `-' / | | |)|   | |   | \  / || | / /___ |  `--.| |\ \   
         /( __.'/( __.'|_|  (_)| |\/| |         |( __.')---'   )\____/          |_|  (_)/(  (_) )---'  /(  (_)  /(_|   | |\/| |`-'(_____/ /( __.'|_| \)\  
        (__)   (__)            '-'  '-'         (_)   (_)     (__)                     (__)    (_)    (__)     (__)    '-'  '-'          (__) v 0.3  (__) 
    by Julien Mousqueton (@JMousqueton)
    
usage: VeeamLogAnonymizer.py [-h] [-i INPUT_FILE] [-d INPUT_DIRECTORY] -o OUTPUT_DIRECTORY [--force]

Replace server names in log files within a directory or an individual log file with random strings.

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input INPUT_FILE
                        Input log file
  -d INPUT_DIRECTORY, --directory INPUT_DIRECTORY
                        Input directory containing log files
  -o OUTPUT_DIRECTORY, --output OUTPUT_DIRECTORY
                        Output directory for processed log files
  --force               Force overwrite if output files exist or force the creation of output directory
  ```

## Development
Want to contribute? Great!

## License
GNU GENERAL PUBLIC LICENSE version 3 
