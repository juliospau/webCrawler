import requests
import re
from colorama import Fore, init
import argparse
import os
from time import perf_counter

init()
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
RESET = Fore.RESET

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", dest="url", help="URL a escanear. webCrawler.py -u https://google.com")
parser.add_argument("-c", "--code", dest="code", help="Códigos a extraer. webCrawler.py -u https://google.com -c 200")
parser.add_argument("-d", "--dic", dest="dicText", help="Códigos a extraer. webCrawler.py -u https://google.com -c 200")
options = parser.parse_args()

codigo = []

b = ""
for i in options.code:
    b += i

c = b.split(",")
for i in c:
    codigo.append(i)

url = options.url
foundDirs = []

#start_time = perf_counter()

if os.path.exists(options.dicText):
    with open(options.dicText, "r") as directories:
        for line in directories.read().splitlines():
            if line[0:0] != "#":
                subDirURL = url + line

                print (f"{YELLOW}-> {subDirURL}{RESET}", end="\r")
                
                getResponse = requests.get(subDirURL)
                filterResponse = re.search("\d\d\d", str(getResponse))
        
                if filterResponse.group(0) in codigo:
                    foundDirs.append(line) 
                else:
                    pass
            else:
                pass

else:
    print ("El diccionario indicado no existe!")

print (f"{CYAN}", "DIRECTORIOS ENCONTRADOS".center(90, "-"), f"{RESET}")
print (f"\n{YELLOW}URL: {options.url}{RESET}\n")
for i in foundDirs:
    print (f"{GREEN}[+] /{i}{RESET}")

#end_time = perf_counter()

#print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

