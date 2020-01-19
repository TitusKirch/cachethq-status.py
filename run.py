from cachet import Cachet
from status import Status
import configparser
import os
import json
from datetime import datetime

if __name__ == "__main__":
    # get constants
    DIR = os.path.join(os.getcwd(), '')

    # create config
    config = configparser.ConfigParser()

    # check if default config file exist
    if os.path.isfile(DIR + "config_default.ini"):
        config.read(DIR + "config_default.ini")

    # check if custom config file exist
    if os.path.isfile(DIR + "config.ini"):
        config.read(DIR + "config.ini")

    # create components and metrics
    components = []
    metrics = []

    # check if components file exist
    if os.path.isfile(DIR + "components.json"):
        file = open(DIR + "/components.json")
        jsonData = json.load(file)
        components = jsonData['components']
        metrics = jsonData['metrics']
        file.close()
    
    # create cachet
    cachet = None
    
    # check if cachet url isset
    if config['cachet']['url'] not in ["", "myUrl"]:
        # check if api_token isset
        if config['cachet']['api_token'] not in ["", "myToken"]:

            #create new cachet connection
            cachet = Cachet(config['cachet']['url'], config['cachet']['api_token'])

    # go through all components
    for component in components:
        
        # get status
        status = Status(component['protocol'], component['address']).get()

        # check if statuspage provider
        if "statuspage" in component and "provider" in component['statuspage']:
            if component['statuspage']['provider'] == "cachet":

                # check if id isset
                if "id" in component['statuspage']:

                    # set payload
                    payload = "{\"status\": " + str(status) + ", \"meta\":{\"time\": \"" + str(int(datetime.timestamp(datetime.now()))) + "\"}}"
                    path = "/api/v1/components/" + str(component['statuspage']['id'])

                    # update cachet component
                    cachet.update(path, payload)
    
    # go through all metrics
    for metric in metrics:
        
        # get status
        status = Status(metric['protocol'], metric['address']).get()

        # check if statuspage provider
        if "statuspage" in metric and "provider" in metric['statuspage']:
            if metric['statuspage']['provider'] == "cachet":

                # check if id isset
                if "id" in metric['statuspage']:

                    # set payload
                    payload = "{\"value\": " + str(int(status)) + ", \"timestamp\": "+ str(int(datetime.timestamp(datetime.now()))) + "}"
                    path = "/api/v1/metrics/" + str(metric['statuspage']['id']) + "/points"
                    
                    # update cachet metric
                    cachet.add(path, payload)

