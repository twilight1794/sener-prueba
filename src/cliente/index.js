function gen_otra_ciudad(tipo, icono, nombre, temp){
    let a = document.createElement("article");
    a.className = window.iconos[icono];
    let cd = document.createElement("div");
    cd.textContent = nombre;
    a.appendChild(cd);
    let cont = document.createElement("div");
    let tmp = document.createElement("div");
    tmp.className = "tmp";
    tmp.textContent = (temp/1000).toString()+"°C";
    cont.appendChild(tmp);
    let dsc = document.createElement("div");
    dsc.className = "dsc";
    dsc.textContent = window.codigos[tipo.toString()][0];
    cont.appendChild(dsc);
    a.appendChild(cont);
    return a;
}

function cp(nombre){
    let obj = null;
    for (let c of Object.values(window.data)){
        if (c.nombre == nombre) {
            obj = c;
        }
    }
    if (obj){
        document.querySelector("h1").textContent = obj.nombre;
        document.getElementById("fecha").textContent = new Date(obj.dato_tiempo).toLocaleDateString('es', { weekday:"long", year:"numeric", month:"short", day:"numeric", hour:"2-digit", minute: "2-digit"});
        document.getElementById("temps").className = window.iconos[obj.tiempo_icono];
        document.getElementById("temp").textContent = (obj.temperatura/1000).toFixed(1)+"°C";
        document.getElementById("max").textContent = (obj.temp_max/1000).toFixed(1)+"°C";
        document.getElementById("min").textContent = (obj.temp_min/1000).toFixed(1)+"°C";
        document.getElementById("msj").textContent = window.codigos[obj.tiempo_tipo][(window.codigos[obj.tiempo_tipo].length == 1)?0:1];
        document.getElementById("hume").textContent = (obj.humedad/1000).toString()+"%";
        document.getElementById("sensa").textContent = (obj.sensacion/1000).toFixed(1)+"°C";
        let fecha_now = new Date().getHours();
        document.getElementById("horas").dataset.modo = (fecha_now<6 || fecha_now>18)?"noche":"dia";
        let alba = new Date(obj.alba);
        console.log(alba);
        document.getElementById("alba").textContent = alba.getHours().toString().padStart(2,"0")+":"+alba.getMinutes().toString().padStart(2,"0");
        let ocaso = new Date(obj.ocaso);
        document.getElementById("ocaso").textContent = ocaso.getHours().toString().padStart(2,"0")+":"+ocaso.getMinutes().toString().padStart(2,"0");
        let pronos = Object.keys(obj.pronosticos).slice(0,8);
        console.log(pronos);
        let tarjes = document.getElementsByClassName("tarje");
        console.log(tarjes);
        for (let i=0; i<8; i++){
            let hora_corr = new Date(pronos[i]);
            tarjes[i].className = "tarje "+window.iconos[obj.pronosticos[pronos[i]].tiempo_icono];
            tarjes[i].children[0].textContent = hora_corr.getHours().toString().padStart(2,"0")+":"+hora_corr.getMinutes().toString().padStart(2,"0");
            tarjes[i].children[1].textContent = (obj.pronosticos[pronos[i]].temperatura/1000).toFixed(1)+"°C";
            tarjes[i].children[2].textContent = (obj.pronosticos[pronos[i]].pop/10).toFixed(0)+"%";
        }
    } else {
        console.error(`${nombre} no encontrado`);
    }
}

