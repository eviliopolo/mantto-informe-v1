# Ejemplos de Estructura de Datos para Sección 2

Este documento muestra cómo estructurar los datos JSON para cada subsección de la Sección 2 (Informe de Mesa de Servicio).

## Índice de Subsecciones

- **2**: Informe de Mesa de Servicio (Principal - con imagen)
- **2.1**: Informe de Mesa de Servicio
- **2.2**: Herramientas de Trabajo
- **2.3**: Visitas de Diagnósticos a Subsistemas
- **2.4**: Informe Consolidado del Estado de los Tickets Administrativos
- **2.5.1**: Escalamientos - ENEL
- **2.5.2**: Escalamientos - Caída Masiva
- **2.5.3**: Escalamientos - Conectividad
- **2.6**: Informe Actualizado de Hojas de Vida
- **2.7**: Informe Ejecutivo del Estado del Sistema

---

## Sección 2 (Principal) - Imagen

```json
{
  "image": "/ruta/a/imagen.png"
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_image

update_seccion_2_image(2025, 11, "/path/to/image.png")
```

---

## Sección 2.1 - Informe de Mesa de Servicio

```json
{
  "parrafo_introductorio": "Durante el mes de noviembre de 2025 se realizó el seguimiento constante a las actividades diarias relacionadas con la mesa de servicio...",
  "informes": [
    {
      "tipo": "Informe Diario",
      "fecha": "2025-11-15",
      "descripcion": "Informe de actividades del día relacionadas con la mesa de servicio",
      "estado": "Enviado"
    },
    {
      "tipo": "Informe Semanal",
      "fecha": "2025-11-20",
      "descripcion": "Resumen semanal de actividades y métricas",
      "estado": "Enviado"
    }
  ]
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_1

datos = {
    "parrafo_introductorio": "Texto del párrafo...",
    "informes": [
        {
            "tipo": "Informe Diario",
            "fecha": "2025-11-15",
            "descripcion": "Descripción del informe",
            "estado": "Enviado"
        }
    ]
}
update_seccion_2_1(2025, 11, datos)
```

---

## Sección 2.2 - Herramientas de Trabajo

```json
{
  "herramientas": [
    "Sistema GLPI para la gestión de tickets e incidentes",
    "Plataforma de monitoreo de disponibilidad de cámaras",
    "Sistema VMS (Video Management System) para visualización de cámaras",
    "Herramientas de comunicación (correo, Teams, WhatsApp corporativo)"
  ],
  "equipos": [
    "Equipos de cómputo y dispositivos móviles para el personal de campo",
    "Vehículos y motocicletas para desplazamiento del personal técnico",
    "Equipos de medición y diagnóstico (multímetros, probadores de red, etc.)",
    "Herramientas manuales y equipos de protección personal"
  ]
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_2

datos = {
    "herramientas": ["Herramienta 1", "Herramienta 2"],
    "equipos": ["Equipo 1", "Equipo 2"]
}
update_seccion_2_2(2025, 11, datos)
```

---

## Sección 2.3 - Visitas de Diagnósticos a Subsistemas

```json
{
  "parrafo_introductorio": "Durante el mes de noviembre de 2025 se realizaron visitas de diagnóstico a los diferentes subsistemas del sistema de videovigilancia.",
  "visitas": [
    {
      "subsistema": "Domos Ciudadanos",
      "cantidad_visitas": 15,
      "observaciones": "Se realizaron visitas de diagnóstico para identificar puntos de mejora en la operación"
    },
    {
      "subsistema": "Cámaras Fijas",
      "cantidad_visitas": 20,
      "observaciones": "Visitas programadas para mantenimiento preventivo"
    }
  ]
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_3

datos = {
    "parrafo_introductorio": "Texto introductorio...",
    "visitas": [
        {
            "subsistema": "Domos Ciudadanos",
            "cantidad_visitas": 15,
            "observaciones": "Observaciones sobre las visitas"
        }
    ]
}
update_seccion_2_3(2025, 11, datos)
```

---

## Sección 2.4 - Informe Consolidado del Estado de los Tickets

