# Generador de Informes Mensuales ETB

Sistema automatizado en Python para generar informes mensuales de ~100 páginas para el contrato de mantenimiento **SCJ-1809-2024** de ETB (Empresa de Telecomunicaciones de Bogotá).

## Características

- ✅ Generación automática de informes mensuales
- ✅ Arquitectura modular por secciones
- ✅ Soporte para múltiples fuentes de datos (Excel, CSV, GLPI, MySQL, SharePoint)
- ✅ Templates Word con placeholders Jinja2
- ✅ Manejo de contenido fijo y dinámico

## Estructura del Proyecto

```
mantto-informe-v1/
├── main.py                    # Punto de entrada principal (CLI)
├── app.py                     # API FastAPI (REST)
├── config.py                  # Configuración global
├── requirements.txt           # Dependencias
├── run_seeders.py            # Script para ejecutar seeders
│
├── templates/                 # Templates Word con placeholders Jinja2
│   ├── seccion_1_info_general.docx
│   ├── seccion_2_mesa_servicio.docx
│   ├── seccion_3_ans.docx
│   ├── seccion_4_bienes_servicios.docx
│   ├── seccion_5_laboratorio.docx
│   ├── seccion_6_visitas.docx
│   ├── seccion_7_siniestros.docx
│   ├── seccion_8_presupuesto.docx
│   ├── seccion_9_riesgos.docx
│   ├── seccion_10_sgsst.docx
│   ├── seccion_11_valores.docx
│   ├── seccion_12_conclusiones.docx
│   ├── seccion_13_anexos.docx
│   └── seccion_14_control_cambios.docx
│
├── data/                      # Datos de entrada
│   ├── fuentes/              # Archivos fuente (Excel, CSV)
│   ├── fijos/                # Contenido fijo del contrato
│   │   ├── alcance.txt
│   │   ├── glosario.json
│   │   ├── infraestructura.txt
│   │   ├── obligaciones_*.txt
│   │   └── personal_requerido.json
│   └── configuracion/        # Archivos de configuración
│       └── meses.json
│
├── output/                    # Informes generados
│   └── seccion_2/            # Informes por sección
│
├── informesAprobados/        # Informes aprobados (PDFs de referencia)
│
├── seeders/                   # Seeders para base de datos
│   ├── 00_access_roles.py
│   └── access_roles.py
│
├── ans_config/                # Configuración ANS
│   └── ans_config.py
│
├── EJEMPLOS_JSON_SECCION2.json  # Ejemplos JSON para Sección 2
├── EJEMPLOS_JSON_SECCION2.md    # Documentación de ejemplos
│
├── ESTADO_IMPLEMENTACION_*.md  # Estados de implementación por sección
├── ESTADO_INTEGRACION_*.md     # Estados de integración por sección
│
├── test_*.py                  # Tests unitarios e integración
│
└── src/                       # Código fuente modular
    ├── controllers/          # Controladores (lógica de negocio)
    │   ├── auth_controller.py
    │   └── section2_controller.py
    │
    ├── routes/               # Rutas de la API
    │   ├── auth_routes.py
    │   └── section2_routes.py
    │
    ├── services/             # Servicios (lógica de aplicación)
    │   ├── database.py
    │   ├── section2_service.py
    │   ├── auth_service.py
    │   ├── jwt_service.py
    │   └── external_auth_service.py
    │
    ├── models/               # Modelos de datos
    │   ├── user.py
    │   └── access_role.py
    │
    ├── middleware/           # Middleware (autenticación, permisos)
    │   ├── auth_middleware.py
    │   └── permissions.py
    │
    ├── data/                 # Repositorios de datos
    │   └── repositories/
    │       ├── build_section2.py
    │       └── EJEMPLOS_ESTRUCTURA_DATOS_SECCION2.md
    │
    ├── generadores/          # Generadores por sección
    │   ├── base.py
    │   ├── seccion_1_info_general.py
    │   ├── seccion_2_mesa_servicio.py
    │   ├── seccion_3_ans.py
    │   ├── seccion_4_bienes.py
    │   ├── seccion_5_laboratorio.py
    │   ├── seccion_6_visitas.py
    │   ├── seccion_7_siniestros.py
    │   ├── seccion_8_presupuesto.py
    │   ├── seccion_9_riesgos.py
    │   ├── seccion_10_sgsst.py
    │   ├── seccion_11_valores.py
    │   ├── seccion_12_conclusiones.py
    │   ├── seccion_13_anexos.py
    │   └── seccion_14_control_cambios.py
    │
    ├── extractores/          # Extractores de datos
    │   ├── excel_extractor.py
    │   ├── glpi_extractor.py
    │   ├── mysql_extractor.py
    │   └── sharepoint_extractor.py
    │
    ├── utils/                # Utilidades
    │   ├── documento_utils.py
    │   ├── fecha_utils.py
    │   ├── formato_moneda.py
    │   ├── numero_a_letras.py
    │   └── tabla_utils.py
    │
    └── ia/                   # Módulos de IA (Fase 4-5)
        ├── analizador_datos.py
        └── generador_parrafos.py
```

## Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Modo CLI (Línea de comandos)

```bash
# Generar informe de Septiembre 2025
python main.py --anio 2025 --mes 9

# Generar informe con versión específica
python main.py -a 2025 -m 9 -v 2
```

**Parámetros CLI:**
- `--anio, -a`: Año del informe (default: año actual)
- `--mes, -m`: Mes del informe 1-12 (default: mes actual)
- `--version, -v`: Versión del documento (default: 1)

### Modo API (REST)

