import requests
import json
import base64

class WizAPI:
    def __init__(self, config, query):
        self.client_id = config['wiz']['CLIENT_ID']
        self.client_secret = config['wiz']['CLIENT_SECRET']
        self.auth_url = config['wiz']['AUTH_URL']
        self.query_one = query['queries']['wiz_query_one']

    def request_api_token(self):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        auth_payload = f'grant_type=client_credentials&audience=wiz-api&client_secret={self.client_secret}&client_id={self.client_id}'
        response = requests.post(url=self.auth_url, headers=headers, data=auth_payload)
        response.raise_for_status()
        return response.json()['access_token']
        
    def pad_base64(self, data):
        return data + "=" * (-len(data) % 4)

    def execute_graphql_query(self, token, variable):
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        payload = json.dumps({"query": self.query_one, "variables": variable})

        dc = json.loads(base64.b64decode(self.pad_base64(token.split(".")[1])))["dc"]
        api_url = f'https://api.{dc}.app.wiz.io/graphql'
        response = requests.post(api_url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()
    
    def transform_graphql_query_response(self, token, variable):
        query_response = self.execute_graphql_query(token, variable)
        final_response = {"virtualMachines": []}
        
        for node in query_response["data"]["graphSearch"]["nodes"]:
            entity = node["entities"][0]
            vm_info = {
                "id": entity["id"],
                "name": entity["name"],
                "cloudPlatform": entity["properties"]["cloudPlatform"],
                "externalId": entity["properties"]["externalId"],
                "validatedOpenPorts": entity["properties"]["validatedOpenPorts"],
                "applicationEndpoint": [
                    {
                        "id": app["id"],
                        "name": app["name"],
                        "port": app["properties"]["port"]
                    }
                    for exposure in entity["publicExposures"]["nodes"]
                    if exposure.get("applicationEndpoints")
                    for app in exposure["applicationEndpoints"]
                ]
            }
            final_response["virtualMachines"].append(vm_info)
            
        return final_response
