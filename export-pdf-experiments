#!/usr/bin/env python3
import datetime
import os
import elabapi_python
import urllib3

###############
# DESCRIPTION #
##############
# In this script, we list experiments from a user and save the recently modified ones into a PDF.
##############

# Configuration with hardcoded API key
API_HOST_URL = 'https://elab.local:3148/api/v2'  # your host URL or any other endpoint you need
API_KEY = 'apiKey4Test'  # Replace with your API key
PERIOD_IN_DAYS = 61  # Or any other period you prefer
user_id = 2 # your own user ID
save_dir = "C:\\...\\files" # the location where to save it, \\-slash for windows users and /-slash for linux users 

if not API_KEY:
    raise ValueError("API_KEY is not set in the script")

#########################
# Suppress SSL warnings (optional, not recommended for production)
#########################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#########################
# Configure the api client
#########################
configuration = elabapi_python.Configuration()
configuration.api_key['api_key'] = API_KEY
configuration.api_key_prefix['api_key'] = 'Authorization'
configuration.host = API_HOST_URL
configuration.debug = False
configuration.verify_ssl = True  # Enable SSL verification

# Create an instance of the API class
api_client = elabapi_python.ApiClient(configuration)
api_client.set_default_header(header_name='Authorization', header_value=API_KEY)

#### SCRIPT START ##################

# Load the experiments API
experimentsApi = elabapi_python.ExperimentsApi(api_client)

# Get the current date and calculate the range
today = datetime.date.today()
date_from = today - datetime.timedelta(days=PERIOD_IN_DAYS)

# Print the date range for debugging
print(f"Fetching experiments modified after: {date_from}")

# Create the save directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

print(f"Saving PDFs to: {save_dir}")

# Get a list of experiments for the specified user ID (with or without date filter)
try:
    # Temporarily disable the timestamp filter to get all experiments
    # results = experimentsApi.read_experiments(owner=user_id, limit=9999, extended=f'timestamped:yes timestamped_at:>{date_from}')
    results = experimentsApi.read_experiments(owner=user_id, limit=9999)  # No date filter
except elabapi_python.exceptions.ApiException as e:
    print(f"Error fetching experiments: {e}")
    exit(1)

# Debugging: Check how many experiments are found
print(f"Number of experiments found: {len(results)}")
if len(results) == 0:
    print("No experiments found in the given period.")

# Save each experiment as a PDF
for exp in results:
    now = datetime.datetime.now()
    # Define the filename and include the save directory
    filename = os.path.join(save_dir, f'{exp.id}-{exp.elabid}-{now.strftime("%Y-%m-%d_%H-%M-%S")}-export.pdf')
    print(f'Saving file {filename}')

    try:
        # Download and save the PDF
        pdf_data = experimentsApi.get_experiment(exp.id, format='pdf', _preload_content=False).data
        if not pdf_data:
            print(f"Error: No PDF data found for experiment {exp.id}.")
        else:
            with open(filename, 'wb') as file:
                file.write(pdf_data)
    except Exception as e:
        print(f"Failed to save experiment {exp.id} as PDF: {e}")
