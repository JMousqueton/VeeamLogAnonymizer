![](/.github/logo.png)

# Veeam Log Anonymizer 
[![Twitter: JMousqueton](https://img.shields.io/twitter/follow/JMousqueton.svg?style=social)](https://twitter.com/JMousqueton)

> __A tool to anonimyze your Veeam logs__


VeeamLogAnonymizeris is a python script which anonimyzes your [Veeam](https://www.veeam.com) Backup & Replication v12 log.
Usefull when you need some confidentiality before sending log to support. 

## ⚠️ Disclamer 

This script is still as an early stage of development. 

⚠️ UNDER CONSTRUCTION ⚠️

## ⚙️ Features

Veeam Log Anonymizer, anonymizes : 

- Veeam Server name 
- Usernames 
- IPs address 
- SMTP Server     
- vCenter Username 
- Domain
- vCenter Server
- Email
- vCenter Location

## 💿 Installation

coming soon

## 🚀 Usage 

You need to files : 
* patterns.json 
* VeeamLogAnonymizer.py 
  

```bash
python3 VeeamLogAnonymizer.py -h

.-.   .-.,---.  ,---.    .--.                   ,-.    .---.    ,--,              .--.  .-. .-. .---.  .-. .-..-.   .-.        ,-. _____  ,---.  ,---.    
\ \ / / | .-'  | .-'   / /\ \ |\    /|         | |   / .-. ) .' .'              / /\ \ |  \| |/ .-. ) |  \| | \ \_/ )/|\    /||(|/___  / | .-'  | .-.\   
 \ V /  | `-.  | `-.  / /__\ \|(\  / |         | |   | | |(_)|  |  __          / /__\ \|   | || | |(_)|   | |  \   (_)|(\  / |(_)   / /) | `-.  | `-'/   
  ) /   | .-'  | .-'  |  __  |(_)\/  |         | |   | | | | \  \ ( _)         |  __  || |\  || | | | | |\  |   ) (   (_)\/  || |  / /(_)| .-'  |   (    
  (_)   |  `--.|  `--.| |  |)|| \  / |         | `--.\ `-' /  \  `-) )         | |  |)|| | |)|\ `-' / | | |)|   | |   | \  / || | / /___ |  `--.| |\ \   
        /( __.'/( __.'|_|  (_)| |\/| |         |( __.')---'   )\____/          |_|  (_)/(  (_) )---'  /(  (_)  /(_|   | |\/| |`-'(_____/ /( __.'|_| \)\  
       (__)   (__)            '-'  '-'         (_)   (_)     (__)                     (__)    (_)    (__)     (__)    '-'  '-'          (__) v 1.0  (__) 
   by Julien Mousqueton (@JMousqueton)
    
usage: VeeamLogAnonymizer.py [-h] [-i INPUT_FILE] [-d INPUT_DIRECTORY] -o OUTPUT_DIRECTORY [-f] [-m] [-v] [-D]

Anonymize your Veeam Backup & Replication logs.

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input INPUT_FILE
                        Input log file
  -d INPUT_DIRECTORY, --directory INPUT_DIRECTORY
                        Input directory containing log files
  -o OUTPUT_DIRECTORY, --output OUTPUT_DIRECTORY
                        Output directory for processed log files
  -f, --force           Force overwrite if output files exist or force the creation of output directory if not exists
  -m, --mapping         Display the mapping table of anonymized data
  -v, --verbose         Display processing files and other information
  -D, --dictionary      output a JSON file with the dictionary of anonymized data
  ```

### Examples 

`python3 VeeamLogAnonymizer.py -d ./log -o ./anonymized -f`
`pyhton3 VeeamLogAnonymizer.py -i ./log/VeeamBackupManager.log -o ./anonymized`
and full options :) 
`python3 VeeamLogAnonymizer.py  -d ./log -o ./anonymized -f -m -v  -D     `

## Author

👤 **Julien Mousqueton**

* Website: <https://www.julien.io>
* Twitter: [@JMousqueton](https://twitter.com/JMousqueton)
* Github: [@JMousqueton](https://github.com/JMousqueton)
* LinkedIn: [Julien Mousqueton](https://linkedin.com/in/julienmousqueton)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/JMousqueton/Badware/issues).

## 🙏🏻 Acknowledgements

For the idea and there support and improvements 

* Bertrand (Veeam Legend)
* Eric (Veeam Vanguard)
  
## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

This project is under [GNU GENERAL PUBLIC LICENSE version 3](https://github.com/JMousqueton/VeeamLogAnonymizer/blob/main/LICENSE).
