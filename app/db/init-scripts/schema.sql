CREATE TYPE estado_civil_t AS ENUM ('soltero', 'casado', 'conviviente', 'divorciado' , 'viudo');

CREATE TABLE paciente (
    paciente_dni TEXT NOT NULL CONSTRAINT dni_check CHECK (char_length(paciente_dni) = 8 AND paciente_dni ~ '^[0-9]+$'),
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    fecha_de_nacimiento DATE NOT NULL,
    lugar_de_nacimiento TEXT NOT NULL,
    estado_civil estado_civil_t NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL CONSTRAINT phone_check CHECK (char_length(telefono) = 9 AND telefono ~ '^[0-9]+$'),
    email TEXT NOT NULL CONSTRAINT email_check CHECK (email ~* '^\S+@\S+\.\S+$'),
    ocupacion TEXT NOT NULL,    
    lugar_trabajo_estudio TEXT NOT NULL,
    apoderado TEXT NOT NULL,
    novedades TEXT NOT NULL,
    PRIMARY KEY (paciente_dni)
);

CREATE TABLE historia_clinica_examenes_estomatologicos (
    historia_clinica_id INTEGER NOT NULL,
    maxilares BOOLEAN NOT NULL,
    vestíbulo BOOLEAN NOT NULL,
    labios BOOLEAN NOT NULL,
    encia BOOLEAN NOT NULL,
    paladar BOOLEAN NOT NULL,
    oclusión BOOLEAN NOT NULL,
    lengua BOOLEAN NOT NULL,
    atm BOOLEAN NOT NULL,
    piso_de_boca BOOLEAN NOT NULL,
    ganglios BOOLEAN NOT NULL,
    orifaringe BOOLEAN NOT NULL,
    halitosis BOOLEAN NOT NULL,
    PRIMARY KEY (historia_clinica_id)
);

CREATE TABLE historia_clinica_antecedentes_medicos (
    historia_clinica_id INTEGER NOT NULL,
    enfermedad_cardiaca BOOLEAN NOT NULL,
    enfermedad_renal BOOLEAN NOT NULL,
    vih BOOLEAN NOT NULL,
    alergias BOOLEAN NOT NULL,
    hemorragias BOOLEAN NOT NULL,
    medicado BOOLEAN NOT NULL,
    diabetes BOOLEAN NOT NULL,
    hepatitis BOOLEAN NOT NULL,
    problemas_hemorragicos BOOLEAN NOT NULL,
    presion_alta BOOLEAN NOT NULL,
    epilepsia BOOLEAN NOT NULL,
    embarazo BOOLEAN NOT NULL,
    otros TEXT NOT NULL,
    PRIMARY KEY (historia_clinica_id)
);

CREATE TABLE paciente_contraindicacion_medica (
    paciente_dni TEXT NOT NULL,
    contraindicacion_id SERIAL NOT NULL,
    descripcion TEXT NOT NULL,
    es_grave BOOLEAN NOT NULL,
    PRIMARY KEY (paciente_dni, contraindicacion_id)
);

CREATE TABLE paciente_examen_auxiliar (
    historia_clinica_id INTEGER NOT NULL,
    examen_id SERIAL NOT NULL,
    titulo TEXT NOT NULL,
    fecha DATE NOT NULL,
    PRIMARY KEY (historia_clinica_id, examen_id)
);

CREATE TABLE tratamiento (
    tratamiento_id SERIAL NOT NULL,
    en_curso BOOLEAN NOT NULL,
    observaciones TEXT NOT NULL,
    odontologo TEXT NOT NULL,
    historia_clinica_id INTEGER NOT NULL,
    PRIMARY KEY (tratamiento_id)
);

CREATE TABLE tratamiento_sesion (
    tratamiento_id INTEGER NOT NULL,
    sesion_id SERIAL NOT NULL,
    fecha DATE NOT NULL,
    descripcion TEXT NOT NULL,
    odontologo TEXT NOT NULL,
    paciente_dni TEXT NOT NULL,
    PRIMARY KEY (tratamiento_id, sesion_id)
);

CREATE TYPE tipo_odontograma_t AS ENUM ('inicial', 'tratamiento', 'evolucion');

CREATE TABLE historia_clinica_odontograma (
    historia_clinica_id INTEGER NOT NULL,
    tipo_odontograma tipo_odontograma_t NOT NULL,
    ultima_edicion DATE NOT NULL,
    PRIMARY KEY (historia_clinica_id, tipo_odontograma)
);

