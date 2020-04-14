#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import requests
import socket

from concurrent.futures import ThreadPoolExecutor, as_completed

def isOpen(host, port=80):
    '''
    Checking host for open port
    host - string
    port - string / int
    
    Returns string, bool
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
    r = requests.get(url_string)
    return r.text

def findMatches(obj, regex):
    '''
    Searching object using provided regexp
    obj - string
    regex - re object
    
    Returns list
    '''
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
            b = b + a
        return b

def generateProxy(hosts):
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_list = []
        t = []
        for host in hosts:
            future = executor.submit(isOpen, host, '80')
            future_list.append(future)
        for f in as_completed(future_list):
            t.append(f.result())
        return t

  


if __name__ == '__main__':
    
    thelist = ['us4948.nordvpn.com', 'us4949.nordvpn.com', 'us4950.nordvpn.com', 'us4951.nordvpn.com', 'us4952.nordvpn.com', 'us4953.nordvpn.com', 'us4955.nordvpn.com', 'us5000.nordvpn.com', 'us5001.nordvpn.com', 'us5002.nordvpn.com', 'us5003.nordvpn.com', 'us5004.nordvpn.com', 'us5005.nordvpn.com', 'us5006.nordvpn.com', 'us5007.nordvpn.com', 'us5008.nordvpn.com', 'us5009.nordvpn.com', 'us5010.nordvpn.com', 'us5011.nordvpn.com', 'us5012.nordvpn.com', 'us5013.nordvpn.com', 'us5014.nordvpn.com', 'us5015.nordvpn.com', 'us5016.nordvpn.com', 'us5017.nordvpn.com', 'us5019.nordvpn.com', 'us502.nordvpn.com', 'us5020.nordvpn.com', 'us5021.nordvpn.com', 'us5022.nordvpn.com']
    
    tl = ['us4948.nordvpn.com', 'us4949.nordvpn.com', 'us4950.nordvpn.com']
    
    
    regex = re.compile(r'<span class="mr-2">'
           r'(\S*)'
           r'</span>')
    '''
    t = getContent('https://nordvpn.com/ru/ovpn/')
    l = findMatches(t, regex)
    with open ('all_servers.txt', 'w') as f:
        for line in l:
            f.write(line + '\r\n')    
    '''    
    t = getContent('https://nordvpn.com/ru/ovpn/')
    l = findMatches(t, regex)
    print(generateProxy(l))
    
    
