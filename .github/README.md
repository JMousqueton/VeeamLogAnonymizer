![](/.github/logo.png)

# Veeam Log Anonymizer 
[![Twitter: JMousqueton](https://img.shields.io/twitter/follow/JMousqueton.svg?style=social)](https://twitter.com/JMousqueton)

> __A tool to anonimyze your Veeam logs__


VeeamLogAnonymizeris python scrypt to anonimyze your [Veeam](https://www.veeam.com) Backup & Replication v12 log.

⚠️ UNDER CONSTRUCTION ⚠️

This script is still as an early stage of development. ⛔️ DO NOT USE.

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

coming soon

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

## Author

👤 **Julien Mousqueton**

* Website: <https://www.julien.io>
* Twitter: [@JMousqueton](https://twitter.com/JMousqueton)
* Github: [@JMousqueton](https://github.com/JMousqueton)
* LinkedIn: [Julien Mousqueton](https://linkedin.com/in/julienmousqueton)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/JMousqueton/Badware/issues).

## Acknowledgements

* Bertrand 
* Eric 
  
## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

This project is under [GNU GENERAL PUBLIC LICENSE version 3](https://github.com/JMousqueton/VeeamLogAnonymizer/blob/main/LICENSE).
