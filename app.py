from datetime import date, datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DESCUENTO_PORCENTAJE = 20  # % fijo de descuento sobre el salario bruto


@app.route("/api/persona", methods=["POST"])
def crear_persona():
    """
    Recibe { "nombre": str, "apellido": str } y responde con el nombre completo.
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Se esperaba un cuerpo JSON con 'nombre' y 'apellido'."}), 400

    nombre = data.get("nombre", "")
    apellido = data.get("apellido", "")

    if not isinstance(nombre, str) or not isinstance(apellido, str):
        return jsonify({"error": "'nombre' y 'apellido' deben ser texto."}), 400

    nombre = nombre.strip()
    apellido = apellido.strip()

    if not nombre or not apellido:
        return jsonify({"error": "'nombre' y 'apellido' son obligatorios y no pueden estar vacíos."}), 400

    nombre_completo = f"{nombre} {apellido}"

    return jsonify({
        "nombre": nombre,
        "apellido": apellido,
        "nombre_completo": nombre_completo
    }), 200


@app.route("/api/salario", methods=["POST"])
def calcular_salario():
    """
    Recibe { "salario": number } y responde el salario neto tras un
    descuento fijo del 20% sobre el salario bruto.
    """
    data = request.get_json(silent=True)

    if not data or "salario" not in data:
        return jsonify({"error": "Se esperaba un cuerpo JSON con la clave 'salario'."}), 400

    salario_raw = data.get("salario")

    try:
        salario_bruto = float(salario_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "'salario' debe ser un número válido."}), 400

    if salario_bruto < 0:
        return jsonify({"error": "'salario' no puede ser negativo."}), 400

    descuento = round(salario_bruto * (DESCUENTO_PORCENTAJE / 100), 2)
    salario_neto = round(salario_bruto - descuento, 2)

    return jsonify({
        "salario_bruto": salario_bruto,
        "porcentaje_descuento": DESCUENTO_PORCENTAJE,
        "descuento": descuento,
        "salario_neto": salario_neto
    }), 200


@app.route("/api/edad", methods=["GET"])
def calcular_edad():
    """
    Recibe fecha_nacimiento=YYYY-MM-DD como query param y responde la edad
    calculada respecto a la fecha actual.
    """
    fecha_nacimiento_str = request.args.get("fecha_nacimiento", "")

    if not fecha_nacimiento_str:
        return jsonify({"error": "El parámetro 'fecha_nacimiento' es obligatorio (formato YYYY-MM-DD)."}), 400

    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    hoy = date.today()

    if fecha_nacimiento > hoy:
        return jsonify({"error": "La fecha de nacimiento no puede ser una fecha futura."}), 400

    edad = hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )

    return jsonify({
        "fecha_nacimiento": fecha_nacimiento_str,
        "edad": edad
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
