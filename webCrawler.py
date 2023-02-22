#!/usr/bin/env python

import requests
import re
from colorama import Fore, init
import argparse
import os
from uritools import urijoin

init()
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
RESET = Fore.RESET

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", dest="url", help="URL a escanear. webCrawler.py -u https://google.com")
parser.add_argument("-c", "--code", dest="code", nargs="*", help="Códigos a extraer. webCrawler.py -u https://google.com -c 200")
parser.add_argument("-d", "--dict", dest="dicText", nargs="*", help="Códigos a extraer. webCrawler.py -u https://google.com -c 200 -d common.txt")
parser.add_argument("-r", "--rec", dest="recursive", nargs="*", help="Buscar directorios recursivamente. webCrawler.py -u https://google.com -c 200 -r true")
parser.add_argument("-l", "--link", dest="link", nargs="*", help="Extraer enlaces de la web indicada. webCrawler.py -u https://google.com -l true")
options = parser.parse_args()

codigo = []

if options.code:
    for i in options.code:
        if i != ",":
            codigo.append(i)

url = options.url
foundDirs = []
foundD2 = []
dirsD = []
targetLinks = []

def getDirs(urlParam, listURL):

    if os.path.exists(options.dicText):
    
        with open(options.dicText, "r") as directories:
        
            for line in directories.read().splitlines():
                if line[0:0] != "#" and url[-2] != "/":
                    subDirURL = urlParam + line

                    try:
                        getResponse = requests.get(subDirURL)
                        filterResponse = re.search("\d\d\d", str(getResponse))
        
                        print (f"\r{YELLOW}-> {subDirURL}{RESET}", end="", flush=True)
                        if filterResponse.group(0) in codigo:
                            if line not in listURL:
                                listURL.append(line)
                        else:
                            pass
                    except:
                        print (f"{RED}Error al conectar con el objetivo: {subDirURL}{RESET}")
                        exit()
                else:
                    pass

    else:
        print (f"{RED}El diccionario indicado no existe!{RESET}\n")


if options.dicText:

    getDirs(url, foundDirs)
    
    print (f"\r{CYAN}", "DIRECTORIOS ENCONTRADOS".center(90, "-"), f"{RESET}")
    print (f"\n{YELLOW}URL: {options.url}{RESET}\n")

    if len(foundDirs) != 0:
        for i in foundDirs:
            print (f"{GREEN}[+] /{i}{RESET}")

        if options.recursive:

            print (f"\n\n{YELLOW}[+] Buscando subdirectorios...\n")

            for i in foundDirs:
                recURL = url + i + '/'

                if recURL not in foundDirs:
                    getDirs(recURL, foundD2)
    
                    for j in foundD2:
                        newURL = i + '/' + j
                        dirsD.append(newURL)

        print ()
        for k in dirsD:
            print (f"{GREEN}-> {k}{RESET}")
    else:
        pass

if options.link:

    requestContent = requests.get(options.url)
    storeLinks = re.findall('(?:href=")(.*?)"', str(requestContent.content))
    for i in storeLinks:
        link = urijoin(options.url, i)
        if link not in targetLinks and "#" not in link:
            targetLinks.append(link)
        else:
            pass
    for i in targetLinks:
        print (f"{GREEN}[+] {i}{RESET}")


