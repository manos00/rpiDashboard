#!/bin/env python3
import json
import requests
import matplotlib.pyplot as plt
import sqlite3
import datetime


TANKERKOENIG_API_KEY = open('tankerkoenigapi.key' ,'r').read()

with open('tankstellen.json', 'r') as t:
    j = t.read()
    tankstellen = json.loads(j)
    t.close()

conn = sqlite3.connect('sprit.db')
c = conn.cursor()

try:
    c.execute("""CREATE TABLE jet
    (date int,
    e5 real,
    e10 real,
    diesel real
    )""")
    conn.commit()
except sqlite3.OperationalError:
    print('Skipping creating table...')

dt = datetime.datetime.now().timestamp()

# loop through gas stations
for tankstelle in tankstellen:
    brand = tankstelle.get('brand')
    TANKSTELLEN_ID = tankstelle.get('id')
    # make api request
    REQ_URL = f'https://creativecommons.tankerkoenig.de/json/detail.php?id={TANKSTELLEN_ID}&apikey={TANKERKOENIG_API_KEY}'
    data = requests.get(REQ_URL)
    # read data with json module
    j = data.json()
    # get prices from json data and write to database
    e5 = j.get('station').get('e5')
    e10 = j.get('station').get('e10')
    diesel = j.get('station').get('diesel')
    c.execute("INSERT INTO jet VALUES (? ,?, ?, ?)", (dt, e5, e10, diesel))
    conn.commit() # commit changes to the db
    break

stamps = []
fig, ax = plt.subplots(constrained_layout=True)
ax.set_title('E5 Preise JET Bendorf')
    # if :
    # now = now.strftime('%B %Y')
    # else:
    

 #, for i, tankstelle in enumerate(['JET', 'bft', 'ARAL']):
prices = []
c.execute("SELECT date, e5 FROM jet")
entries = c.fetchall()
for entry in entries:
    stamps.append(entry[0])
    prices.append(entry[1])
ax.plot(stamps, prices) #, color=f'{int(i)/3}', **{'marker': 'x'}

conn.close()

ax.set_xticks([stamps[0], stamps[-1]])
ax.set_xticklabels([datetime.datetime.fromtimestamp(stamps[0]).strftime('%B %Y'), datetime.datetime.fromtimestamp(stamps[-1]).strftime('%B %Y')])
plt.gcf().set_size_inches(2.8, 2)
plt.margins(0,0)
plt.savefig('e5.png', orientation='landscape', bbox_inches='tight', pad_inches=0.0)