import requests
from django.conf import settings

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
        return (True, response.json(), session.cookies)  # Mengembalikan respons Odoo
    else:
        print('Odoo auth error!')
        return (False, None, None)
        
