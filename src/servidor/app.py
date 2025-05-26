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
def datos():
    obj = {}
    # Tiempo actual
    q1 = "select a.id, a.nombre, b.tiempo_tipo, b.tiempo_icono, b.temperatura, b.sensacion, b.temp_min, b.temp_max, b.humedad, b.dato_tiempo, b.alba, b.ocaso from ciudad as a inner join tiempo as b on a.id=b.ciudad"
    cur.execute(q1)
    res1 = cur.fetchall()
    for c1 in res1:
        obj[str(c1[0])] = {
            "nombre": c1[1],
            "tiempo_tipo": c1[2],
            "tiempo_icono": c1[3],
            "temperatura": c1[4],
            "sensacion": c1[5],
            "temp_min": c1[6],
            "temp_max": c1[7],
            "humedad": c1[8],
            "dato_tiempo": c1[9],
            "alba": c1[10],
            "ocaso": c1[11],
            "pronosticos": {}
        }
    # Pronósticos
    q2 = "select * from pronostico"
    cur.execute(q2)
    res2 = cur.fetchall()
    for c2 in res2:
        obj[str(c1[0])]["pronosticos"][str(c2[2])] = {
            "tiempo_tipo": c2[3],
            "tiempo_icono": c2[4],
            "temperatura": c2[5],
            "pop": c2[6]
        }
    return obj

@app.route("/actualizar")
def actualizar():
    # Limpiar
    cur.execute("delete from pronostico")
    con.commit()
    cur.execute("select * from ciudad")
    res = cur.fetchall()
    for c in res:
        # Tiempo actual
        r1 = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+c[2]+"&lon="+c[3]+"&appid="+os.environ["OWM_TOKEN"])
        j1 = r1.json()
        q1 = "update tiempo set tiempo_tipo="+j1["weather"][0]["id"]+", tiempo_icono='"+j1["weather"][0]["icon"]+"', temperatura="+int((j1["main"]["temp"]-273.15)*100)+", sensacion="+int((j1["main"]["feels_like"]-273.15)*100)+", temp_min="+int((j1["main"]["temp_min"]-273.15)*100)+", temp_max="+int((j1["main"]["temp_max"]-273.15)*100)+", humedad="+int(j1["main"]["humidity"]*100)+", dato_tiempo="+j1["dt"]+", alba="+j["sys"]["sunrise"]+", ocaso="+j1["sys"]["sunset"]+" where ciudad = "+c[0]
        print(q1)
        cur.execute(q1)
        # Pronósticos
        r2 = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat="+c[2]+"&lon="+c[3]+"&appid="+os.environ["OWM_TOKEN"])
        j2 = r2.json()
        for l in j2["list"]:
            q2 = "insert into pronostico(ciudad, dato_tiempo, tiempo_tipo, tiempo_icono, temperatura, pop) values ("+c[0]+","+l["dt"]+","+l["weather"][0]["id"]+",'"+l["weather"][0]["icon"]+"',"+int((l["main"]["temp"]-273.15)*100)+","+int(l["pop"]*100)+")"
            print(q2)
            cur.execute(q2)
        con.commit()
    return "OK"
