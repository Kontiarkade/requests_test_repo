#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import re
import requests
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import getpass
import time
import yaml

# Default values:
url_string = 'https://nordvpn.com/ru/ovpn/'
regex = re.compile(r'<span class="mr-2">'
                   r'(\S*)'
                   r'</span>')


def isOpen(host, port=80):
    '''
    Checking host for open port
    host - string
    port - string / int
    
    Returns (string, bool)
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      s.connect((host, int(port)))
      s.shutdown(2)
      return host, True
    except:
      return host, False

def getContent(url_string):
    '''
    Loading web page form provided url by using http
    url_string - string
    
    Returns string
    '''
    try:
        print('Geting content from ', url_string)
        r = requests.get(url_string)
        return r.text
    except requests.exceptions.ConnectionError as e:
        raise SystemExit(str(e).strip('()'))
    except requests.exceptions.SSLError as e:
        raise SystemExit(str(e).strip('()'))
    except requests.exceptions.RequestException as e:
        raise SystemExit(str(e).strip('()'))

def findMatches(obj, regex):
    '''
    Searching object using provided regexp
    obj - string
    regex - re object
    
    Returns list
    '''
    print('Finding servers...')
    match = regex.findall(obj)
    if match: return match

def readFile(f):
    '''
    Reading file by chunks
    obj - string
    regex - re object
    
    Returns string
    '''
    with open (f) as f:
        b = ''
        while True:
            a = f.read(1024)
            if not a: break
            b += a
        return b

def writeFile(d):
    print('Making yaml with all servers...')
    timestr = 'all_servers_' + time.strftime("%Y%m%d-%H%M%S") + '.yml'
    with open (timestr, 'w') as f:
        yaml.dump(d, f)
        
def generateProxy(hosts):
    '''
    Generating proxys list
    hosts - list of strings
    
    Returns dictionary
    '''
    print('Generating proxys list...')
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_list = []
        tlist = []
        flist = []
        for host in hosts:
            future = executor.submit(isOpen, host, '80')
            future_list.append(future)
        with click.progressbar(length=len(future_list),
                               show_pos=True,
                               fill_char='#',
                               empty_char=' ') as bar:           
            for f in as_completed(future_list):
                if f.result()[1]:
                    tlist.append(f.result()[0])
                else:
                    flist.append(f.result()[0])                
                bar.update(1)
        d = {True:tlist, False:flist}
        return d
  
def generateConfig(login, password, proxy_d, port=80):
    print('Making config file...')
    timestr = 'config_file_' + time.strftime("%Y%m%d-%H%M%S") + '.txt'
    with open (timestr, 'w') as f:
        for host in proxy_d[True]:
            s = 'http://' + login + ':' + password + '@' + host + ':' + str(port) + '\r\n'
            f.write(s)            

if __name__ == '__main__':  
    '''
    thelist = ['us4948.nordvpn.com', 'us4949.nordvpn.com', 'us4950.nordvpn.com', 'us4951.nordvpn.com', 'us4952.nordvpn.com', 'us4953.nordvpn.com', 'us4955.nordvpn.com', 'us5000.nordvpn.com', 'us5001.nordvpn.com', 'us5002.nordvpn.com', 'us5003.nordvpn.com', 'us5004.nordvpn.com', 'us5005.nordvpn.com', 'us5006.nordvpn.com', 'us5007.nordvpn.com', 'us5008.nordvpn.com', 'us5009.nordvpn.com', 'us5010.nordvpn.com', 'us5011.nordvpn.com', 'us5012.nordvpn.com', 'us5013.nordvpn.com', 'us5014.nordvpn.com', 'us5015.nordvpn.com', 'us5016.nordvpn.com', 'us5017.nordvpn.com', 'us5019.nordvpn.com', 'us502.nordvpn.com', 'us5020.nordvpn.com', 'us5021.nordvpn.com', 'us5022.nordvpn.com']
    tl = ['us4948.nordvpn.com', 'us4949.nordvpn.com', 'us4950.nordvpn.com']    
    d = {True: ['us4949.nordvpn.com', 'us4948.nordvpn.com', 'us5001.nordvpn.com', 'us5000.nordvpn.com', 'us5002.nordvpn.com', 'us5007.nordvpn.com', 'us5006.nordvpn.com', 'us5004.nordvpn.com', 'us5003.nordvpn.com', 'us5005.nordvpn.com', 'us5009.nordvpn.com', 'us5008.nordvpn.com', 'us5011.nordvpn.com', 'us5012.nordvpn.com', 'us5010.nordvpn.com', 'us5013.nordvpn.com', 'us5015.nordvpn.com', 'us5017.nordvpn.com', 'us5016.nordvpn.com', 'us5019.nordvpn.com', 'us5021.nordvpn.com', 'us502.nordvpn.com', 'us5020.nordvpn.com', 'us5022.nordvpn.com', 'us5014.nordvpn.com'], False: ['us4951.nordvpn.com', 'us4950.nordvpn.com', 'us4952.nordvpn.com', 'us4955.nordvpn.com', 'us4953.nordvpn.com']}

    getContent(url_string)
    l = findMatches(t, regex)
    with open ('all_servers.txt', 'w') as f:
        for line in l:
            f.write(line + '\r\n')    
    #Http://login:pass@server:port
    '''
    t = getContent(url_string)
    try:
        l = findMatches(t, regex)    
        d = generateProxy(thelist)
        writeFile(d)
        print('Proxys list successfully generated!')
    except:
        raise SystemExit('Something went terrible wrong!')
    try:
        login = input('Input login: ')
        password = getpass.getpass()
        generateConfig(login, password, d)
    except:
        raise SystemExit('Something went terrible wrong!')
    print('Success!')
