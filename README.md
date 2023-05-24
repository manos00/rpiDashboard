# rpiDashboard
Scripts I created for a dashboard-like screen rendered on an e-paper display.

## Requirements
### Hardware
- [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)
- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/?variant=raspberry-pi-pico-w)
- [Waveshare Pico e-Paper 3.7in](https://www.waveshare.com/wiki/Pico-ePaper-3.7)
### Software (for Zero W)
#### Python Libraries (also found in [requirements.txt](ZeroW/requirements.txt))
These can be installed by running the following command after cloning the repository:

`pip install -r rpiDashboard/ZeroW/requirements.txt`
- cachetools
- certifi
- charset-normalizer
- contourpy
- cycler
- fonttools
- google-api-core
- google-api-python-client
- google-auth
- google-auth-httplib2
- google-auth-oauthlib
- googleapis-common-protos
- httplib2
- idna
- kiwisolver
- matplotlib
- numpy
- oauthlib
- packaging
- Pillow
- protobuf
- pyasn1
- pyasn1-modules
- pyparsing
- python-dateutil
- requests
- requests-oauthlib
- rsa
- six
- uritemplate
- urllib3
#### Programs
- [image-magick](https://imagemagick.org/)

## Zero W
### Step 1
The Pi Zero W fetches data from the following APIs:
- [Tankerkönig API](https://creativecommons.tankerkoenig.de/) (used for getting gas prices)
- [Google Calendar API](https://developers.google.com/calendar/api/guides/overview) (syncing my google calendar events)
- [Weatherapi](https://www.weatherapi.com/)

In addintion it also formats the current date and time.
### Step 2
Most of the data is stored in a plain text file called `formattedData.txt`.
The gas prices are stored in a database, which is then used to draw a graph with time on the x and price on the y-axis.
### Step 3
The graph is exported as an image and converted to a bytearray. The script used for that is [`img_to_bytearray.py`](ZeroW/image_conversion/img_to_bytearray.py). 
It requires image-magick to be installed on the system for it to work.
### Step 4
Lastly the data is wirelessly sent to the Pi Pico W.

## Nano W
### Step 1 (only on boot)
The Pi Nano W connects to the local Wi-Fi.
### Step 2 (every minute)
Upon recieving the data from the Pi Zero W, the Pico generates an output for the e-Paper display and displays the dashboard-screen.
