import requests
from django.conf import settings
import xmlrpc.client

def authenticate(username, password):
    url = f"https://{settings.ODOO_URL}/web/session/authenticate"
    db = settings.ODOO_DB  # Nama database Odoo
    data = {
        'jsonrpc': '2.0',
        'params': {
            'db': db,
            'login': username,
            'password': password,
        }
    }
    
    session = requests.Session()
    response = session.post(url, json=data)
    if (response.status_code == 200):
        try:
            res = response.json()['result']
            return (True, response.json(), session.cookies)  # Mengembalikan respons Odoo
        except:
            return (False, None, None)
            
    else:
        print('Odoo auth error!')
        return (False, None, None)
    

def auth_xmlrpc(username, password):
    url = f"https://{settings.ODOO_URL}/web/login"
    db = settings.ODOO_DB  # Nama database Odoo
    common = xmlrpc.client.ServerProxy(f'https://{settings.ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})

    if uid:
        # Buat request POST untuk login ke Odoo web agar cookie sesi diset
        session = requests.Session()
        login_data = {
        'jsonrpc': '2.0',
        'params': {
            'db': db,
            'login': username,
            'password': password,
        }
    }
        response = session.post(f'https://{settings.ODOO_URL}/web/login?', data=login_data)
        return response
        
