# Data Analysis API

API REST para análisis estadístico de datos numéricos, desarrollada con Flask y NumPy.

## Descripción

Esta API recibe datasets numéricos y devuelve análisis estadísticos completos incluyendo medidas de tendencia central, dispersión, detección de valores atípicos (outliers) e histogramas de frecuencia.

## Tecnologías

- Python 3.11
- Flask
- NumPy
- Docker

## Instalación local
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

El servidor estará disponible en `http://localhost:5001`

## Endpoints

### GET /
Información general del API.

### GET /stats/summary
Retorna el último análisis realizado.

### POST /stats/analyze
Recibe una lista de números y retorna análisis estadístico completo.

**Body (JSON):**
```json
{
  "data": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
}
```

**Respuesta incluye:** media, mediana, moda, desviación estándar, varianza, rango, cuartiles, detección de outliers (IQR) e histograma de frecuencias.

## Docker
```bash
docker build -t data-analysis-api .
docker run -p 5001:5001 data-analysis-api
```

## Pruebas con curl
```bash
# GET raíz
curl http://localhost:5001/

# POST análisis
curl -X POST http://localhost:5001/stats/analyze \
  -H "Content-Type: application/json" \
  -d '{"data": [10, 20, 30, 40, 50]}'

# Validación de errores
curl -X POST http://localhost:5001/stats/analyze \
  -H "Content-Type: application/json" \
  -d '{"data": []}'
```