CREATE TABLE presupuesto (
    presupuesto_id INTEGER NOT NULL,
    paciente_dni TEXT NOT NULL,
    PRIMARY KEY (presupuesto_id)
);

CREATE TABLE presupuesto_item (
    presupuesto_id INTEGER NOT NULL,
    item_id SERIAL NOT NULL,
    descripcion TEXT NOT NULL,
    costo BIGINT NOT NULL CONSTRAINT positive_check CHECK (costo >= 0),
    es_procedimiento BOOLEAN NOT NULL,
    PRIMARY KEY (presupuesto_id, item_id)
);

CREATE TABLE paciente_pago (
    paciente_dni TEXT NOT NULL,
    pago_id SERIAL NOT NULL,
    fecha  DATE NOT NULL,
    monto BIGINT NOT NULL CONSTRAINT positive_check CHECK (monto >= 0),
    presupuesto_id INTEGER NOT NULL,
    PRIMARY KEY (paciente_dni, pago_id)
);

CREATE TABLE historia_clinica (
    historia_clinica_id SERIAL NOT NULL,
    fecha_creacion DATE NOT NULL,
    paciente_dni TEXT NOT NULL,
    PRIMARY KEY (historia_clinica_id)
);

ALTER TABLE historia_clinica_examenes_estomatologicos ADD FOREIGN KEY (historia_clinica_id) REFERENCES historia_clinica(historia_clinica_id);
ALTER TABLE historia_clinica_antecedentes_medicos ADD FOREIGN KEY (historia_clinica_id) REFERENCES historia_clinica(historia_clinica_id);
ALTER TABLE paciente_contraindicacion_medica ADD FOREIGN KEY (paciente_dni) REFERENCES paciente(paciente_dni);
ALTER TABLE paciente_examen_auxiliar ADD FOREIGN KEY (historia_clinica_id) REFERENCES historia_clinica(historia_clinica_id);
ALTER TABLE tratamiento ADD FOREIGN KEY (historia_clinica_id) REFERENCES historia_clinica(historia_clinica_id);
ALTER TABLE tratamiento_sesion ADD FOREIGN KEY (paciente_dni) REFERENCES paciente(paciente_dni);
ALTER TABLE tratamiento_sesion ADD FOREIGN KEY (tratamiento_id) REFERENCES tratamiento(tratamiento_id);
ALTER TABLE historia_clinica_odontograma ADD FOREIGN KEY (historia_clinica_id) REFERENCES historia_clinica(historia_clinica_id);
ALTER TABLE presupuesto ADD FOREIGN KEY (presupuesto_id) REFERENCES tratamiento(tratamiento_id);
ALTER TABLE presupuesto ADD FOREIGN KEY (paciente_dni) REFERENCES paciente(paciente_dni);
ALTER TABLE presupuesto_item ADD FOREIGN KEY (presupuesto_id) REFERENCES presupuesto(presupuesto_id);
ALTER TABLE paciente_pago ADD FOREIGN KEY (paciente_dni) REFERENCES paciente(paciente_dni);
ALTER TABLE paciente_pago ADD FOREIGN KEY (presupuesto_id) REFERENCES presupuesto(presupuesto_id);
ALTER TABLE historia_clinica ADD FOREIGN KEY (paciente_dni) REFERENCES paciente(paciente_dni);

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_paciente_nombres_apellidos_trgm ON Paciente USING GIST (lower(nombres || ' ' || apellidos) gist_trgm_ops);
CREATE INDEX idx_paciente_examen_auxiliar_fecha ON Paciente_examen_auxiliar (fecha);
CREATE INDEX idx_tratamiento_sesion_fecha ON Tratamiento_sesion (fecha);

CREATE OR REPLACE FUNCTION crear_odontogramas_al_insertar_historia()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO historia_clinica_odontograma (historia_clinica_id, tipo_odontograma, ultima_edicion)
  VALUES (NEW.historia_clinica_id, 'inicial', CURRENT_DATE);

  INSERT INTO historia_clinica_odontograma (historia_clinica_id, tipo_odontograma, ultima_edicion)
  VALUES (NEW.historia_clinica_id, 'tratamiento', CURRENT_DATE);

  INSERT INTO historia_clinica_odontograma (historia_clinica_id, tipo_odontograma, ultima_edicion)
  VALUES (NEW.historia_clinica_id, 'evolucion', CURRENT_DATE);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_crear_odontogramas
AFTER INSERT ON historia_clinica
FOR EACH ROW
EXECUTE FUNCTION crear_odontogramas_al_insertar_historia();