```json
{
  "resumen": {
    "total_tickets": 150,
    "tickets_cerrados": 120,
    "tickets_abiertos": 30,
    "tasa_cierre": 80.0
  },
  "tickets_por_proyecto": [
    {
      "proyecto": "Proyecto Domos Ciudadanos",
      "generados": 50,
      "cerrados": 40,
      "abiertos": 10
    },
    {
      "proyecto": "Proyecto Cámaras Fijas",
      "generados": 100,
      "cerrados": 80,
      "abiertos": 20
    }
  ],
  "tickets_por_estado": [
    {
      "estado": "Cerrado",
      "cantidad": 120,
      "porcentaje": 80.0
    },
    {
      "estado": "Abierto",
      "cantidad": 30,
      "porcentaje": 20.0
    }
  ],
  "tickets_por_subsistema": [
    {
      "subsistema": "Domos Ciudadanos",
      "cantidad": 45
    },
    {
      "subsistema": "Cámaras Fijas",
      "cantidad": 105
    }
  ]
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_4

datos = {
    "resumen": {
        "total_tickets": 150,
        "tickets_cerrados": 120,
        "tickets_abiertos": 30,
        "tasa_cierre": 80.0
    },
    "tickets_por_proyecto": [
        {
            "proyecto": "Proyecto A",
            "generados": 50,
            "cerrados": 40,
            "abiertos": 10
        }
    ],
    "tickets_por_estado": [
        {
            "estado": "Cerrado",
            "cantidad": 120,
            "porcentaje": 80.0
        }
    ],
    "tickets_por_subsistema": [
        {
            "subsistema": "Domos Ciudadanos",
            "cantidad": 45
        }
    ]
}
update_seccion_2_4(2025, 11, datos)
```

---

## Sección 2.5.1 - Escalamientos ENEL

```json
{
  "parrafo_introductorio": "Durante el mes de noviembre de 2025 se realizaron escalamientos al operador de red ENEL por fallas en el suministro de energía eléctrica.",
  "escalamientos": [
    {
      "ticket": "TKT-12345",
      "localidad": "Bogotá",
      "fecha": "2025-11-15",
      "descripcion": "Falla en suministro eléctrico en punto de videovigilancia ubicado en la localidad de Usaquén",
      "estado": "Resuelto"
    },
    {
      "ticket": "TKT-12346",
      "localidad": "Bogotá",
      "fecha": "2025-11-18",
      "descripcion": "Interrupción del servicio eléctrico por mantenimiento programado",
      "estado": "En proceso"
    }
  ],
  "total_escalamientos": 2
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_5_1_enel

datos = {
    "parrafo_introductorio": "Texto introductorio...",
    "escalamientos": [
        {
            "ticket": "TKT-12345",
            "localidad": "Bogotá",
            "fecha": "2025-11-15",
            "descripcion": "Descripción del escalamiento",
            "estado": "Resuelto"
        }
    ],
    "total_escalamientos": 1
}
update_seccion_2_5_1_enel(2025, 11, datos)
```

---

## Sección 2.5.2 - Caída Masiva

```json
{
  "parrafo_introductorio": "Durante el mes de noviembre de 2025 se presentaron eventos de caída masiva que afectaron la disponibilidad del sistema.",
  "hubo_caida_masiva": true,
  "eventos": [
    {
      "fecha": "2025-11-15",
      "descripcion": "Caída masiva del sistema de videovigilancia",
      "afectacion": "50 cámaras afectadas en 3 localidades",
      "causa": "Falla en servidor principal de gestión",
      "acciones": "Se activó el plan de contingencia y se restableció el servicio en 2 horas",
      "tiempo_solucion": "2 horas"
    }
  ]
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_5_2_caida_masiva

datos = {
    "parrafo_introductorio": "Texto introductorio...",
    "hubo_caida_masiva": true,
    "eventos": [
        {
            "fecha": "2025-11-15",
            "descripcion": "Descripción del evento",
            "afectacion": "50 cámaras afectadas",
            "causa": "Falla en servidor",
            "acciones": "Acciones tomadas",
            "tiempo_solucion": "2 horas"
        }
    ]
}
update_seccion_2_5_2_caida_masiva(2025, 11, datos)
```

---

## Sección 2.5.3 - Escalamientos Conectividad

```json
{
  "parrafo_introductorio": "Durante el mes de noviembre de 2025 se realizaron escalamientos por fallas de conectividad al área técnica de ETB.",
  "escalamientos": [
    {
      "ticket": "TKT-12347",
      "localidad": "Bogotá",
      "fecha": "2025-11-16",
      "descripcion": "Pérdida de conectividad en punto de videovigilancia",
      "estado": "En proceso"
    }
  ],
  "total_escalamientos": 1
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_5_3_conectividad

datos = {
    "parrafo_introductorio": "Texto introductorio...",
    "escalamientos": [
        {
            "ticket": "TKT-12347",
            "localidad": "Bogotá",
            "fecha": "2025-11-16",
            "descripcion": "Pérdida de conectividad",
            "estado": "En proceso"
        }
    ],
    "total_escalamientos": 1
}
update_seccion_2_5_3_conectividad(2025, 11, datos)
```

