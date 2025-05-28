from flask import Flask, abort, Response

import json
import mariadb
import os
import requests
import sys

app = Flask(__name__)
def maria_cur():
    con = mariadb.connect(
        user="root",
        password="contra",
        host="db",
        port=3306,
        database="sener"
    )
    return con

@app.route("/datos")
def datos():
    con = maria_cur()
    cur = con.cursor()
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
        obj[str(c2[1])]["pronosticos"][str(c2[2])] = {
            "tiempo_tipo": c2[3],
            "tiempo_icono": c2[4],
            "temperatura": c2[5],
            "pop": c2[6]
        }
    con.close()
    resp = Response(json.dumps(obj, default=str))
    resp.headers['Access-Control-Allow-Origin']  = "*"
    return resp

@app.route("/actualizar")
def actualizar():
    con = maria_cur()
    cur = con.cursor()
    # Limpiar
    cur.execute("delete from pronostico")
    con.commit()
    cur.execute("select * from ciudad")
    res = cur.fetchall()
    for c in res:
        # Tiempo actual
        r1 = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+str(c[2]/1000)+"&lon="+str(c[3]/1000)+"&appid="+os.environ["OWM_TOKEN"])
        j1 = r1.json()
        print(j1)
        q1 = "update tiempo set tiempo_tipo="+str(j1["weather"][0]["id"])+", tiempo_icono='"+j1["weather"][0]["icon"]+"', temperatura="+str(int((j1["main"]["temp"]-273.15)*1000))+", sensacion="+str(int((j1["main"]["feels_like"]-273.15)*1000))+", temp_min="+str(int((j1["main"]["temp_min"]-273.15)*1000))+", temp_max="+str(int((j1["main"]["temp_max"]-273.15)*1000))+", humedad="+str(int(j1["main"]["humidity"]*1000))+", dato_tiempo=FROM_UNIXTIME("+str(j1["dt"])+"), alba=FROM_UNIXTIME("+str(j1["sys"]["sunrise"])+"), ocaso=FROM_UNIXTIME("+str(j1["sys"]["sunset"])+") where ciudad = "+str(c[0])
        print(q1)
        cur.execute(q1)
        # Pronósticos
        r2 = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat="+str(c[2]/1000)+"&lon="+str(c[3]/1000)+"&appid="+os.environ["OWM_TOKEN"])
        j2 = r2.json()
        print(j2)
        for l in j2["list"]:
            q2 = "insert into pronostico(ciudad, dato_tiempo, tiempo_tipo, tiempo_icono, temperatura, pop) values ("+str(c[0])+",FROM_UNIXTIME("+str(l["dt"])+"),"+str(l["weather"][0]["id"])+",'"+l["weather"][0]["icon"]+"',"+str(int((l["main"]["temp"]-273.15)*1000))+","+str(int(l["pop"]*1000))+")"
            print(q2)
            cur.execute(q2)
        con.commit()
    con.close()
    return "OK"
