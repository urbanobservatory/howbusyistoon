import os
import json
import datetime
import logging
import random
import numpy as np
import urllib.request
import schedule
import time
from urllib.error import HTTPError

LOCAL_DEV = False # todo - setup testing/production pipelines; not this hack

CARPARKS_NAMES = ['Eldon%20Square', 'Claremont%20Road', 'Dean%20Street', 'Eldon%20Garden', 'Ellison%20Place', 'Grainger%20Town', 'Manors']
CARPARKS_API_URL = 'https://api.newcastle.urbanobservatory.ac.uk/api/v2/sensors/entity?metric="Occupied%20spaces"&name="{car_park}"'
FOOTFALL_SENSOR_NAMES = ['PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_0', 'PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_1']
FOOTFALL_API_URL = "https://newcastle.urbanobservatory.ac.uk/api/v1.1/sensors/{sensor_name}/data/json/?starttime={start_time}&endtime={end_time}" 
ACTIVITY_LEVELS = ['quiet', 'average', 'busy']

# Assert an output directory exists
if not os.path.exists('out'):
    os.makedirs('out')

if LOCAL_DEV:
    FILE_NAME_CREDENTIALS = "settings.json" # local dev
    CAR_PARKS_PUBLIC_BAYS = "car_park_capacity.json" # local dev
    FILE_NAME_LATEST_CITY_STATE = "testing/latest_city_state.json"
    FILE_NAME_LATEST_CAR_PARKS = "testing/latest_car_parks.json"
    FOOTFALL_TIME_WINDOW_MINUTES = 120
else:
    FILE_NAME_LATEST_CITY_STATE = "latest_city_state.json"
    FILE_NAME_LATEST_CAR_PARKS = "latest_car_parks.json"
    FILE_NAME_CREDENTIALS = "settings.json"
    CAR_PARKS_PUBLIC_BAYS = "car_park_capacity.json"
    FOOTFALL_TIME_WINDOW_MINUTES = 60

# logging
logging.basicConfig(format='%(asctime)s %(funcName)s [%(lineno)d] %(message)s', level=logging.DEBUG)

# start
logging.info('Update service started')

# load credentials/settings
#with open(FILE_NAME_CREDENTIALS, 'r') as fIn:
#    creds = json.load(fIn)
#logging.debug("Credentials loaded.")

# load car parks public bays
with open(CAR_PARKS_PUBLIC_BAYS, 'r') as fIn:
    car_park_public_bays = json.load(fIn)
logging.debug("Car park bays loaded.")


def extract_footfall(sensor_name, response):
    logging.debug(f"{sensor_name};{response}")
    tmp = json.loads(response)
    out = dict()
    out['sensor_name'] = sensor_name
    footfall_all = []

    # check that UO returned some data
    if len(tmp['sensors'][0]['data']) > 0:
        for record in tmp['sensors'][0]['data']['Walking North']:
            footfall_all.append(record['Value'])
        for record in tmp['sensors'][0]['data']['Walking South']:
            footfall_all.append(record['Value'])
    else:
        # end early - no datapoints returned; don't return 0 as activity level
        return(out)
    
    # format stats
    out['number_of_datapoints'] = len(footfall_all) / 2
    out['average_people_count'] = round(np.sum(footfall_all) / out['number_of_datapoints'], 2)
    return(out)

def get_footfall_data(sensors, api_url):
    logging.debug(f"{sensors};{api_url}")
    result = []
    for sensor in sensors:
        time_now = datetime.datetime.now()
        end_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        start_time = (time_now - datetime.timedelta(minutes=FOOTFALL_TIME_WINDOW_MINUTES)).strftime("%Y%m%d%H%M")
        sensor_url = api_url.format(sensor_name = sensor, start_time = start_time, end_time = end_time)
        logging.debug(sensor_url)
        try:
            contents = urllib.request.urlopen(sensor_url).read()
            out = extract_footfall(sensor, contents)
        except HTTPError as e:
            logging.error("UO API call failed: " + e)
        result.append(out)
    return(result)

def get_carpark_activity(current_occupancy): # todo recode for easier mod
    logging.debug(f"{current_occupancy}")
    if current_occupancy < 35:
        return(ACTIVITY_LEVELS[0])
    elif current_occupancy < 75:
        return(ACTIVITY_LEVELS[1])
    return(ACTIVITY_LEVELS[2])

# checks against the static file loaded at the beginning for the car park
# if not found the public bays information, uses whatever UO says 
def get_car_park_capacity(carpark_name, carparks_prepopulated, carpark_received):
    if carpark_name in carparks_prepopulated:
        return carparks_prepopulated[carpark_name]
    else:
        return carpark_received

