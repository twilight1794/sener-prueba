CREATE IF NOT EXISTS meta (
  ultima_act TIMESTAMP not null
);

CREATE IF NOT EXISTS ciudad (
  id int auto_increment,
  nombre varchar(50) not null,
  latitud int not null,
  longitud int not null,
  tiempo_tipo varchar(50),
  tiempo_desc varchar(100),
  temperatura int,
  sensacion int,
  temp_min int,
  temp_max int,
  humedad int,
  dato_tiempo timestamp,
  alba timestamp,
  ocaso timestamp
  primary key (id)
);
