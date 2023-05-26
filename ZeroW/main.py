from calendar_sync.calendardisplay import getEvents, formatEvents
from gas_station_display.tankerkoenig import update_prices, draw_graph
from weather_sync.weather_sync import getWeather
from image_conversion.img_to_bytearray import convert
from date_sync import update_date
import socket
from os.path import getsize, exists
from os import SEEK_END
from time import sleep
from pathlib import Path
import threading as th

fileDir = Path(__file__).parent.resolve()

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
        # resp = s.recv(BUFFER_SIZE)
    # print(f'Server response: {resp!r}')
    s.close()

def updateNformat(full_update=False):
    # execute methods to get data 
    datestr = update_date()
    calendarEvents = getEvents()
    eventstr = formatEvents(calendarEvents)
    info = [datestr]
    if full_update:
        weatherstr = getWeather()
        update_prices()
        draw_graph()
        info.append(weatherstr)
    else:
        with open(f'{fileDir}/formattedData.txt', 'r') as f:
            c = f.readlines()
            weatherstr = ''.join(c[2:7])
            info.append(weatherstr[:-1])
    info.append(eventstr)
    # clear data from file
    open(f'{fileDir}/formattedData.txt', 'w').truncate(0)
    # write data to text file
    for str in info:
        with open(f'{fileDir}/formattedData.txt', 'a') as f:
            f.write(f'{str}\n<HLINE>\n')
    # delete last newline
    with open(f'{fileDir}/formattedData.txt', 'rb+') as f:
        f.seek(-1, SEEK_END)
        f.truncate()


def main():
    if exists(f'{fileDir}/count.txt'):
        with open(f'{fileDir}/count.txt', 'r') as f:
            count = int(f.read())%30
        with open(f'{fileDir}/count.txt', 'w') as f:
            f.truncate(0)
            f.write(f'{(count+1)}')
    else:
        with open(f'{fileDir}/count.txt', 'w') as f:
            f.write('0')
            count = 0
    if count == 0:
        full_update = True
    else:
        full_update = False        
    updateNformat(full_update=full_update)
    # send data to pico
    for i in range(10):
        try:
            send(f'{fileDir}/formattedData.txt')
            break
        except ConnectionRefusedError as error:
            print(error)
            sleep(1)
            if i == 9:
                print('bruh moment')

    sleep(5)

    # convert generated gas prices graph to bytes and send it to the pico
    if full_update:
        convert(f'{fileDir}/gas_station_display/e5.png')
    for i in range(10):
        try:
            send(f'{fileDir}/image_conversion/out')
            break
        except ConnectionRefusedError as error:
            print(error)
            sleep(1)
            if i == 9:
                print('bruh moment 2')


if __name__ == '__main__':
    # import argparse
    # parser = argparse.ArgumentParser(description='Format and send dashboard data to PicoW.')
    # parser.add_argument('--full_update', action='store_true')
    # args = parser.parse_args()
    
    class RepeatTimer(th.Timer):  
        def run(self):  
            while not self.finished.wait(self.interval):  
                self.function(*self.args,**self.kwargs)
    timer = RepeatTimer(60, main)
    timer.start()
