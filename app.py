from flask import Flask, request, jsonify
import numpy as np
from datetime import datetime
import logging

# Configurar logs estructurados
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Variable para almacenar el último análisis
last_analysis = None


def calculate_stats(data):
    """Calcula estadísticas descriptivas de una lista de números."""
    arr = np.array(data, dtype=float)

    # Detección de outliers usando IQR
    q1 = np.percentile(arr, 25)
    q3 = np.percentile(arr, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = arr[(arr < lower_bound) | (arr > upper_bound)].tolist()

    # Histograma de frecuencias
    counts, bin_edges = np.histogram(arr, bins='auto')
    histogram = []
    for i in range(len(counts)):
        histogram.append({
            "range": f"{bin_edges[i]:.2f} - {bin_edges[i+1]:.2f}",
            "frequency": int(counts[i])
        })

    # Calcular moda manualmente
    values, freq = np.unique(arr, return_counts=True)
    max_freq = freq.max()
    modes = values[freq == max_freq].tolist()

    return {
        "count": len(arr),
        "mean": round(float(np.mean(arr)), 4),
        "median": round(float(np.median(arr)), 4),
        "mode": modes,
        "std_dev": round(float(np.std(arr, ddof=1)), 4),
        "variance": round(float(np.var(arr, ddof=1)), 4),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "range": round(float(np.max(arr) - np.min(arr)), 4),
        "q1": round(float(q1), 4),
        "q3": round(float(q3), 4),
        "iqr": round(float(iqr), 4),
        "outliers": outliers,
        "histogram": histogram,
        "timestamp": datetime.now().isoformat()
    }


@app.route('/', methods=['GET'])
def home():
    """Endpoint raíz con información del API."""
    logger.info("GET / - Página principal")
    return jsonify({
        "api": "Data Analysis API",
        "version": "1.0.0",
        "description": "API para análisis estadístico de datos numéricos",
        "endpoints": {
            "GET /": "Información del API",
            "GET /stats/summary": "Resumen del último análisis realizado",
            "POST /stats/analyze": "Analizar un nuevo dataset"
        }
    })


@app.route('/stats/summary', methods=['GET'])
def get_summary():
    """Devuelve el último análisis realizado."""
    logger.info("GET /stats/summary")
    if last_analysis is None:
        return jsonify({
            "message": "No hay análisis previos. Envía datos con POST /stats/analyze"
        }), 404
    return jsonify(last_analysis)


@app.route('/stats/analyze', methods=['POST'])
def analyze_data():
    """Recibe una lista de números y devuelve análisis estadístico."""
    global last_analysis

    # Validar que se envió JSON
    if not request.is_json:
        logger.warning("POST /stats/analyze - Request sin JSON")
        return jsonify({"error": "El Content-Type debe ser application/json"}), 400

    body = request.get_json()

    # Validar que existe el campo 'data'
    if 'data' not in body:
        logger.warning("POST /stats/analyze - Campo 'data' faltante")
        return jsonify({"error": "El campo 'data' es requerido"}), 400

    data = body['data']

    # Validar que sea una lista
    if not isinstance(data, list):
        return jsonify({"error": "'data' debe ser una lista de números"}), 400

    # Validar que no esté vacía
    if len(data) == 0:
        return jsonify({"error": "La lista no puede estar vacía"}), 400

    # Validar que todos sean números
    if not all(isinstance(x, (int, float)) for x in data):
        return jsonify({"error": "Todos los elementos deben ser números"}), 400

    # Validar mínimo 2 elementos para estadísticas
    if len(data) < 2:
        return jsonify({"error": "Se necesitan al menos 2 números para el análisis"}), 400

    logger.info(f"POST /stats/analyze - Analizando {len(data)} datos")
    result = calculate_stats(data)
    last_analysis = result

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)