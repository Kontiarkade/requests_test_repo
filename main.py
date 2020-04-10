#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import socket
import ssl

from concurrent.futures import ThreadPoolExecutor, as_completed

def isOpen(host, port):
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
    result = ''
    s = socket.socket()
    host = socket.gethostbyname(url_string)
    port = 80
    s.connect((host,port))
    s.sendall(b"GET /\r\n")
    while True:
        data = s.recv(1024)
        if not data: break
        result += data.decode('utf-8')
    return result

def getSSLContent(url_string):
    '''
    Loading web page form provided url by using https
    url_string - string
    
    Returns string
    '''
    result = ''
    s = socket.socket()
    host = socket.gethostbyname(url_string)
    port = 443
    s.connect((host,port))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None,
                    server_side=False, cert_reqs=ssl.CERT_NONE,
                    ssl_version=ssl.PROTOCOL_SSLv23)
    s.sendall(b"GET /\r\n")
    while True:
        data = s.recv(1024)
        if not data: break
        result += data.decode('utf-8')
    return result

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
    #print(getSSLContent('www.google.com'))
    regex = re.compile(r'<span class="mr-2">'
           r'(\S*)'
           r'</span>')
    t = readFile('source.txt')
    #templist = findMatches(t, regex)
    templist = [
        '10.10.53.101', '10.10.53.2', 'google.com'
    ]
    print(generateProxy(templist))
    
        
    
    
