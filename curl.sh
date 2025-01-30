#!/usr/bin/env bash

echo "This script shows how to use cURL to interact with eLabFTW's REST API"

usage() {
    echo "Usage: SITE_URL=<your_site_url> APIKEY=<your_api_key> ./curl.sh"
    echo "\nBoth SITE_URL and APIKEY environment variables must be set."
    exit 1
}

# Check if SITE_URL is set and not empty
if [[ -z "$SITE_URL" ]]; then
    echo "Error: SITE_URL is not set or is empty."
    usage
fi

# Check if APIKEY is set and not empty
if [[ -z "$APIKEY" ]]; then
    echo "Error: APIKEY is not set or is empty."
    usage
fi

# SCRIPT START

# GET /info
# -k flag is to allow self signed certs
# -s flag is to hide transfer information
echo "GET /info"
curl -sk -H "Authorization: $APIKEY" -H "Content-Type:application/json" "{$SITE_URL}/info" | jq

echo "--------------------------"
echo "GET /experiments/1"
curl -sk -H "Authorization: $APIKEY" -H "Content-Type:application/json" "{$SITE_URL}/experiments/1" | jq

echo "Creating an experiment..."
# -D flag is to get response headers
response_headers=$(curl -sk -D - -o /dev/null \
    -H "Authorization: $APIKEY" \
    -H "Content-Type:application/json" \
    -X POST \
    -d '{"title": "Created from API"}' \
    "${SITE_URL}/experiments/")
location_header=$(echo "$response_headers" | grep -i "^Location:" | awk '{print $2}' | tr -d '\r\n')
echo "New experiment created: "${location_header}""

echo "Changing the title..."
curl -sk -o /dev/null \
    -H "Authorization: $APIKEY" \
    -H "Content-Type:application/json" \
    -X PATCH \
    -d '{"title": "New title from API"}' \
    "$location_header"

echo "Verifying the title has been changed..."
echo -n "Title attribute after doing a GET: "
curl -sk \
    -H "Authorization: $APIKEY" \
    -H "Content-Type:application/json" \
    "$location_header" | jq -r '.title'
