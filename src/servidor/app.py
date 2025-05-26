from flask import Flask, abort

import mariadb
import os
import requests
import sys

app = Flask(__name__)
try:
    con = mariadb.connect(
      user="root",
      password="contra",
      host="db",
      port=3306,
      database="sener"
    )
    cur = con.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

@app.route("/datos")
def fun():
    return "<p>Hello, World!</p>"

@app.route("/actualizar")
def fun():
    cur.execute("select * from ciudad")
    res = cur.fetchall()
    for c in res:
        try:
            r = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+res[2]+"&lon="+res[3]+"&appid="+os.environ["OWM_TOKEN"])
            j = r.json()
            q = "update tiempo set tiempo_tipo="+j["weather"][0]["id"]+", tiempo_icono='"+j["weather"][0]["icon"]+"', temperatura="+int((j["main"]["temp"]-273.15)*100)+", sensacion="+int((j["main"]["feels_like"]-273.15)*100)+", temp_min="+int((j["main"]["temp_min"]-273.15)*100)+", temp_max="+int((j["main"]["temp_max"]-273.15)*100)+", humedad="+int(j["main"]["humidity"]*100)+", dato_tiempo="+j["dt"]+", alba="+j["sys"]["sunrise"]+", ocaso="+j["sys"]["sunset"]+" where ciudad = "+res[0]
            print(q)
            cur.execute(q)
            con.commit()
        except Exception as e:
            print(e)
            abort(500)
        
