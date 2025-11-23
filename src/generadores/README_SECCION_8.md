# Sección 8 - Ejecución Presupuestal

## Descripción

La Sección 8 genera el reporte de ejecución presupuestal del contrato SCJ-1809-2024, incluyendo:
- Ejecución mensual por categorías
- Consolidado presupuestal
- Compras y uso de la bolsa de repuestos
- Variaciones presupuestales y justificaciones
- Observaciones y recomendaciones

## Archivos

- `src/generadores/seccion_8_presupuesto.py`: Generador principal
- `templates/seccion_8_presupuesto.docx`: Template Word con placeholders Jinja2
- `data/fuentes/ejecucion_presupuestal_demo.csv`: CSV de ejemplo con datos dummy

## Uso

### Generación básica

```bash
python main.py --anio 2025 --mes 9
```

### Fuentes de datos

El generador busca datos en el siguiente orden:

1. **CSV**: `data/fuentes/ejecucion_presupuestal.csv`
   - Columnas esperadas: `categoria`, `presupuesto`, `ejecutado`, `mes`, etc.

2. **JSON**: `data/fuentes/ejecucion_presupuestal_{mes}_{anio}.json`
   - Estructura esperada:
     ```json
     {
       "ejecucion_mensual": [...],
       "consolidado": [...],
       "compras_bolsa": [...],
       "variaciones": [...]
     }
     ```

3. **Datos dummy**: Si no encuentra fuentes, genera automáticamente datos de prueba

### Estructura de datos

#### Ejecución mensual
```python
{
    "categoria": "Mano de obra",
    "presupuesto": 200000000,
    "ejecutado": 180000000,
    "porcentaje_ejecucion": 90.0,
    "presupuesto_formato": "$200.000.000",
    "ejecutado_formato": "$180.000.000"
}
```

#### Consolidado
```python
{
    "mes": "Septiembre 2025",
    "presupuesto_mes": 280000000,
    "ejecutado_mes": 270000000,
    "porcentaje_ejecucion": 96.43,
    "presupuesto_mes_formato": "$280.000.000",
    "ejecutado_mes_formato": "$270.000.000"
}
```

#### Compras bolsa
```python
{
    "item": "Cámara Domo",
    "cantidad": 10,
    "valor_unitario": 1200000,
    "valor_total": 12000000,
    "fecha": "2025-09-05",
    "valor_unitario_formato": "$1.200.000",
    "valor_total_formato": "$12.000.000"
}
```

#### Variaciones
```python
{
    "categoria": "Repuestos",
    "variacion": -16.0,
    "explicacion": "Ajuste por compras centralizadas y descuentos por volumen"
}
```

## Características

- **Cálculo automático de porcentajes**: Calcula % de ejecución = (ejecutado / presupuesto) * 100
- **Formato de moneda**: Usa formato colombiano ($XXX.XXX.XXX)
- **Datos dummy automáticos**: Genera datos de prueba si no hay fuentes
- **CSV de ejemplo**: Guarda `ejecucion_presupuestal_demo.csv` cuando genera datos dummy

## Pruebas locales

### Prueba con datos dummy

```bash
# Eliminar fuentes de datos para forzar generación dummy
rm data/fuentes/ejecucion_presupuestal*.csv
rm data/fuentes/ejecucion_presupuestal*.json

# Generar sección
python main.py --anio 2025 --mes 9
```

### Prueba con CSV

1. Crear `data/fuentes/ejecucion_presupuestal.csv`:
```csv
categoria,presupuesto,ejecutado
Mano de obra,200000000,180000000
Repuestos,50000000,42000000
```

2. Ejecutar:
```bash
python main.py --anio 2025 --mes 9
```

### Prueba con JSON

1. Crear `data/fuentes/ejecucion_presupuestal_9_2025.json` con la estructura esperada
2. Ejecutar el generador

## Notas

- El placeholder `{{ grafico_ejecucion_img }}` en el template puede ser reemplazado manualmente en Word con una imagen PNG
- Los porcentajes se calculan automáticamente y se redondean a 2 decimales
- Los valores monetarios se formatean usando `formato_moneda_cop()` de `src/utils/formato_moneda.py`

