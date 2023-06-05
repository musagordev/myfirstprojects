from django.db import models
import urllib.request, urllib.parse, urllib.error
import sqlite3
import json
import ssl
import codecs

# Create your models here.

class Load (models.Model):
    api_key = False
    if api_key is False:
        api_key = 42
        serviceurl = "http://py4e-data.dr-chuck.net/json?"
    else :
        serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

    conn = sqlite3.connect('geodata.sqlite')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    fh = """Teker Suite
Altintas Group
Ilbeyi Konaklama
Imperium Konaklama
Aria Plus Konaklama
Boz Suit
Palmiye Gold
Mersin Kent Konaklama
Altintas Konaklama"""
    count = 0
    for line in fh:
        if count > 200 :
            break
        address = line.strip()
        cur.execute("SELECT geodata FROM Locations WHERE address= ?",
            (memoryview(address.encode()), ))
        try:
            data = cur.fetchone()[0]
            continue
        except:
            pass
        parms = dict()
        parms["address"] = address
        if api_key is not False: parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        count = count + 1
        try:
            js = json.loads(data)
        except:
            continue
        if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
            break
        cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
        conn.commit()

class Dumb (models.Model):
    conn = sqlite3.connect('geodata.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Locations')
    fhand = codecs.open('loc.js', 'w', "utf-8")
    fhand.write("myData = [\n")
    count = 0
    for row in cur :
        data = str(row[1].decode())
        try: js = json.loads(str(data))
        except: continue
        if not('status' in js and js['status'] == 'OK') : continue
        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        if lat == 0 or lng == 0 : continue
        where = js['results'][0]['formatted_address']
        try :
            count = count + 1
            if count > 1 : fhand.write(",\n")
            output = "["+str(lat)+","+str(lng)+", '"+where+"']"
            fhand.write(output)
        except:
            continue
    fhand.write("\n];\n")
    cur.close()
    fhand.close()


