import requests
import json
import boto3


SM = boto3.client('secretsmanager',region_name='us-west-2')

class DivvyAPI(object):
    def __init__(self, config):
        self.divvy_creds = json.loads(SM.get_secret_value(SecretId=f'/INFRASEC-C-UW2/{config["Divvycloud"]["COMMERCIAL_SSM_PARAM"]}')['SecretString'])
        self.base_url = config["Divvycloud"]["COMMERCIAL_URL"]
    
    def get_auth(self):
        divvy_params = self.divvy_creds
        resp = requests.request(
            'POST',
            url=f'{self.base_url}/v2/public/user/login',
            data=json.dumps({"username":divvy_params["username"],"password":divvy_params["password"]}),
            headers={'Content-Type': 'application/json'}
        )
       
        if resp.status_code == 200:
            jsonData = resp.json()
            return jsonData



with open('config.json', 'r') as config_file:
    config = json.load(config_file)


my_instance = DivvyAPI(config)
response_check = my_instance.get_auth()
print(response_check)
