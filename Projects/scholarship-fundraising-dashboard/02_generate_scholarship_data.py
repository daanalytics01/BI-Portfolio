"""
02_generate_scholarship_data.py

Genera un dataset SINTÉTICO (no son datos reales de ninguna institución)
que simula un programa de becas universitarias financiado por donaciones
corporativas dolarizadas, replicando la lógica de negocio típica de estos
programas:

- Las donaciones se miden en USD.
- El "arancel" (costo de la beca) es un DIVISOR, nunca se suma entre sí.
- Existen 3 estados de reconocimiento: comprometido -> reconocido -> devengado.
- La medida objetivo es: devengado + reconocido acumulado.
- Hay 7 tipos de producto/beca.
- Se define una meta (target) anual en USD por "ejercicio" (año fiscal
  no calendario, ej. marzo a febrero).

Salida:
  data/donantes.csv
  data/donaciones.csv
  data/becas.csv
"""

import random
import csv
from datetime import date, timedelta

random.seed(42)

# ---- Catálogos ----
TIPOS_PRODUCTO = [
    "Beca Nominada",
    "Beca Mérito Académico",
    "Beca Necesidad Económica",
    "Beca Convenio Corporativo",
    "Beca Investigación",
    "Beca Deportiva",
    "Beca Comunidad",
]

SECTORES = ["Tecnología", "Banca", "Energía", "Consumo Masivo", "Industria", "Agro"]

NOMBRES_DONANTES = [
    "Grupo Andes SA", "TecnoSur Argentina", "Banco Meridiano", "Energía Patagónica",
    "Consumo Norte SA", "Industrias del Plata", "AgroCampo SA", "Fundación Horizonte",
    "Vertex Software", "Banco Austral", "Grupo Litoral", "Comercial del Sur",
    "Minera Cuyo", "Alimentos Pampa", "Constructora Río", "Textil Nordeste",
    "Farma Andina", "Logística Central", "Retail Provincia", "Consultora Delta",
]

# Ejercicio fiscal: marzo 2024 a febrero 2026 (2 ejercicios completos)
FECHA_INICIO = date(2024, 3, 1)
FECHA_FIN = date(2026, 2, 28)

ESTADOS = ["comprometido", "reconocido", "devengado"]
# Distribución de estados: la mayoría de donaciones viejas ya están devengadas
def estado_segun_antiguedad(fecha_donacion: date) -> str:
    dias = (FECHA_FIN - fecha_donacion).days
    if dias > 300:
        return random.choices(ESTADOS, weights=[0.05, 0.15, 0.80])[0]
    elif dias > 120:
        return random.choices(ESTADOS, weights=[0.15, 0.35, 0.50])[0]
    else:
        return random.choices(ESTADOS, weights=[0.50, 0.35, 0.15])[0]

def ejercicio_de(fecha_: date) -> str:
    # Ejercicio: marzo a febrero. Ej: fecha en marzo 2024 -> "Ejercicio 2024-2025"
    anio_inicio = fecha_.year if fecha_.month >= 3 else fecha_.year - 1
    return f"Ejercicio {anio_inicio}-{anio_inicio + 1}"

# ---- 1) Donantes ----
donantes = []
for i, nombre in enumerate(NOMBRES_DONANTES, start=1):
    donantes.append({
        "donante_id": i,
        "nombre": nombre,
        "sector": random.choice(SECTORES),
        "pais": "Argentina",
    })

# ---- 2) Donaciones ----
donaciones = []
donacion_id = 1
current = FECHA_INICIO
while current <= FECHA_FIN:
    # entre 2 y 6 donaciones por mes
    n_donaciones_mes = random.randint(2, 6)
    for _ in range(n_donaciones_mes):
        donante = random.choice(donantes)
        dia = random.randint(1, 27)
        fecha_donacion = date(current.year, current.month, dia)
        monto_usd = round(random.uniform(2000, 25000), 2)
        tipo_producto = random.choice(TIPOS_PRODUCTO)
        estado = estado_segun_antiguedad(fecha_donacion)
        donaciones.append({
            "donacion_id": donacion_id,
            "donante_id": donante["donante_id"],
            "fecha": fecha_donacion.isoformat(),
            "ejercicio": ejercicio_de(fecha_donacion),
            "monto_usd": monto_usd,
            "tipo_producto": tipo_producto,
            "estado": estado,
        })
        donacion_id += 1
    # avanzar al próximo mes
    if current.month == 12:
        current = date(current.year + 1, 1, 1)
    else:
        current = date(current.year, current.month + 1, 1)

# ---- 3) Becas (vinculadas a donaciones, con arancel USD) ----
becas = []
beca_id = 1
for d in donaciones:
    # cada donación financia entre 1 y 3 becas
    n_becas = random.randint(1, 3)
    for _ in range(n_becas):
        arancel_usd = round(random.uniform(1500, 6000), 2)
        becas.append({
            "beca_id": beca_id,
            "donacion_id": d["donacion_id"],
            "tipo_producto": d["tipo_producto"],
            "arancel_usd": arancel_usd,
            "ejercicio": d["ejercicio"],
        })
        beca_id += 1

# ---- Guardar CSVs ----
with open("../data/donantes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=donantes[0].keys())
    w.writeheader()
    w.writerows(donantes)

with open("../data/donaciones.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=donaciones[0].keys())
    w.writeheader()
    w.writerows(donaciones)

with open("../data/becas.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=becas[0].keys())
    w.writeheader()
    w.writerows(becas)

print(f"Donantes: {len(donantes)}")
print(f"Donaciones: {len(donaciones)}")
print(f"Becas: {len(becas)}")
