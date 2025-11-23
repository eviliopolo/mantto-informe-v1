# Sección 9 - Matriz de Riesgos

## Descripción

La Sección 9 genera la matriz de riesgos del contrato SCJ-1809-2024, incluyendo:
- Identificación y evaluación de riesgos
- Clasificación por nivel (Bajo/Medio/Alto/Crítico)
- Medidas de mitigación y responsables
- Gráfico heatmap de probabilidad vs impacto
- Resumen estadístico por clasificación

## Archivos

- `src/generadores/seccion_9_riesgos.py`: Generador principal
- `templates/seccion_9_riesgos.docx`: Template Word con placeholders Jinja2
- `data/fuentes/matriz_riesgos_demo.csv`: CSV de ejemplo con datos dummy
- `output/matriz_riesgos_heatmap.png`: Gráfico generado automáticamente

## Dependencias

**Importante**: Esta sección requiere `matplotlib` para generar el gráfico heatmap.

Si no está instalado, agregar a `requirements.txt`:
```
matplotlib==3.7.2
```

Instalar con:
```bash
pip install matplotlib
```

Si matplotlib no está disponible, la sección funcionará pero no generará el gráfico.

## Uso

### Generación básica

```bash
python main.py --anio 2025 --mes 9
```

### Fuentes de datos

El generador busca datos en el siguiente orden:

1. **CSV**: `data/fuentes/matriz_riesgos.csv`
   - Columnas esperadas: `id`, `riesgo`, `probabilidad`, `impacto`, `descripcion`, `mitigacion`, `responsable`, `fecha_compromiso`

2. **Datos dummy**: Si no encuentra CSV, genera automáticamente datos de prueba

### Estructura de datos

#### Riesgo individual
```python
{
    "id": 1,
    "riesgo": "Fallas eléctricas masivas",
    "probabilidad": 3,  # Escala 1-5
    "impacto": 5,       # Escala 1-5
    "descripcion": "Cortes de energía que afectan centros de monitoreo",
    "mitigacion": "Instalación UPS adicional y pruebas de respaldo",
    "responsable": "Coordinación Técnica",
    "fecha_compromiso": "2025-09-05",
    "nivel_num": 15,           # Calculado: probabilidad × impacto
    "clasificacion": "Crítico" # Calculado según nivel_num
}
```

## Cálculos y Clasificación

### Nivel Numérico
```
nivel_num = probabilidad × impacto
```

### Clasificación por Nivel
- **Bajo**: nivel_num 1-4
- **Medio**: nivel_num 5-8
- **Alto**: nivel_num 9-12
- **Crítico**: nivel_num 13-25

### Escalas
- **Probabilidad**: 1 (Muy baja) a 5 (Muy alta)
- **Impacto**: 1 (Muy bajo) a 5 (Muy alto)

## Interpretación de la Clasificación

### Bajo (1-4)
Riesgos con baja probabilidad y/o bajo impacto. Requieren monitoreo rutinario pero no acciones inmediatas.

### Medio (5-8)
Riesgos moderados que requieren planificación de mitigación y seguimiento periódico.

### Alto (9-12)
Riesgos significativos que requieren atención prioritaria y medidas de mitigación en el corto plazo.

### Crítico (13-25)
Riesgos de máxima prioridad que requieren acciones inmediatas y recursos dedicados para su mitigación.

## Características

- **Cálculo automático**: Nivel numérico y clasificación calculados automáticamente
- **Ordenamiento**: Riesgos ordenados por nivel numérico descendente (mayor riesgo primero)
- **Resumen estadístico**: Tabla agregada por clasificación con cantidades y porcentajes
- **Gráfico heatmap**: Matriz visual de probabilidad vs impacto (requiere matplotlib)
- **Datos dummy automáticos**: Genera datos de prueba si no hay fuentes
- **CSV de ejemplo**: Guarda `matriz_riesgos_demo.csv` cuando genera datos dummy

## Pruebas locales

### Prueba con datos dummy

```bash
# Eliminar fuentes de datos para forzar generación dummy
rm data/fuentes/matriz_riesgos.csv

# Generar sección
python main.py --anio 2025 --mes 9
```

### Prueba con CSV

1. Crear `data/fuentes/matriz_riesgos.csv`:
```csv
id,riesgo,probabilidad,impacto,descripcion,mitigacion,responsable,fecha_compromiso
1,Fallas eléctricas masivas,3,5,Cortes de energía que afectan centros,Instalación UPS,Coordinación Técnica,2025-09-05
2,Vandalismo en cámaras,4,3,Daños físicos a cámaras,Refuerzo de carcasa,Seguridad Operativa,2025-09-30
```

2. Ejecutar:
```bash
python main.py --anio 2025 --mes 9
```

### Verificar gráfico

Después de generar, verificar que se creó:
```bash
ls output/2025/09_Septiembre/matriz_riesgos_heatmap.png
```

## Salida generada

- **Documento Word**: `output/{anio}/{mes}_{nombre_mes}/seccion_9_riesgos.docx`
- **Gráfico PNG**: `output/{anio}/{mes}_{nombre_mes}/matriz_riesgos_heatmap.png`
- **CSV demo** (si se generaron datos dummy): `data/fuentes/matriz_riesgos_demo.csv`

## Notas

- El placeholder `{{ grafico_matriz_img }}` en el template puede ser reemplazado manualmente en Word con la imagen PNG generada
- El gráfico se genera automáticamente si matplotlib está disponible
- Los riesgos se ordenan automáticamente por nivel de riesgo (mayor a menor)
- El resumen por clasificación se calcula automáticamente con porcentajes

## Ejemplo de datos dummy

El generador crea automáticamente 6 riesgos de ejemplo con diferentes niveles:
- 1 riesgo Crítico (nivel 15)
- 1 riesgo Alto (nivel 12)
- 2 riesgos Medios (niveles 8 y 12)
- 2 riesgos Bajos (niveles 4 y 8)

Esto permite probar todas las clasificaciones y visualizar el gráfico heatmap.

