import PicoEPaper
import manageWLAN
from machine import Timer
from math import floor
import ntptime
import gc
import utime
import socket

ssid = 'FRITZ!Box 6490 Cable'
password = 'FritzBoxWagner1972$!'
manageWLAN.connectWLAN(ssid, password)
ntptime.host = '1.europe.pool.ntp.org'
ntptime.settime()

# def updateDate():
#     weekdays = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
#     ctime = utime.localtime(utime.time()+2*60*60)
#     datestr = "{}, {:02d}.{:02d}.{} {:02d}:{:02d}".format(weekdays.get(ctime[6]), ctime[2], ctime[1], ctime[0], ctime[3], ctime[4])
#     return datestr


def center_x(str: str):
    return 140-len(str)*8//2


def recieve():
    SERVER_HOST = "" # 192.168.178.112
    SERVER_PORT = 30123
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((SERVER_HOST, SERVER_PORT))
    except OSError as error:
        print(f"{error}")
    s.listen(10)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    print("Waiting for the client to connect... ")
    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = filename.split('/')[-1]
    print(filename)
    filesize = int(filesize)
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            # client_socket.sendall(b'Data recieved successfully.')
    client_socket.close()
    s.close()


timMin = Timer()

def update_uptime():
    with open('uptime.tmp', 'r') as f:
        stime = int(f.read())
        f.close()
    ctime = utime.time()
    dtime = (ctime-stime)//60
    uptimestr = f'Uptime: {floor(dtime/60/24)}Days {floor(dtime/60%24)}Hours {dtime%60}Minutes'
    return uptimestr


def main(*kwargs):
    # Initializing EPD
    epd = PicoEPaper.EPD_3in7()
    # Erasing EPD
    epd.image4Gray.fill(0xff)
    # Declaring height var
    y = 5

    with open('formattedData.txt', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip() == '<HLINE>':
                epd.image4Gray.hline(0, y, 280, epd.black)
                y += 8
            else:
                if i == 0:
                    x = center_x(line)
                else:
                    x = 4
                epd.image4Gray.text(line.strip(), x, y, epd.black)
                y += 16
    with open('out', 'rb') as f:
        graph = f.read()
        epd.buffer_4Gray[int(y*280/4):int(y*280/4)+len(graph)] = graph
    # Updating uptime and writing to display buffer
    epd.image4Gray.hline(0, 480-24, 280, epd.black)
    uptimestr = update_uptime()
    epd.image4Gray.text(uptimestr, center_x(uptimestr), 480-16, epd.black)
    # Displaying buffer
    epd.EPD_3IN7_4Gray_Display(epd.buffer_4Gray)
    # Sending EPD to sleep
    epd.Sleep()

def every_minute(*kwargs):
    recieve()
    utime.sleep(2)
    recieve()
    gc.collect()
    main()
    return 

# reset uptime.tmp file on reboot
with open('uptime.tmp', 'w') as f:
    t = utime.time()
    f.write(str(t))
    f.close()
# update everything on boot (timer first executes methods after the first period of time has passed)
every_minute()
# Recieve and display data every 60000 milliseconds / every minute
timMin.init(period=60_000, mode=Timer.PERIODIC, callback=every_minute)
