# Sección 10 - Sistema de Gestión de Seguridad y Salud en el Trabajo (SG-SST)

## Descripción

La Sección 10 genera el reporte del Sistema de Gestión de Seguridad y Salud en el Trabajo del contrato SCJ-1809-2024, incluyendo:
- Inducciones y capacitaciones
- Reporte e investigación de incidentes/accidentes
- Entrega de elementos de protección personal (EPP)
- Inspecciones de seguridad
- Actividades del COPASST
- Medidas preventivas y correctivas
- Seguimiento e indicadores del mes

## Archivos

- `src/generadores/seccion_10_sgsst.py`: Generador principal
- `templates/seccion_10_sgsst.docx`: Template Word con placeholders Jinja2
- `data/fuentes/sgsst_dummy.csv`: CSV de ejemplo con datos dummy

## Uso

### Generación básica

```bash
python main.py --anio 2025 --mes 9
```

### Fuentes de datos

El generador busca datos en el siguiente orden:

1. **CSV**: `data/fuentes/sgsst.csv`
   - Estructura esperada con columnas según tipo de registro
   - Columnas comunes: `tipo`, `fecha`, `responsable`, etc.

2. **Datos dummy**: Si no encuentra CSV, genera automáticamente datos de prueba

### Estructura de datos

#### Capacitaciones
```python
{
    "tema": "Trabajo seguro en alturas",
    "fecha": "2025-09-03",
    "participantes": 12,
    "responsable": "HSE"
}
```

#### Incidentes
```python
{
    "fecha": "2025-09-11",
    "tipo": "Incidente sin lesión",
    "descripcion": "Resbalón en área húmeda sin consecuencias",
    "clasificacion": "Leve",
    "accion_tomada": "Secado de área, señalización preventiva"
}
```

#### EPP
```python
{
    "item": "Casco dieléctrico",
    "cantidad": 5,
    "fecha": "2025-09-05",
    "entregado_a": "Equipo Técnico"
}
```

#### Inspecciones
```python
{
    "lugar": "Bodega Central",
    "fecha": "2025-09-08",
    "estado": "Cumple",
    "observaciones": "Sin novedades, condiciones seguras"
}
```

#### COPASST
```python
{
    "actividad": "Reunión mensual COPASST",
    "fecha": "2025-09-04",
    "acuerdos": "Actualizar matriz de peligros y revisar protocolos"
}
```

#### Medidas Correctivas
```python
{
    "medida": "Recarga de extintores",
    "responsable": "Infraestructura",
    "fecha_compromiso": "2025-09-20",
    "estado": "En ejecución"
}
```

#### Indicadores
```python
{
    "accidentalidad": "0 casos con lesión",
    "porcentaje_capacitacion": 85.0,
    "cumplimiento_inspecciones": 90.0,
    "total_capacitaciones": 4,
    "total_incidentes": 2,
    "total_epp_entregado": 35,
    "total_inspecciones": 4,
    "total_medidas": 3
}
```

## Características

- **Cálculo automático de indicadores**: Porcentajes de capacitación y cumplimiento calculados dinámicamente
- **Datos dummy automáticos**: Genera datos de prueba si no hay fuentes
- **CSV de ejemplo**: Guarda `sgsst_dummy.csv` cuando genera datos dummy
- **Múltiples subsecciones**: 7 subsecciones con tablas independientes
- **Manejo de listas vacías**: Mensajes informativos cuando no hay datos

## Pruebas locales

### Prueba con datos dummy

```bash
# Eliminar fuentes de datos para forzar generación dummy
rm data/fuentes/sgsst.csv

# Generar sección
python main.py --anio 2025 --mes 9
```

### Prueba con CSV

1. Crear `data/fuentes/sgsst.csv` con estructura apropiada:
```csv
tipo,tema,fecha,participantes,responsable
capacitacion,Trabajo seguro en alturas,2025-09-03,12,HSE
capacitacion,Uso adecuado de EPP,2025-09-10,18,Seguridad Industrial
```

2. Ejecutar:
```bash
python main.py --anio 2025 --mes 9
```

## Subsecciones

### 10.1 Inducciones y capacitaciones
Registro de todas las capacitaciones realizadas durante el periodo, incluyendo tema, fecha, participantes y responsable.

### 10.2 Reporte e investigación de incidentes / accidentes
Registro de incidentes y accidentes reportados, con clasificación y acciones tomadas.

### 10.3 Entrega de elementos de protección personal (EPP)
Control de entrega de EPP a los trabajadores, incluyendo tipo, cantidad y destinatario.

### 10.4 Inspecciones de seguridad
Resultados de inspecciones de seguridad realizadas en diferentes áreas, con estado y observaciones.

### 10.5 Actividades del COPASST
Registro de actividades del Comité Paritario de Seguridad y Salud en el Trabajo.

### 10.6 Medidas preventivas y correctivas
Seguimiento a medidas implementadas para prevenir o corregir situaciones de riesgo.

### 10.7 Seguimiento e indicadores del mes
Indicadores clave de desempeño del SG-SST:
- Accidentalidad
- Porcentaje de capacitación
- Porcentaje de cumplimiento en inspecciones

## Notas

- Los indicadores se calculan automáticamente a partir de los datos cargados
- El porcentaje de capacitación se calcula sobre un total estimado de personal
- El porcentaje de cumplimiento se calcula sobre las inspecciones realizadas
- Los datos dummy incluyen ejemplos realistas para todas las subsecciones

## Ejemplo de datos dummy

El generador crea automáticamente:
- 4 capacitaciones
- 2 incidentes
- 4 entregas de EPP
- 4 inspecciones
- 3 actividades COPASST
- 3 medidas correctivas
- Indicadores calculados automáticamente

Esto permite probar todas las subsecciones y visualizar el formato completo del reporte.

