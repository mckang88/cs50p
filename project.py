#! /usr/bin/python3
# Python script to output search results in json format on pubs within 500 meters.

import sys
import argparse
import requests
import json
import geocoder
from itertools import islice

def main():

    parser = argparse.ArgumentParser(description='''Gives output of top 5 best rated pubs near the suburb that was input''')
    parser.add_argument("-a", "--address", help="Street address and name, e.g. 123 John St")
    parser.add_argument("-c", "--city", help="Name of the city, e.g. Sydney")
    parser.add_argument("-s", "--state", help="Name of the state, e.g. NSW")
    args = parser.parse_args()
    # if no argument given, default to my IP
    if len(sys.argv) == 1:
        location = my_location()
    else:
        location = geo_code(args)

    # Request URL for Google maps text search API to look for pubs in that location
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?location={location}&query=pub&radius=500&strictbounds=true&opennow=true&key={api_key()}"
    #print(url)

    payload={}
    headers = {}
    response = requests.get(url, headers=headers, data=payload)
    print(filter_json(response.json()))

# Reads API key from the key file in this directory
def api_key():
    try:
        with open("key") as file:
            api_key = file.read()
            return api_key
    except FileNotFoundError:
        return "key file not found"

# return city in geocode location
def geo_code(a):
    try:
        geocode = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={a}&key={api_key()}")
        geocode_result = geocode.json()
        # get values for Latitude and Longitude
        lat = geocode_result["results"][0]["geometry"]["location"]["lat"]
        lng = geocode_result["results"][0]["geometry"]["location"]["lng"]
        return str(lat)+","+str(lng)
    except IndexError:
        sys.exit("Invalid Address")

# find my location based on my public IP address
def my_location():
    my_ip = geocoder.ip("me")
    # list comprehension to conver it to string
    string = ','.join([str(s) for s in my_ip.latlng])
    return string

# Takes json data and filters out redudant info
# Returns top 5 rated pubs
def filter_json(j):
    try:
        filtered_data = []
        for data in j["results"]:
            json_data = {
                "name": data["name"],
                "rating": data["rating"],
                "address": data["formatted_address"],
            }
            filtered_data.append(json_data)
        # Sort results by rating
            filtered_data.sort(key=lambda x: x["rating"], reverse=True)
            new_data = top5(5, filtered_data)
    except:
        raise ValueError("Invalid format")
    return json.dumps(new_data, indent=2)

# Returns top 5 results
def top5(n, iterable):
    try:
        return list(islice(iterable, n))
    except:
        raise ValueError("Invalid format")

if __name__ == "__main__":
    main()


