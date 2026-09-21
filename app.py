from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

registos = []

HTML = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Controlo de Acesso NFC</title>

    <meta http-equiv="refresh" content="5">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            margin: 0;
            padding: 30px;
        }

        h1 {
            text-align: center;
        }

        table {
            width: 100%;
            max-width: 800px;
            margin: 20px auto;
            border-collapse: collapse;
            background: white;
        }

        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #333;
            color: white;
        }

        .autorizado {
            color: green;
            font-weight: bold;
        }

        .negado {
            color: red;
            font-weight: bold;
        }

        .desconhecido {
            color: orange;
            font-weight: bold;
        }
    </style>
</head>

<body>

    <h1>Controlo de Acesso NFC</h1>

    <table>
        <tr>
            <th>UID</th>
            <th>Estado</th>
            <th>Hora</th>
        </tr>

        {% for registo in registos %}
        <tr>
            <td>{{ registo.uid }}</td>
            <td class="{{ registo.estado }}">{{ registo.estado }}</td>
            <td>{{ registo.hora }}</td>
        </tr>
        {% endfor %}

    </table>

</body>
</html>
"""


@app.route("/")
def pagina_inicial():
    return render_template_string(HTML, registos=registos)


@app.route("/registo", methods=["POST"])
def receber_registo():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "JSON inválido ou ausente"
        }), 400

    uid = dados.get("uid")
    estado = dados.get("estado")
    hora = dados.get("hora")

    if not uid or not estado or not hora:
        return jsonify({
            "erro": "É necessário enviar uid, estado e hora"
        }), 400

    if estado not in ["autorizado", "negado", "desconhecido"]:
        return jsonify({
            "erro": "Estado inválido"
        }), 400

    registo = {
        "uid": uid,
        "estado": estado,
        "hora": hora
    }

    registos.insert(0, registo)

    return jsonify({
        "mensagem": "Registo recebido com sucesso",
        "registo": registo
    }), 201


@app.route("/dados", methods=["GET"])
def obter_dados():
    return jsonify(registos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