def extract_carpark_data(response, carparks):
    logging.debug(f"{response};{carparks}")
    tmp = json.loads(response)
    carpark_out = dict()
    if len(tmp['items']) > 0:
        carpark_out['name'] = tmp['items'][0]['meta']['name']
        ts = tmp['items'][0]['feed'][0]['timeseries'][0]['latest']['time'] # get timestamp
        carpark_out['timestamp'] = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone().isoformat() # parse and format
        carpark_out['capacity'] = get_car_park_capacity(carpark_out['name'], car_park_public_bays, tmp['items'][0]['feed'][0]['meta']['totalSpaces']) # if not latest info provided upfront, use what UO has
        carpark_out['occupancy'] = tmp['items'][0]['feed'][0]['timeseries'][0]['latest']['value']
        carpark_out['reserved_bays'] = 0 # todo update once we know
        carpark_out['free_spaces'] = carpark_out['capacity'] - carpark_out['occupancy'] - carpark_out['reserved_bays']
        carpark_out['state'] = get_carpark_activity(carpark_out['occupancy'] * 100 / carpark_out['capacity'])  
    return(carpark_out)

def get_carpark_data(carparks, api_url):
    logging.debug(f"{carparks};{api_url}")
    out = []
    for carpark in carparks:
        tmp_url = api_url.format(car_park = carpark)
        logging.debug(tmp_url)
        try:
            contents = urllib.request.urlopen(tmp_url).read() 
        except HTTPError as e:
            logging.error("UO API call failed: " + e)
        out.append(extract_carpark_data(contents, carpark))
    return(out)    

def get_city_activity(footfall): # todo record for easier mod
    logging.debug(f"{footfall}")
    total_footfall = 0
    for record in footfall:
        # check if something fell over
        if 'average_people_count' in record:
            total_footfall += record['average_people_count']
        # else: log problem todo
    logging.info(f"total_footfall: {total_footfall}; len(footfall): {len(footfall)}")
    total_footfall = total_footfall / len(footfall)
    if total_footfall < 25:
        return(ACTIVITY_LEVELS[0])
    elif total_footfall < 100:
        return(ACTIVITY_LEVELS[1])
    return(ACTIVITY_LEVELS[2])

def format_city_state(footfall, response_time):
    logging.debug(f"{footfall},{response_time}")
    out = dict()
    out['timestamp'] = str(datetime.datetime.now().astimezone().isoformat())
    out['response_time_us'] = response_time.microseconds 
    out['city_state'] = get_city_activity(footfall)
    out['footfall'] = footfall
    return(out)

def format_car_parks(carparks, response_time):
    logging.debug(f"{carparks},{response_time}")
    out = dict()
    out['timestamp'] = str(datetime.datetime.now().astimezone().isoformat())
    out['response_time_us'] = response_time.microseconds 
    out['carparks'] = carparks
    return(out)    

def update_all():
    # ToDo - put everything into classes; tidy-up this mess
    # ToDo - split city state from car park execution
    # ToDo - monitor lag in response time from UO
    # CAR PARKS
    # # start the clock for car parks
    start_time = datetime.datetime.now()

    # pull the car parks data
    carpark_out = get_carpark_data(CARPARKS_NAMES, CARPARKS_API_URL)
    print(carpark_out)
    # # persist car parks
    file_name = f"ncc-car-parks.json"
    if LOCAL_DEV:
        local_file_name = "out" + os.sep + file_name # todo uff
    else:
        local_file_name = "out" + os.sep + file_name # todo uff    

    # # local copy
    with open(local_file_name, 'w') as fOut:
        fOut.write(json.dumps(format_car_parks(carpark_out, datetime.datetime.now() - start_time)))

    # persist locally
    car_out = []

    for carpark in carpark_out:
        car_out.append(f"{carpark['name']}:{carpark['occupancy']}") 
    logging.info(carpark_out)

    # CITY STATE
    # pull all footfall data
    footfall_out = get_footfall_data(FOOTFALL_SENSOR_NAMES, FOOTFALL_API_URL)
    logging.debug(format_city_state(footfall_out, datetime.datetime.now() - start_time))

    # # persist city state
    file_name = f"ncc-city-state.json"
    if LOCAL_DEV:
        local_file_name = "out" + os.sep + file_name # todo uff
    else:
        local_file_name = "out" + os.sep + file_name # todo uff

    # local copy
    city_state = format_city_state(footfall_out, datetime.datetime.now() - start_time)
    with open(local_file_name, 'w') as fOut:
        fOut.write(json.dumps(city_state))

    logging.info(footfall_out)

    logging.info(f"Update complete. City is {city_state['city_state']}, processing time: {city_state['response_time_us']} us")


# Initial run
update_all()

# Scheduled runs
schedule.every(5).minutes.do(update_all)
while True:
    schedule.run_pending()
    time.sleep(1)
