CREATE DATABASE IF NOT EXISTS sener;
USE sener;

CREATE TABLE IF NOT EXISTS meta (
  ultima_act TIMESTAMP not null
);

CREATE TABLE IF NOT EXISTS ciudad (
  id int auto_increment,
  nombre varchar(50) not null,
  latitud int not null,
  longitud int not null,
  primary key(id)
);

CREATE TABLE IF NOT EXISTS tiempo (
  id int auto_increment,
  ciudad int not null,
  tiempo_tipo varchar(50),
  tiempo_desc varchar(100),
  temperatura int,
  sensacion int,
  temp_min int,
  temp_max int,
  humedad int,
  dato_tiempo timestamp,
  alba timestamp,
  ocaso timestamp,
  primary key (id)
);

INSERT INTO ciudad (nombre, latitud, longitud) VALUES
  ('CDMX', 19419, -99145),
  ('Monterrey', 25684, -100318),
  ('Guadalajara', 20676, -103347),
  ('Puebla', 19051, -98218),
  ('Toluca', 19292, -99654),
  ('Tijuana', 32536, -117037),
  ('León', 21122, -101683),
  ('Queretaro', 20588, -100388),
  ('Ciudad Juárez', 31668, -106420),
  ('Torreón', 25167, -103266);
