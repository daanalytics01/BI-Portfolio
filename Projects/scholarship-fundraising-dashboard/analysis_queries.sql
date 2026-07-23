-- ============================================================
-- Queries de análisis: Scholarship Fundraising Dashboard
-- ============================================================

-- 1) Medida objetivo del ejercicio: reconocido + devengado acumulado (USD)
--    (comprometido NO cuenta para el objetivo, solo es un pipeline)
SELECT
    ejercicio,
    SUM(CASE WHEN estado IN ('reconocido', 'devengado') THEN monto_usd ELSE 0 END) AS total_objetivo_usd,
    SUM(CASE WHEN estado = 'devengado' THEN monto_usd ELSE 0 END) AS total_devengado_usd,
    SUM(CASE WHEN estado = 'reconocido' THEN monto_usd ELSE 0 END) AS total_reconocido_usd,
    SUM(CASE WHEN estado = 'comprometido' THEN monto_usd ELSE 0 END) AS total_comprometido_usd
FROM donaciones
GROUP BY ejercicio
ORDER BY ejercicio;

-- 2) Cantidad de becas otorgadas por ejercicio y tipo de producto
--    (arancel_usd es un DIVISOR: se promedia, nunca se suma entre becas)
SELECT
    b.ejercicio,
    b.tipo_producto,
    COUNT(*) AS cantidad_becas,
    ROUND(AVG(b.arancel_usd), 2) AS arancel_promedio_usd
FROM becas b
GROUP BY b.ejercicio, b.tipo_producto
ORDER BY b.ejercicio, b.tipo_producto;

-- 3) Avance de fundraising mes a mes vs. meta (para gráfico de tendencia)
SELECT
    strftime('%Y-%m', fecha) AS mes,
    SUM(CASE WHEN estado IN ('reconocido', 'devengado') THEN monto_usd ELSE 0 END) AS objetivo_mes_usd
FROM donaciones
GROUP BY mes
ORDER BY mes;

-- 4) Top donantes por monto reconocido+devengado acumulado
SELECT
    d.nombre,
    d.sector,
    SUM(CASE WHEN dn.estado IN ('reconocido', 'devengado') THEN dn.monto_usd ELSE 0 END) AS total_objetivo_usd,
    COUNT(DISTINCT dn.donacion_id) AS cantidad_donaciones
FROM donantes d
JOIN donaciones dn ON dn.donante_id = d.donante_id
GROUP BY d.donante_id, d.nombre, d.sector
ORDER BY total_objetivo_usd DESC
LIMIT 10;

-- 5) Equivalente en ARS del monto objetivo, usando el tipo de cambio oficial
--    del mes de la donación (join por mes, no por día exacto, para simplificar)
SELECT
    strftime('%Y-%m', dn.fecha) AS mes,
    SUM(CASE WHEN dn.estado IN ('reconocido', 'devengado') THEN dn.monto_usd ELSE 0 END) AS objetivo_usd,
    AVG(tc.usd_ars_oficial) AS tipo_cambio_promedio_mes,
    SUM(CASE WHEN dn.estado IN ('reconocido', 'devengado') THEN dn.monto_usd ELSE 0 END) * AVG(tc.usd_ars_oficial) AS objetivo_ars_estimado
FROM donaciones dn
LEFT JOIN tipo_cambio_oficial tc
    ON strftime('%Y-%m', tc.fecha) = strftime('%Y-%m', dn.fecha)
GROUP BY mes
ORDER BY mes;

-- 6) Distribución por sector de donante (para gráfico de torta / barras)
SELECT
    d.sector,
    ROUND(SUM(CASE WHEN dn.estado IN ('reconocido', 'devengado') THEN dn.monto_usd ELSE 0 END), 2) AS total_objetivo_usd,
    COUNT(DISTINCT d.donante_id) AS cantidad_donantes
FROM donantes d
JOIN donaciones dn ON dn.donante_id = d.donante_id
GROUP BY d.sector
ORDER BY total_objetivo_usd DESC;
