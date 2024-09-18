import requests

def check_trial_status(user_id):
    url = 'http://127.0.0.1:8000/trial/'
    params = {'email': user_id}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Akan menghasilkan exception untuk kode status 4xx/5xx

        # Memeriksa dan mencetak hasil
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data['status']}, Message: {data['data']['msg']}")
        else:
            print(f"Unexpected response code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Ganti '1' dengan ID pengguna yang ingin Anda periksa
check_trial_status('admin.com')
