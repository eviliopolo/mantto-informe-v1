# Ejemplos JSON Completos - Sección 2

Este documento contiene todos los ejemplos JSON para las secciones de la Sección 2, listos para copiar y pegar en Postman.

---

## Sección 2 - INFORME DE MESA DE SERVICIO

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2",
  "level": 1,
  "content": {
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
  }
}
```

---

## Sección 2.1 - INFORME DE MESA DE SERVICIO

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.1",
  "level": 2,
  "content": {
    "route": "",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "table_1": [
      {
        "item": "1",
        "fecha": "6/11/2025",
        "referencia": "REF-001",
        "radicado": "RAD-001",
        "estado": "Aprobado",
        "aprobacion": "Sí"
      }
    ],
    "table_2": [
      {
        "subsistema": "Domos Ciudadanos",
        "diagnostico": "10",
        "diagnostico_subsistema": "5",
        "limpieza_acrilico": "3",
        "mto_acometida": "2",
        "mto_correctivo": "8",
        "mto_correctivo_subsistema": "4",
        "plan_de_choque": "1",
        "total": "33"
      }
    ]
  }
}
```

---

## Sección 2.2 - HERRAMIENTAS DE TRABAJO

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.2",
  "level": 2,
  "content": {
    "email": "ergrodz@etb.com.co"
  }
}
```

---

## Sección 2.3 - VISITAS DE DIAGNÓSTICOS A SUBSISTEMAS

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.3",
  "level": 2,
  "content": {
    "table_1": [
      {
        "subsistema": "Domos Ciudadanos",
        "ejecutadas": "15"
      },
      {
        "subsistema": "TransMilenio",
        "ejecutadas": "12"
      }
    ],
    "comunicacion": "",
    "oficio": ""
  }
}
```

---

## Sección 2.4 - INFORME CONSOLIDADO DEL ESTADO DE LOS TICKETS ADMINISTRATIVOS

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.4",
  "level": 2,
  "content": {
    "table_1": [
      {
        "subsistema": "Domos Ciudadanos",
        "diagnostico": "10",
        "diagnostico_subsistema": "5",
        "limpieza_acrilico": "3",
        "mto_acometida": "2",
        "mto_correctivo": "8",
        "mto_correctivo_subsistema": "4",
        "plan_de_choque": "1",
        "total": "33"
      }
    ],
    "name_document": "INFORME CONSOLIDADO TICKETS ADMINISTRATIVOS NOVIEMBRE 2025",
    "table_2": [
      {
        "subsistema": "Domos Ciudadanos",
        "cerrado": "45",
        "en_curso_asignada": "12",
        "en_curso_planificada": "8",
        "en_espera": "5",
        "resueltas": "3",
        "total": "73"
      }
    ]
  }
}
```

---

## Sección 2.5 - ESCALAMIENTOS

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.5",
  "level": 2,
  "content": {}
}
```

**Nota:** Esta sección calcula automáticamente los datos desde SharePoint. Puedes enviar `content` vacío o con `table_1` como fallback.

---

## Sección 2.5.1 - ENEL

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.5.1",
  "level": 3,
  "content": {}
}
```

**Nota:** Esta sección obtiene datos automáticamente desde SharePoint (hoja 3 - ENEL). Puedes enviar `content` vacío o con `table_1` como fallback.

---

## Sección 2.5.2 - CAÍDA MASIVA

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.5.2",
  "level": 3,
  "content": {}
}
```

**Nota:** Esta sección obtiene datos automáticamente desde SharePoint (hoja 1 - CAÍDA MASIVA). Puedes enviar `content` vacío o con `table_1` como fallback.

---

## Sección 2.5.3 - CONECTIVIDAD

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.5.3",
  "level": 3,
  "content": {}
}
```

**Nota:** Esta sección obtiene datos automáticamente desde SharePoint (hoja 2 - CONECTIVIDAD). Puedes enviar `content` vacío o con `table_1` como fallback.

---

## Sección 2.6 - INFORME ACTUALIZADO DE HOJAS DE VIDA

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.6",
  "level": 2,
  "content": {}
}
```

