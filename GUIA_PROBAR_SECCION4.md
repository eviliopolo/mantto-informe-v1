# Guía para Probar la Sección 4

## 📋 Endpoints Disponibles

### 1. Generar Documento Sección 4

**Endpoint:** `POST /api/seccion4/generar`

**URL completa:** `http://localhost:8000/api/seccion4/generar`

**Body (JSON):**
```json
{
  "anio": 2025,
  "mes": 11,
  "output_path": "output/seccion_4/seccion_4_2025_11.docx"
}
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Sección 4 generada exitosamente",
  "file_path": "output/seccion_4/seccion_4_2025_11.docx",
  "anio": 2025,
  "mes": 11
}
```

---

### 2. Descargar Documento Sección 4

**Endpoint:** `POST /api/seccion4/descargar`

**URL completa:** `http://localhost:8000/api/seccion4/descargar`

**Body (JSON):**
```json
{
  "anio": 2025,
  "mes": 11
}
```

**Respuesta:** Archivo Word descargable

---

## 🧪 Cómo Probar con cURL

### Opción 1: Generar y obtener ruta del archivo

```bash
curl -X POST "http://localhost:8000/api/seccion4/generar" \
  -H "Content-Type: application/json" \
  -d '{
    "anio": 2025,
    "mes": 11
  }'
```

### Opción 2: Descargar directamente

```bash
curl -X POST "http://localhost:8000/api/seccion4/descargar" \
  -H "Content-Type: application/json" \
  -d '{
    "anio": 2025,
    "mes": 11
  }' \
  --output seccion_4_2025_11.docx
```

---

## 🧪 Cómo Probar con Postman

1. **Crear nueva petición POST**
   - URL: `http://localhost:8000/api/seccion4/generar`
   - Headers: `Content-Type: application/json`

2. **Body (raw JSON):**
```json
{
  "anio": 2025,
  "mes": 11
}
```

3. **Enviar petición**

4. **Verificar respuesta:**
   - Debe retornar `success: true`
   - Debe incluir `file_path` con la ruta del archivo generado

---

## 🧪 Cómo Probar con Python (requests)

```python
import requests
import json

# URL del endpoint
url = "http://localhost:8000/api/seccion4/generar"

# Datos a enviar
data = {
    "anio": 2025,
    "mes": 11
}

# Headers
headers = {
    "Content-Type": "application/json"
}

# Realizar petición
response = requests.post(url, json=data, headers=headers)

# Verificar respuesta
if response.status_code == 200:
    result = response.json()
    print(f"✅ Éxito: {result.get('message')}")
    print(f"📁 Archivo: {result.get('file_path')}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

---

## 📊 Estructura de Datos Esperada en MongoDB

El servicio espera que los datos estén en MongoDB en la colección `inventarios` con esta estructura:

```json
{
  "anio": 2025,
  "mes": 11,
  "seccion": "4",
  "subsecciones": {
    "4": {
      "1": {
        "texto": "Texto de gestión de inventario",
        "ruta": "Ruta del archivo",
        "tabla": [...]
      },
      "2": {
        "hayEntradas": true,
        "texto": "Texto de entradas",
        "comunicado": "COM-001",
        "fechaIngreso": "2025-11-15",
        "tablaEntradas": [
          {
            "itemBolsa": "Cámara IP",
            "cantidad": 10,
            "valor_unitario": 500000,
            "valor_total": 5000000
          }
        ]
      },
      "3": {
        "haySalidas": true,
        "texto": "Texto de equipos no operativos",
        "tablaDetalleEquipos": [...]
      },
      "4": {
        "texto": "Texto de inclusión a bolsa",
        "tablaGestionInclusion": {
          "consecutivoETB": "ETB-001",
          "fecha": "2025-11-20",
          "descripcion": "Descripción"
        }
      }
    }
  }
}
```

---

## ⚠️ Notas Importantes

1. **Base de datos MongoDB:** Asegúrate de que MongoDB esté corriendo y tenga datos de inventario para el año y mes especificados.

2. **Template Word:** El template debe estar en `src/resources/templates/seccion_4_bienes_servicios.docx`

3. **Estructura del template:** El template debe contener los placeholders:
   - `{{ mes }}`, `{{ anio }}`
   - `{{ texto_41 }}`, `{{ tabla_41_placeholder }}`
   - `{{ comunicado_42 }}`, `{{ fecha_42 }}`, `{{ tabla_42_placeholder }}`, `{{ valor_letras_42 }}`, `{{ anexos_42 }}`
   - `{{ comunicado_43 }}`, `{{ fecha_43 }}`, `{{ tabla_43_placeholder }}`, `{{ valor_letras_43 }}`, `{{ anexos_43 }}`
   - `{{ comunicado_44 }}`, `{{ fecha_44 }}`, `{{ tabla_44_placeholder }}`, `{{ valor_letras_44 }}`, `{{ anexos_44 }}`

4. **Placeholders de tablas:** Los placeholders de tablas deben estar en formato `[[TABLE_41]]`, `[[TABLE_42]]`, etc.

---

## 🔍 Verificar que Funciona

1. **Verificar logs:** Revisa los logs del servidor para ver si hay errores
2. **Verificar archivo generado:** Busca el archivo en la ruta especificada en `file_path`
3. **Abrir el documento:** Abre el archivo Word generado y verifica que:
   - Los placeholders fueron reemplazados
   - Las tablas se insertaron correctamente
   - Los valores monetarios están formateados
   - Los valores en letras están correctos

---

## 🐛 Solución de Problemas

### Error: "Template no encontrado"
- Verifica que el archivo `seccion_4_bienes_servicios.docx` esté en `src/resources/templates/`

### Error: "No se encontró inventario"
- Verifica que existan datos en MongoDB para el año y mes especificados
- Revisa la colección `inventarios` en MongoDB

### Error: "db es requerido"
- Asegúrate de que MongoDB esté configurado correctamente
- Verifica las variables de entorno de MongoDB

### Las tablas no se insertan
- Verifica que los placeholders en el template estén en formato `[[TABLE_XX]]`
- Revisa que los datos en MongoDB tengan la estructura correcta

