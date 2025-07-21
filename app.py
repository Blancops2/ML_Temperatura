from flask import Flask, request, jsonify, render_template_string
import pickle

# Cargar modelo
with open("modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

app = Flask(__name__)

# HTML incrustado
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Conversión Celsius a Fahrenheit</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input, button { padding: 10px; font-size: 1rem; }
        .resultado { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Convertir Celsius a Fahrenheit</h1>
    <p>Introduce la temperatura en °C:</p>
    <input type="number" id="inputTemp" placeholder="Ej: 23">
    <button onclick="enviar()">Convertir</button>
    <div class="resultado" id="resultado"></div>

    <script>
        async function enviar() {
            const temp = document.getElementById("inputTemp").value;
            const res = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ temperatura: parseFloat(temp) })
            });
            const data = await res.json();
            if (data.Fahrenheit !== undefined) {
                document.getElementById("resultado").innerText = 
                    `${data.Celsius}°C = ${data.Fahrenheit.toFixed(2)}°F`;
            } else {
                document.getElementById("resultado").innerText = 
                    "Error: " + (data.error || "Entrada inválida");
            }
        }
    </script>
</body>
</html>
'''

@app.route("/")
def formulario():
    return render_template_string(html_template)

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
