from flask import Flask, json, jsonify, request, render_template
from appsApi.wiz import WizAPI
from appsApi.orca import OrcaAPI
from appsApi.servicenow import ServiceNowAPI
from appsApi.signalscience import SignalScienceAPI
#from appsApi.divvycloud import DivvyAPI


app = Flask(__name__)
app.config['DEBUG'] = True

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
with open('utilities/query.json', 'r') as query_file:
    query = json.load(query_file)
with open('utilities/variable.json', 'r') as variable_file:
    data = json.load(variable_file)

# Initialize API clients
wiz_api = WizAPI(config,query)
signalscience_api = SignalScienceAPI(config)
servicenow_api = ServiceNowAPI(config)
orca_api = OrcaAPI(config)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/getNavItem')
def getNavItem():
    data = {
        "data": [
            {
                "ID": "1",
                "text": "Number of open ports and services(non-443) exposed to the Internet"
            },
            {
                "ID": "2",
                "text": "Percentage of applications protected by WAF"
            },
            {
                "ID": "3",
                "text": "Percentage of network connectivity through SASE"
            },
            {
                "ID": "4",
                "text": "Additional metrics on FW requests and exceptions"
            }]
    }
    return jsonify(data)

@app.route('/wiz-graphql-data')
def wiz_graphql_data():
    token = wiz_api.request_api_token()
    response = wiz_api.transform_graphql_query_response(token, data)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
