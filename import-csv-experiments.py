#!/usr/bin/env python

###############
# DESCRIPTION #
##############
#
# This script will read a csv file that contains a list of antibodies, and add
# them to the experiments database with a fine control on which columns are
# processed and how.
#

import elabapi_python
import csv
import json
import urllib3

# disable warnings (they are scary)
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

#########################
#         CONFIG        #
#########################
# replace with your instance address
API_HOST_URL = 'https://elab.local:3148/api/v2'
# replace with your api key
API_KEY = 'apiKey4Test'
# this is the resource category where the entries will be created. Visit /api/v2/items_types to GET a list.
# in this example, category with id 6 corresponds to "Antibody"
RESOURCE_CATEGORY_ID = 6
# path to the csv file, change this too
CSV_PATH = './data/antibodies.csv'
#########################
#      END CONFIG       #
#########################

# Configure the api client
configuration = elabapi_python.Configuration()
configuration.api_key['api_key'] = API_KEY
configuration.api_key_prefix['api_key'] = 'Authorization'
configuration.host = API_HOST_URL
configuration.debug = False
configuration.verify_ssl = False

api_client = elabapi_python.ApiClient(configuration)
api_client.set_default_header(header_name='Authorization', header_value=API_KEY)

experimentApi = elabapi_python.ExperimentsApi(api_client)

# function to build the metadata json for a row
def getMetadataFromRow(row):
    metadata = {'extra_fields': {}}
    for keyval in row.items():
        field_type = 'text'
        if keyval[0] in ['Name', 'Comment', 'ID']:
            continue
        if keyval[0].lower() == 'url':
            field_type = 'url'
        if keyval[0].lower() == 'price':
            field_type = 'number'
        if keyval[0].lower() == 'concentration' and keyval[1]:
            split_conc = keyval[1].split()
            metadata['extra_fields'].update({keyval[0]: {'value': split_conc[0], 'type': 'number', 'unit': split_conc[1], 'units': ['mg/mL', 'μg/mL']}})
        elif keyval[0].lower() == 'primary vs secondary':
            metadata['extra_fields'].update({keyval[0]: {'value': 'Primary', 'type': 'select', 'options': ['Primary', 'Secondary']}})
        elif keyval[0].lower() == 'raised in':
            metadata['extra_fields'].update({keyval[0]: {'value': keyval[1], 'type': 'select', 'options': ['Rabbit', 'Mouse']}})
        elif keyval[0].lower() == 'recognizes':
            metadata['extra_fields'].update({keyval[0]: {
                'value': keyval[1].split(', '), 'type': 'select', 'allow_multi_values': True, 'options': ['Ape', 'Chicken', 'Dog', 'Goat', 'Guinea Pig', 'Hamster', 'Human', 'Mink', 'Monkey', 'Mouse', 'Rabbit', 'Rat', 'Sheep', 'Zebrafish']}})
        else:
            metadata['extra_fields'].update({keyval[0]: {'value': keyval[1], 'type': field_type}})
    return json.dumps(metadata)

def getBodyFromRow(row) -> str:
    return f'<p>{row["Comment"]}</p>' if "Comment" in row else ''

print("Starting import script...")
with open(CSV_PATH, newline='') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        if row.get("elabftw_id"):
            itemId = row["elabftw_id"]
        else:
            print(f'Creating experiment...')
            response = experimentApi.post_experiment_with_http_info(body={})
            locationHeaderInResponse = response[2].get("Location")
            itemId = int(locationHeaderInResponse.split("/").pop())
            row["elabftw_id"] = itemId

        print(f'[-] Patching item {itemId}')
        experimentApi.patch_experiment(itemId, body={'title': row['Name'], 'body': getBodyFromRow(row), 'custom_id': row['ID'], 'metadata': getMetadataFromRow(row)})

print("Everything imported successfully! :)")