```bash
# Iniciar servidor API
python app.py

# O con uvicorn directamente
uvicorn app:app --reload --port 8000
```

**Endpoints principales:**
- `POST /api/section2/send-data` - Enviar datos de una sección
- `GET /api/section2/get-section` - Obtener datos de una sección
- `GET /api/section2/get-all` - Obtener todas las secciones
- `POST /api/section2/generate` - Generar documento Word
- `POST /api/auth/login` - Autenticación

## Configuración

Editar `config.py` para ajustar:

- Información del contrato
- Rutas de directorios
- Configuración de subsistemas
- Parámetros del contrato

## Archivos de Datos

### Contenido Fijo

Los archivos en `data/fijos/` contienen contenido que no cambia entre informes:

- `alcance.txt`
- `obligaciones_generales.txt`
- `obligaciones_especificas.txt`
- `obligaciones_ambientales.txt`
- `glosario.json`
- `personal_requerido.json`

### Datos Fuente

Los archivos en `data/fuentes/` contienen datos variables que se extraen mensualmente:

- `comunicados_{mes}_{anio}.json`
- Excel/CSV con datos de tickets, inventario, etc.

## Templates Word

Los templates deben crearse manualmente en `templates/` con formato y estilos deseados, usando placeholders Jinja2:

```
{{ variable }}
{% for item in lista %}
  {{ item.campo }}
{% endfor %}
```

## Secciones del Informe

1. **Información General del Contrato** - ✅ Implementado
2. **Mesa de Servicio (GLPI)** - ✅ Implementado (API REST)
   - 2.1 Informe de Mesa de Servicio
   - 2.2 Herramientas de Trabajo
   - 2.3 Visitas de Diagnósticos a Subsistemas
   - 2.4 Informe Consolidado del Estado de los Tickets
   - 2.5 Escalamientos
     - 2.5.1 ENEL
     - 2.5.2 Caída Masiva
     - 2.5.3 Conectividad
   - 2.6 Informe Actualizado de Hojas de Vida
   - 2.7 Informe Ejecutivo del Estado del Sistema
3. ANS (Disponibilidad) - ✅ Implementado
4. Bienes y Servicios - ✅ Implementado
5. Laboratorio - ✅ Implementado
6. Visitas Técnicas - ✅ Implementado
7. Siniestros - ✅ Implementado
8. Ejecución Presupuestal - ✅ Implementado
9. Matriz de Riesgos - ✅ Implementado
10. SGSST - ✅ Implementado
11. Valores Públicos - ✅ Implementado
12. Conclusiones - ✅ Implementado
13. Anexos - ✅ Implementado
14. Control de Cambios - ✅ Implementado

## Desarrollo

### Arquitectura

El proyecto sigue una arquitectura en capas:

- **Controllers**: Manejan las peticiones HTTP y coordinan servicios
- **Services**: Contienen la lógica de negocio y acceso a datos
- **Repositories**: Acceso a base de datos (MongoDB)
- **Generators**: Generan documentos Word desde templates
- **Models**: Modelos de datos (User, AccessRole)
- **Middleware**: Autenticación y autorización

### Agregar nueva sección

1. Crear generador en `src/generadores/seccion_X_nombre.py`
2. Crear template en `templates/seccion_X_nombre.docx`
3. Crear repositorio en `src/data/repositories/build_sectionX.py`
4. Crear servicio en `src/services/sectionX_service.py`
5. Crear controlador en `src/controllers/sectionX_controller.py`
6. Crear rutas en `src/routes/sectionX_routes.py`
7. Registrar rutas en `app.py`

### Extractores de datos

Los extractores en `src/extractores/` están preparados para:

- **Excel/CSV**: `excel_extractor.py` ✅
- **GLPI**: `glpi_extractor.py` ✅
- **MySQL**: `mysql_extractor.py` ✅
- **SharePoint**: `sharepoint_extractor.py` ✅

### Base de Datos

El proyecto usa **MongoDB** para almacenar:
- Documentos de secciones
- Usuarios y roles
- Configuraciones

Configurar `MONGO_URI` y `MONGO_DB` en `.env`

### Autenticación

- Autenticación JWT
- Roles y permisos
- Integración con sistema externo de autenticación

## Archivos de Ejemplo

- `EJEMPLOS_JSON_SECCION2.json` - Ejemplos JSON completos para todas las secciones de la Sección 2
- `EJEMPLOS_JSON_SECCION2.md` - Documentación de ejemplos en formato Markdown

## Testing

Ejecutar tests:

```bash
# Tests unitarios
python test_seccion1.py
python test_seccion2.py

# Tests de integración
python test_integracion_seccion4.py
python test_integracion_seccion6.py
```

## Documentación Adicional

- `ESTADO_IMPLEMENTACION_*.md` - Estados de implementación por sección
- `ESTADO_INTEGRACION_*.md` - Estados de integración por sección
- `INSTRUCCIONES_ACTUALIZAR_TEMPLATE_SECCION1.md` - Guía para actualizar templates
- `templates/README_TEMPLATES.md` - Guía de templates Word

## Notas

- Los templates Word deben crearse manualmente con el formato deseado usando placeholders Jinja2
- El contenido fijo debe completarse desde el Anexo Técnico del contrato real
- Para producción, configurar conexiones a fuentes de datos externas (GLPI, MySQL, SharePoint)
- Configurar variables de entorno en `.env` (MONGO_URI, MONGO_DB, JWT_SECRET, etc.)

## Licencia

Proyecto interno para ETB - Contrato SCJ-1809-2024


