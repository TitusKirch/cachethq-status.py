from cachet import Cachet
from status import Status
import configparser
import os
import json
from datetime import datetime
import time

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

        # check if protocol is uninteresting bot
        if component['protocol'] == "uninteresting_bot":

            # check if statuspage provider
            if "statuspage" in component and "provider" in component['statuspage']:
                if component['statuspage']['provider'] == "cachet":
                    if "interval" in component['statuspage']:

                        # check if id isset
                        if "id" in component['statuspage']:
                            
                            # set path
                            path = "/api/v1/components/" + str(component['statuspage']['id'])

                            # get cachet component
                            response = cachet.get(path, payload)

                            # check status code
                            if response.status_code == 200:

                                # get json
                                json = json.loads(response.text)['data']

                                # check status
                                if json['status'] != 4:

                                    # get last update
                                    lastUpdateBefore = int(time.mktime(datetime.strptime(json['updated_at'], "%Y-%m-%d %H:%M:%S").timetuple())) - int(datetime.timestamp(datetime.now()))
                                    lastUpdateBefore = int(lastUpdateBefore/(-1))

                                    # check if last update is not in interval
                                    if lastUpdateBefore > int(component['statuspage']['interval']):

                                        # get status
                                        status = Status(component['protocol'], component['address']).get()

                                    else:
                                        continue
                                else:
                                    continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            # get status
            status = Status(component['protocol'], component['address']).get()

        # check if statuspage provider
        if "statuspage" in component and "provider" in component['statuspage']:
            if component['statuspage']['provider'] == "cachet":

                # check if id isset
                if "id" in component['statuspage']:

                    # set payload and path
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