**Nota:** Esta sección busca automáticamente el archivo Excel en SharePoint y establece `name_document`. Puedes enviar `content` vacío o con `name_document` como fallback.

---

## Sección 2.7 - INFORME EJECUTIVO DEL ESTADO DEL SISTEMA

```json
{
  "anio": 2025,
  "mes": 11,
  "user_id": 22,
  "name_file": "INFORME MENSUAL 2",
  "section_id": "2.7",
  "level": 2,
  "content": {
    "cantidades_estado": {
      "caida_masiva": "56",
      "fuera_de_servicio": "1607",
      "operativa": "3509",
      "operativa_con_novedad": "652"
    },
    "cantidades_responsable": {
      "pte_aprobacion_uso_de_bolsa": "609",
      "conectividad": "591",
      "mantenimiento": "174",
      "siniestro": "107",
      "energizacion": "57",
      "obras": "52",
      "punto_desmontado": "12",
      "enel": "5"
    },
    "datos_subsistemas": {
      "estaciones_de_policia": {
        "caida_masiva": "0",
        "fuera_de_servicio": "45",
        "operativa": "233",
        "operativa_con_novedad": "24"
      },
      "proyecto_350": {
        "caida_masiva": "4",
        "fuera_de_servicio": "120",
        "operativa": "251",
        "operativa_con_novedad": "58"
      },
      "proyecto_732": {
        "caida_masiva": "7",
        "fuera_de_servicio": "373",
        "operativa": "1011",
        "operativa_con_novedad": "250"
      },
      "proyecto_alcaldia": {
        "caida_masiva": "42",
        "fuera_de_servicio": "407",
        "operativa": "1047",
        "operativa_con_novedad": "178"
      },
      "proyecto_cai": {
        "caida_masiva": "0",
        "fuera_de_servicio": "138",
        "operativa": "360",
        "operativa_con_novedad": "12"
      },
      "proyecto_colegios": {
        "caida_masiva": "0",
        "fuera_de_servicio": "162",
        "operativa": "30",
        "operativa_con_novedad": "43"
      },
      "proyecto_ctp": {
        "caida_masiva": "0",
        "fuera_de_servicio": "11",
        "operativa": "93",
        "operativa_con_novedad": "0"
      },
      "proyecto_esu_c4": {
        "caida_masiva": "3",
        "fuera_de_servicio": "134",
        "operativa": "158",
        "operativa_con_novedad": "30"
      },
      "proyecto_esu_estadio": {
        "caida_masiva": "0",
        "fuera_de_servicio": "2",
        "operativa": "56",
        "operativa_con_novedad": "0"
      },
      "proyecto_fvs": {
        "caida_masiva": "0",
        "fuera_de_servicio": "139",
        "operativa": "194",
        "operativa_con_novedad": "45"
      },
      "proyecto_transmilenio": {
        "caida_masiva": "0",
        "fuera_de_servicio": "76",
        "operativa": "76",
        "operativa_con_novedad": "12"
      }
    },
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "section_1": "Texto de la sección 1",
    "section_2": "Texto de la sección 2",
    "section_3": "Texto de la sección 3",
    "name_document": "",
    "observaciones": ""
  }
}
```

---

## Notas Importantes:

1. **Endpoint común**: Todas las secciones usan el mismo endpoint: `POST /section2/send_data_section`

2. **Secciones automáticas**: Las secciones 2.5, 2.5.1, 2.5.2, 2.5.3 y 2.6 obtienen datos automáticamente desde SharePoint. Puedes enviar `content` vacío.

3. **Imágenes**: Se incluye un base64 básico de 1x1 pixel azul como placeholder. Reemplázalo con tus imágenes reales en base64.

4. **Fechas**: Las fechas se formatean automáticamente al formato `d/m/yyyy` (ej: `6/11/2025`).

5. **Totales**: Los totales se calculan automáticamente si no se proporcionan en las secciones 2.7.

6. **Variables en template Word**:
   - `{{ table_27_1 }}` - Tabla de estados
   - `{{ table_27_2 }}` - Tabla de responsables
   - `{{ table_27_3 }}` - Tabla de subsistemas
   - `{{ suma_total_registros_252 }}` - Número de consecutivos únicos en sección 2.5.2

