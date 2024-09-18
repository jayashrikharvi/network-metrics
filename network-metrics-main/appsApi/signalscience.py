import requests

class SignalScienceAPI:
    def __init__(self, config):
        self.api_user = config['signal_science']['API_USER']
        self.api_token = config['signal_science']['API_TOKEN']
        self.base_url = config['signal_science']['BASE_URL']
        self.corp_name = config['signal_science']['CORP_NAME']
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-token': f'{self.api_token}',
            'x-api-user': f'{self.api_user}'
        }

    def get_sites(self):
        url = f"{self.base_url}/corps/{self.corp_name}/sites"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()  # Assuming the JSON response contains a 'data' key with the list of sites
        else:
            raise Exception('Failed to retrieve sites')

