import requests

class OrcaAPI:
    def __init__(self, config):
        self.api_key = config['orca']['ORCA_API_KEY']
        self.api_url = config['orca']['ORCA_API_URL']
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{self.api_key}'
        }

    def get_vulnerabilities(self):
        url = f"{self.api_url}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()  # Assuming the JSON response contains a 'data' key with the list of sites
        else:
            raise Exception('Failed to retrieve vulnerabilities')