---

## Sección 2.6 - Informe Actualizado de Hojas de Vida

```json
{
  "parrafo_introductorio": "Durante el mes de noviembre de 2025 se mantuvieron actualizadas las hojas de vida de los puntos de videovigilancia en el sistema GLPI.",
  "hojas_vida": [
    {
      "subsistema": "Domos Ciudadanos",
      "total_puntos": 100,
      "actualizados": 95,
      "porcentaje_actualizado": 95.0
    },
    {
      "subsistema": "Cámaras Fijas",
      "total_puntos": 200,
      "actualizados": 190,
      "porcentaje_actualizado": 95.0
    }
  ]
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_6

datos = {
    "parrafo_introductorio": "Texto introductorio...",
    "hojas_vida": [
        {
            "subsistema": "Domos Ciudadanos",
            "total_puntos": 100,
            "actualizados": 95,
            "porcentaje_actualizado": 95.0
        }
    ]
}
update_seccion_2_6(2025, 11, datos)
```

---

## Sección 2.7 - Informe Ejecutivo del Estado del Sistema

```json
{
  "parrafo_introductorio": "Al cierre del mes de noviembre de 2025, el sistema de videovigilancia presenta un total de 850 cámaras operativas de un total de 1000 puntos.",
  "estado_sistema": {
    "operativas": 850,
    "no_operativas": 50,
    "mantenimiento": 100,
    "total": 1000,
    "porcentaje_operativas": 85.0,
    "porcentaje_no_operativas": 5.0,
    "porcentaje_mantenimiento": 10.0
  },
  "estado_por_localidad": [
    {
      "localidad": "Bogotá",
      "operativas": 400,
      "no_operativas": 20,
      "mantenimiento": 50,
      "total": 470
    },
    {
      "localidad": "Medellín",
      "operativas": 300,
      "no_operativas": 15,
      "mantenimiento": 30,
      "total": 345
    }
  ]
}
```

**Ejemplo de uso:**
```python
from src.data.repositories.build_section2 import update_seccion_2_7

datos = {
    "parrafo_introductorio": "Texto introductorio...",
    "estado_sistema": {
        "operativas": 850,
        "no_operativas": 50,
        "mantenimiento": 100,
        "total": 1000,
        "porcentaje_operativas": 85.0,
        "porcentaje_no_operativas": 5.0,
        "porcentaje_mantenimiento": 10.0
    },
    "estado_por_localidad": [
        {
            "localidad": "Bogotá",
            "operativas": 400,
            "no_operativas": 20,
            "mantenimiento": 50,
            "total": 470
        }
    ]
}
update_seccion_2_7(2025, 11, datos)
```

---

## Función Genérica para Actualizar Cualquier Sección

Si necesitas actualizar una sección de forma genérica, puedes usar la función `update_content_section2`:

```python
from src.data.repositories.build_section2 import update_content_section2

# Actualizar con texto simple
update_content_section2(2025, 11, "2.1", "Texto del contenido")

# Actualizar con objeto JSON
datos = {"campo1": "valor1", "campo2": "valor2"}
update_content_section2(2025, 11, "2.4", datos)

# Actualizar con lista
lista_datos = [{"item": 1}, {"item": 2}]
update_content_section2(2025, 11, "2.3", lista_datos)
```

---

## Obtener el Contenido de una Sección

Para leer el contenido de una sección:

```python
from src.data.repositories.build_section2 import get_content_section2

# Obtener el contenido de la sección 2.4
contenido = get_content_section2(2025, 11, "2.4")
print(contenido)
```

---

## Notas Importantes

1. **Formato de fechas**: Usa el formato `YYYY-MM-DD` para las fechas (ej: "2025-11-15")
2. **IDs de secciones**: Los IDs deben coincidir exactamente con los definidos en `build_section2` (ej: "2", "2.1", "2.2", etc.)
3. **Tipos de datos**: El campo `content` puede ser:
   - Un string (texto simple)
   - Un objeto JSON (dict)
   - Una lista (array)
   - Cualquier estructura JSON válida
4. **Actualización de timestamps**: Las funciones de actualización automáticamente actualizan los campos `updated_at` y `user_updated`

