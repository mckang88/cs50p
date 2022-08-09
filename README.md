# Pubs near me
### Video Demo:  <URL HERE>
### Description:
This python script is to show where are the 5 best pubs around my area.

It uses Googles maps API to retrieve results.

https://developers.google.com/maps/documentation/places/web-service/search-text

### Preparation
You will need to get Google maps API key from below.

https://developers.google.com/maps/documentation/javascript/get-api-key

Once the key is generated, create a file in the same directory as project.py as "key"

Install geocoder package which will provide coordination of your IP address.
```
pip install geocoder
```

### Usage
```
usage: project.py [-h] [-a ADDRESS] [-c CITY] [-s STATE]
```
If no argument options are input, it will default to the location of your public IP.

Adding all 3 arguments (street address, city, state) will give the best results.

It will only show pubs that are currently opened.

### Additonal notes
- Some pubs may not show as some of them are classified as hotels by Google.
- It will try to show results within 500m of the location but could go up to 50kms