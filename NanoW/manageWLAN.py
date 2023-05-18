import network
import time

wlan = network.WLAN(network.STA_IF)

def connectWLAN(ssid, password):
    wlan.active(True)
    wlan.connect(ssid, password)
    tries = 0
    while not wlan.isconnected() and wlan.status() >= 0 and tries <= 10:
        print('Waiting to connect...')
        time.sleep(1)
        tries+=1
    if tries == 10:
        print('Connection failed after 10 tries. Aborting.')
        exit(1)
    print(f'Successfully connected to {ssid} with ip {wlan.ifconfig()[0]}')

def disconnectWLAN():
    wlan.disconnect()

def enableWLAN():
    wlan.active(True)

def disableWLAN():
    wlan.active(False)

if __name__ == '__main__':
    ssid = 'FRITZ!Box 6490 Cable'
    password = 'FritzBoxWagner1972$!'
    connectWLAN(ssid, password)
