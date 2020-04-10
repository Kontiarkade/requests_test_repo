#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import HTTPError

def get_page(page):
    try:
        response = requests.get(page)
        if '200' in str(response):
            print(response.status_code)
            print(response)            
        else:
            print('oops')
    
    except HTTPError as e:
        print('Mistake', e)
    
    except Exception as err:
        print(f'Other error occurred: {err}')

if __name__ == '__main__':
    t = 'https://ya.ru'
    #t = 'https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations'
    #get_page(t)
