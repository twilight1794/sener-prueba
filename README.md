# Tablero
Este tablero muestra una serie de datos metereológicos de las 10 ciudades mexicanas con mayor población. Las ciudades son:
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
## Docker
Es requisito tener Docker instalado en el sistema, y simplemente ejecutar `docker compose up -d`. Hará todo lo necesario para preparar el entorno, que estará accesible desde [localhost:3000](http://localhost:3000/).

## Manual
### Servidor
Es necesario tener MySQL instalado y configurado, así como los puentes para poder acceder desde Python, que en sistemas de la familia Debian, se suple instalando los paquetes `libmariadb3` y `libmariadb-dev`.

Es necesario tener python instalado, así como los paquetes de Python `Flask` y `mariadb`.

Para correr la aplicación Flask, ejecutar `flask run --host=0.0.0.0` dentro del directorio `src/servidor`.

### Cliente
Nada especial, basta con ejecutar `python -m http.server` en el directorio `src/cliente`, lo que expondrá el cliente en [localhost:8000](http://localhost:8000).
