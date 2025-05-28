# Tablero
Este tablero muestra una serie de datos metereológicos de las 10 ciudades mexicanas con mayor población, y un pronóstico para las siguientes 24 horas. Las ciudades son:
- Ciudad de México
- Monterrey
- Guadalajara
- Puebla
- Tijuana
- Toluca
- León
- Querétaro
- Ciudad Juárez
- Torreón

# Instalación
Antes de ejecutar el programa, es necesario establecer en el sistema la variable de entorno `OWM_TOKEN` con el token obtenido desde OpenWeatherMap; y después de instalar todo, visitar la dirección [/actualizar](http://localhost:3001/actualizar) (hay qué verificar el puerto usado para exponer al cliente), para cargar datos nuevos desde OpenWeatherMap.

## Docker
Es requisito tener Docker instalado en el sistema. Simplemente ejecutar `docker compose up -d`. Hará todo lo necesario para preparar el entorno, que estará accesible desde [localhost:3001](http://localhost:3001/).

## Manual
### Servidor
Es necesario tener MySQL instalado y configurado, así como los puentes para poder acceder desde Python, que en sistemas de la familia Debian, se suple instalando los paquetes `libmariadb3` y `libmariadb-dev`.

Es necesario tener python instalado, así como los paquetes de Python `Flask`, `mariadb` y `requests`.

Para correr la aplicación Flask, ejecutar `flask run --host=0.0.0.0` dentro del directorio `src/servidor`.

### Cliente
Nada especial, basta con ejecutar `python -m http.server` en el directorio `src/cliente`, lo que expondrá el cliente en [localhost:8000](http://localhost:8000).

# API
La API expuesta por el servidor simplemente tiene dos endpoints, ambos sin parámetros y accesibles por el método GET:
* `/actualizar`: actualiza todos los datos disponibles en la API de OpenWeatherMap. En total, se realizan 20 llamadas al sistema, dos por cada ciudad, por lo que hay qué tener cuidado de no exceder el límite de llamadas establecido. Si todo sale bien, devolverá el texto OK.
* `/datos`: devuelve un JSON con todos los datos disponibles en la base de datos.
