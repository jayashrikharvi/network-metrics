import requests
from requests.auth import HTTPBasicAuth
import base64
import json
import warnings
warnings.filterwarnings("ignore")

class ServiceNowAPI:
    def __init__(self, config):
        self.instance = config['servicenow']['SERVICENOW_INSTANCE']
        self.user = config['servicenow']['SERVICENOW_USER']
        self.password = config['servicenow']['SERVICENOW_PASSWORD']
        self.table = config['servicenow']['SERVICENOW_TABLE']
        self.base_url = f"https://{self.instance}.service-now.com/api/now/table/{self.table}"
        self.queryparam = config['servicenow']['QP_EXCEPTION_REQ']
        self.queryparam_fw = config['servicenow']['QP_TICKET_REQ']

        #Converting authorization to base64 encoded format to send in request
        authorization = self.user+':'+self.password
        text_bytes = authorization.encode('utf-8')
        base64_bytes = base64.b64encode(text_bytes)
        self.encoded_authorization = base64_bytes.decode('utf-8')

    def service_now_exception(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        url= self.base_url+'?'+self.queryparam
        response = requests.get(url=url,headers=headers,auth=HTTPBasicAuth(self.user, self.password))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to retrieve records')
    
    def service_now_firewall(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        exception_ticket = self.service_now_exception()
        for value in exception_ticket["result"]:
            ritm_values = value["variables.enter_firewall_ritm"].replace(',','%2c')
            firewall_url = self.base_url+'?'+self.queryparam_fw+ritm_values
            response = requests.get(url=firewall_url,headers=headers,auth=HTTPBasicAuth(self.user, self.password))
            for result in response.json()["result"]:
                firewallTickets = []
                firewallTickets.append(result["number"])
            modified_response = json.dumps(response.json()).replace("result","firewallTickets")
            modified_response = json.loads(modified_response)
            value["firewallTickets"] = firewallTickets
            value["firwewallTicketsDetails"] = modified_response["firewallTickets"]
        return exception_ticket


with open('config.json', 'r') as config_file:
    config = json.load(config_file)


my_instance = ServiceNowAPI(config)
my_instance.service_now_firewall()

        