document.addEventListener("DOMContentLoaded", (event) => {
    fetch("http://localhost:5000/datos")
    .then((response) => {
        if (!response.ok) {
            console.log(response.status);
            throw new Error(`HTTP error, status = ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        // Otras ciudades
        window.data = data;
        let aside = document.querySelector("aside");
        for (let c of Object.values(data)){
            let item = gen_otra_ciudad(c.tiempo_tipo, c.tiempo_icono, c.nombre, c.temperatura);
            item.addEventListener("click", (e) => cp(e.target.children[0].textContent) );
            aside.appendChild(item);
        }
        // Ciudad principal
        cp(Object.values(data)[0].nombre);
    })
    .catch((error) => {
        console.log(error);
        alert("Error al consultar los datos :(");
    });
});

window.codigos = {
    "200": ["Tormenta", "Tormenta con lluvia ligera"],
    "201": ["Tormenta", "Tormenta con lluvia"],
    "202": ["Tormenta", "Tormenta con lluvia abundante"],
    "210": ["Tormenta", "Tormenta ligera"],
    "211": ["Tormenta"],
    "212": ["Tormenta", "Tormenta abundante"],
    "221": ["Tormenta", "Tormenta violenta"],
    "230": ["Tormenta", "Tormenta con llovizna ligera"],
    "231": ["Tormenta", "Tormenta con llovizna"],
    "232": ["Tormenta", "Tormenta con llovizna abundante"],
    "300": ["Llovizna", "Llovizna ligera"],
    "301": ["Llovizna"],
    "302": ["Llovizna", "Llovizna abundante"],
    "310": ["Llovizna", "Light intensity drizzle rain"],
    "311": ["Llovizna", "Drizzle rain"],
    "312": ["Llovizna", "Heavy intensity drizzle rain"],
    "313": ["Llovizna", "Shower rain and drizzle"],
    "314": ["Llovizna", "Heavy shower rain and drizzle"],
    "321": ["Llovizna", "Shower drizzle"],
    "500": ["Lluvia", "Lluvia ligera"],
    "501": ["Lluvia", "Lluvia moderada"],
    "502": ["Lluvia", "Lluvia intensa"],
    "503": ["Lluvia", "Lluvia muy intensa"],
    "504": ["Lluvia", "Lluvia extrema"],
    "511": ["Lluvia", "Lluvia helada"],
    "520": ["Lluvia", "Chubasco ligero"],
    "521": ["Lluvia", "Chubasco"],
    "522": ["Lluvia", "Chubasco intenso"],
    "531": ["Lluvia", "Chubasco violento"],
    "600": ["Nieve", "Nevada ligera"],
    "601": ["Nieve", "Nevada"],
    "602": ["Nieve", "Nevada abundante"],
    "611": ["Nieve", "Sleet"],
    "612": ["Nieve", "Light shower sleet"],
    "613": ["Nieve", "Shower sleet"],
    "615": ["Nieve", "Light rain and snow"],
    "616": ["Nieve", "Rain and snow"],
    "620": ["Nieve", "Light shower snow"],
    "621": ["Nieve", "Shower snow"],
    "622": ["Nieve", "Heavy shower snow"],
    "701": ["Neblina"],
    "711": ["Humo"],
    "721": ["Bruma"],
    "731": ["Tolvanera"],
    "741": ["Niebla"],
    "751": ["Arena"],
    "761": ["Polvareda"],
    "762": ["Cenizas"],
    "771": ["Borrasca"],
    "781": ["Tornado"],
    "800": ["Despejado"],
    "801": ["Nublado", "Pocas nubes"],
    "802": ["Nublado", "Algunas nubes"],
    "803": ["Nublado", "Muchas nubes"],
    "804": ["Nublado", "Muchísimas nubes"]
}

window.iconos = {
    "01d": "clear-sky-d",
    "01n": "clear-sky-n",
    "02d": "few-clouds-d",
    "02n": "few-clouds-n",
    "03d": "scattered-clouds-d",
    "03n": "scattered-clouds-n",
    "04d": "broken-clouds-d",
    "04n": "broken-clouds-n",
    "09d": "shower-rain-d",
    "09n": "shower-rain-n",
    "10d": "rain-d",
    "10n": "rain-n",
    "11d": "thunderstorm-d",
    "11n": "thunderstorm-n",
    "13d": "snow-d",
    "13n": "snow-n",
    "50d": "mist-d",
    "50n": "mist-n",
}
