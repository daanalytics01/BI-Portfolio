# Medidas DAX — Scholarship Fundraising Dashboard

Reglas de negocio clave a respetar en el modelo:
1. **La medida objetivo** de fundraising es `reconocido + devengado`. El estado `comprometido` es pipeline, no cuenta para el cumplimiento de meta.
2. **`arancel_usd` es un DIVISOR**, nunca se debe sumar entre becas — se usa para calcular cuántas becas equivalen a un monto, o el arancel promedio. Sumarlo directamente rompe la lógica de negocio.
3. Las comparaciones de cumplimiento de meta se hacen siempre en USD (la meta está fijada en USD, no en ARS, por la inflación).

## Medidas principales

```dax
Total Objetivo USD =
CALCULATE(
    SUM(donaciones[monto_usd]),
    donaciones[estado] IN {"reconocido", "devengado"}
)
```

```dax
Total Devengado USD =
CALCULATE(
    SUM(donaciones[monto_usd]),
    donaciones[estado] = "devengado"
)
```

```dax
Total Comprometido USD (Pipeline) =
CALCULATE(
    SUM(donaciones[monto_usd]),
    donaciones[estado] = "comprometido"
)
```

```dax
Meta Ejercicio USD =
-- Ejemplo: valor fijo por ejercicio, cargar desde una tabla de metas
-- o parametrizar como constante si el dashboard es de un solo ejercicio
SWITCH(
    SELECTEDVALUE(donaciones[ejercicio]),
    "Ejercicio 2024-2025", 400000,
    "Ejercicio 2025-2026", 480000,
    BLANK()
)
```

```dax
% Cumplimiento de Meta =
DIVIDE([Total Objetivo USD], [Meta Ejercicio USD])
```

```dax
Cantidad de Becas =
DISTINCTCOUNT(becas[beca_id])
```

```dax
Arancel Promedio USD =
AVERAGE(becas[arancel_usd])
-- NUNCA usar SUM(becas[arancel_usd]) — el arancel es un divisor por beca,
-- no una magnitud acumulable entre becas.
```

```dax
Becas Financiadas Equivalentes =
-- Cuántas "becas completas" representa el monto objetivo, usando el arancel promedio
DIVIDE([Total Objetivo USD], [Arancel Promedio USD])
```

## Sugerencia de visuales

- **KPI card**: % Cumplimiento de Meta (con meta de referencia)
- **Gráfico de columnas apiladas**: Total Objetivo USD por mes, con línea de Meta
- **Gráfico de dona**: distribución de USD por tipo de producto (7 categorías)
- **Tabla**: Top donantes por Total Objetivo USD
- **Gráfico de líneas**: evolución del tipo de cambio oficial superpuesto contra el equivalente en ARS del objetivo (para mostrar el efecto de la devaluación sobre el poder adquisitivo de las donaciones)
