from flask import Flask, request, jsonify

app = Flask(__name__)

# Dados simulados (mock)
alimentos = [
    {"id": 1, "nome": "Arroz", "quantidade": 10},
    {"id": 2, "nome": "Feijão", "quantidade": 5}
]

doadores = [
    {"id": 1, "nome": "Maria Silva", "email": "maria@email.com"},
    {"id": 2, "nome": "João Santos", "email": "joao@email.com"}
]

instituicoes = [
    {"id": 1, "nome": "Fazenda Cristo Rei Toledo", "endereco": "..."},
    {"id": 2, "nome": "Embaixada Solidaria Toledo", "endereco": ""},
    {"id": 3, "nome": "Banco de Alimentos Toledo", "endereco": ""}
]   

# ---------------- ROTAS GET ----------------
@app.route("/alimentos", methods=["GET"])
def listar_alimentos():
    return jsonify(alimentos), 200

@app.route("/alimentos/<int:id>", methods=["GET"])
def obter_alimento(id):
    alimento = next((a for a in alimentos if a["id"] == id), None)
    if alimento:
        return jsonify(alimento), 200
    return jsonify({"erro": "Alimento não encontrado"}), 404

@app.route("/doadores", methods=["GET"])
def listar_doadores():
    return jsonify(doadores), 200

@app.route("/instituicoes", methods=["GET"])
def listar_instituicoes():
    return jsonify(instituicoes), 200

# ---------------- ROTAS POST ----------------
@app.route("/alimentos", methods=["POST"])
def cadastrar_alimento():
    dados = request.json
    if not dados or "nome" not in dados or "quantidade" not in dados:
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400
    
    novo_id = len(alimentos) + 1
    alimento = {
        "id": novo_id,
        "nome": dados["nome"],
        "quantidade": dados["quantidade"],
        "validade": dados.get("validade", None)
    }
    alimentos.append(alimento)
    return jsonify(alimento), 201

@app.route("/doadores", methods=["POST"])
def cadastrar_doador():
    dados = request.json
    if not dados or "nome" not in dados or "email" not in dados:
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400
    
    novo_id = len(doadores) + 1
    doador = {
        "id": novo_id,
        "nome": dados["nome"],
        "email": dados["email"],
        "telefone": dados.get("telefone", None)
    }
    doadores.append(doador)
    return jsonify(doador), 201

@app.route("/instituicoes", methods=["POST"])
def cadastrar_instituicao():
    dados = request.json
    if not dados or "nome" not in dados or "endereco" not in dados:
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400
    
    novo_id = len(instituicoes) + 1
    instituicao = {
        "id": novo_id,
        "nome": dados["nome"],
        "endereco": dados["endereco"],
        "contato": dados.get("contato", None)
    }
    instituicoes.append(instituicao)
    return jsonify(instituicao), 201

if __name__ == "__main__":
    app.run(debug=True)
