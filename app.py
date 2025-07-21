from flask import Flask, request, jsonify
import pickle

# Cargar modelo
with open("modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Modelo de predicción de Fahrenheit a partir de Celsius"

@app.route("/predict", methods=["POST"])
def predecir():
    datos = request.get_json()
    celsius = datos.get("temperatura")
    if celsius is None:
        return jsonify({"error": "Falta el valor de 'temperatura'"}), 400

    resultado = modelo.predict([[celsius]])
    return jsonify({
        "Celsius": celsius,
        "Fahrenheit": resultado[0][0]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)