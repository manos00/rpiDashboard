from calendar_sync.calendardisplay import getEvents, formatEvents
from gas_station_display.tankerkoenig import update_prices, draw_graph
from weather_sync.weather_sync import getWeather
from image_conversion.img_to_bytearray import convert
# from date_sync import update_date
import socket
from os.path import getsize
from time import sleep

def send(file=None):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.178.112"
    port = 420
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected to ", host)
    if not file:
        file = input("File to Transfer : ")
    filesize = getsize(file)
    s.send(f"{file}{SEPARATOR}{filesize}".encode())
    #file = open(filename, 'wb') 

    with open(file, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
    s.close()

# execute methods to get data
# datestr = update_date()
weatherstr = getWeather()
calendarEvents = getEvents()
eventstr = formatEvents(calendarEvents)
update_prices()
draw_graph()

# clear data from file
open('formattedData.txt', 'w').truncate(0)

# write data to text file
for str in [weatherstr, eventstr]: # datestr
    with open('formattedData.txt', 'a') as f:
        f.write(f'\n{str}\n<HLINE>')
        f.close()

# send data to pico
for i in range(15):
    try:
        send('formattedData.txt')
        break
    except ConnectionRefusedError as error:
        print(error)
        sleep(1)
        if i == 14:
            print('bruh moment')
            exit()

sleep(5)

# convert generated gas prices graph to bytes and send it to the pico
convert('gas_station_display/e5.png')
for i in range(15):
    try:
        send('image_conversion/out')
        break
    except ConnectionRefusedError as error:
        print(error)
        sleep(1)
