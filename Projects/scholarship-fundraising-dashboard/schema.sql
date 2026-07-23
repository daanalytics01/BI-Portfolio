-- Schema del modelo de datos: Scholarship Fundraising Dashboard
-- Compatible con SQLite / PostgreSQL / SQL Server (ajustar tipos si hace falta)

CREATE TABLE donantes (
    donante_id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    sector TEXT,
    pais TEXT
);

CREATE TABLE donaciones (
    donacion_id INTEGER PRIMARY KEY,
    donante_id INTEGER REFERENCES donantes(donante_id),
    fecha DATE NOT NULL,
    ejercicio TEXT NOT NULL,
    monto_usd DECIMAL(12,2) NOT NULL,
    tipo_producto TEXT NOT NULL,
    estado TEXT CHECK (estado IN ('comprometido', 'reconocido', 'devengado'))
);

CREATE TABLE becas (
    beca_id INTEGER PRIMARY KEY,
    donacion_id INTEGER REFERENCES donaciones(donacion_id),
    tipo_producto TEXT NOT NULL,
    arancel_usd DECIMAL(12,2) NOT NULL,  -- IMPORTANTE: es un DIVISOR, nunca sumar arancel_usd entre becas
    ejercicio TEXT NOT NULL
);

CREATE TABLE tipo_cambio_oficial (
    fecha DATE PRIMARY KEY,
    usd_ars_oficial DECIMAL(10,2) NOT NULL
);
