# Sección 11 - Valores Públicos

## Descripción

La Sección 11 genera el reporte de Valores Públicos del contrato SCJ-1809-2024, incluyendo:
- Pilotos e iniciativas de valor público
- Proyectos aprobados y en implementación
- Aprobaciones / actas y soportes
- Resultados cuantitativos y evidencias
- Recomendaciones y próximos pasos

## Archivos

- `src/generadores/seccion_11_valores.py`: Generador principal
- `templates/seccion_11_valores.docx`: Template Word con placeholders Jinja2
- `data/fuentes/valores_publicos_demo.csv`: CSV de ejemplo con datos dummy

## Uso

### Generación básica

```bash
python main.py --anio 2025 --mes 9
```

### Fuentes de datos

El generador busca datos en el siguiente orden:

1. **CSV**: `data/fuentes/valores_publicos.csv`
   - Estructura esperada con columnas según tipo de registro
   - Columnas comunes: `tipo`, `titulo`, `descripcion`, `estado`, `fecha`, etc.

2. **Datos dummy**: Si no encuentra CSV, genera automáticamente datos de prueba

### Estructura de datos

#### Pilotos
```python
{
    "titulo": "Piloto puntos con energía solar",
    "descripcion": "Implementación de paneles solares en 5 puntos piloto",
    "estado": "Aprobado",
    "fecha_aprobacion": "2025-08-20",
    "responsable": "Innovación ETB",
    "valor_aprobado": 32000000,
    "valor_aprobado_formato": "$32.000.000"
}
```

#### Proyectos
```python
{
    "nombre": "Integración estación piloto colegio",
    "alcance": "Integración de cámaras y conectividad en 1 colegio",
    "estado": "Culminado",
    "fecha_inicio": "2025-07-10",
    "fecha_fin": "2025-08-30",
    "coste": 9500000,
    "coste_formato": "$9.500.000"
}
```

#### Actas y Soportes
```python
{
    "tipo": "Acta aprobación PVV",
    "numero": "PVV-001-2025",
    "fecha": "2025-08-21",
    "url_soporte": "{{ soporte_pvv_001 }}"
}
```

#### Evidencias
```python
{
    "tipo": "Foto",
    "descripcion": "Instalación panel solar punto A",
    "ruta": "{{ evidencia_1_img }}"
}
```

#### Indicadores
```python
{
    "puntos_solar_operativos": 5,
    "reduccion_fallos_energia_pct": 30,
    "pvvs_aprobados": 2,
    "total_inversion_aprobada_formato": "$75.000.000"
}
```

## Características

- **Formato de moneda**: Valores monetarios formateados en formato colombiano ($XXX.XXX.XXX)
- **Datos dummy automáticos**: Genera datos de prueba si no hay fuentes
- **CSV de ejemplo**: Guarda `valores_publicos_demo.csv` cuando genera datos dummy
- **Placeholders multimedia**: Preparado para insertar imágenes, documentos y videos
- **Cálculo automático**: Total de inversión aprobada calculado automáticamente

## Pruebas locales

### Prueba con datos dummy

```bash
# Eliminar fuentes de datos para forzar generación dummy
rm data/fuentes/valores_publicos.csv

# Generar sección
python main.py --anio 2025 --mes 9
```

### Prueba con CSV

1. Crear `data/fuentes/valores_publicos.csv`:
```csv
tipo,titulo,descripcion,estado,fecha_aprobacion,responsable,valor_aprobado
piloto,Piloto puntos con energía solar,Implementación de paneles solares,Aprobado,2025-08-20,Innovación ETB,32000000
```

2. Ejecutar:
```bash
python main.py --anio 2025 --mes 9
```

## Subsecciones

### 11.1 Pilotos e iniciativas de valor público
Registro de pilotos e iniciativas innovadoras orientadas a mejorar la operación y resiliencia del sistema.

### 11.2 Proyectos aprobados y en implementación
Proyectos de valor público en diferentes estados: culminados, en ejecución, programados.

### 11.3 Aprobaciones / actas y soportes
Documentación oficial de aprobaciones, actas de comités y soportes relacionados.

### 11.4 Resultados cuantitativos y evidencias
Indicadores medibles y evidencias documentales (fotos, documentos, videos) de los proyectos.

### 11.5 Recomendaciones y próximos pasos
Recomendaciones estratégicas para continuar con los proyectos de valor público.

## Placeholders multimedia

El template incluye placeholders para recursos multimedia que deben ser reemplazados manualmente en Word:

- `{{ evidencia_1_img }}`: Para insertar imágenes
- `{{ evidencia_2_pdf }}`: Para insertar documentos PDF
- `{{ evidencia_3_img }}`: Para insertar imágenes adicionales
- `{{ evidencia_4_video }}`: Para insertar videos o enlaces
- `{{ soporte_pvv_001 }}`: Para insertar soportes de actas

### Cómo reemplazar placeholders en Word

1. Abrir el documento generado en Word
2. Buscar el placeholder (Ctrl+F)
3. Seleccionar el placeholder
4. Insertar > Imagen (o Insertar > Objeto para PDFs)
5. Seleccionar el archivo correspondiente
6. Eliminar el placeholder de texto

## Notas

- Los valores monetarios se formatean automáticamente usando `formato_moneda_cop()`
- El total de inversión aprobada se calcula sumando los valores de todos los pilotos
- Los datos dummy incluyen ejemplos realistas para todas las subsecciones
- Las fechas se generan dinámicamente según el mes del informe

## Ejemplo de datos dummy

El generador crea automáticamente:
- 3 pilotos (diferentes estados: Aprobado, En implementación, En evaluación)
- 3 proyectos (diferentes estados: Culminado, En ejecución, Programado)
- 3 actas y soportes
- 4 evidencias (fotos, documentos, videos)
- Indicadores calculados automáticamente
- Recomendaciones estratégicas

Esto permite probar todas las subsecciones y visualizar el formato completo del reporte.

