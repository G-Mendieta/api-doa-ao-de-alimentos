import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Carrega os dados dos arquivos JSON
with open("alimentos.json", "r", encoding="utf-8") as f:
    alimentos = json.load(f)

with open("doadores.json", "r", encoding="utf-8") as f:
    doadores = json.load(f)

with open("instituicoes.json", "r", encoding="utf-8") as f:
    instituicoes = json.load(f)


# ROTAS GET ///////////////////////////////////////////////////////////////////

@app.route("/alimentos", methods=["GET"])
def listar_alimentos():
    return jsonify(alimentos), 200

@app.route("/alimentos/<int:id>", methods=["GET"])
def obter_alimento(id):
    for alimento in alimentos:
        if alimento["id"] == id:
            return jsonify(alimento), 200
    return jsonify({"erro": "Alimento não encontrado"}), 404

@app.route("/doadores", methods=["GET"])
def listar_doadores():
    return jsonify(doadores), 200

@app.route("/doadores/<int:id>", methods=["GET"])
def obter_doador(id):
    for doador in doadores:
        if doador["id"] == id:
            return jsonify(doador), 200
    return jsonify({"erro": "Doador não encontrado"}), 404

@app.route("/instituicoes", methods=["GET"])
def listar_instituicoes():
    return jsonify(instituicoes), 200

@app.route("/instituicoes/<int:id>", methods=["GET"])
def obter_instituicao(id):
    for instituicao in instituicoes:
        if instituicao["id"] == id:
            return jsonify(instituicao), 200
    return jsonify({"erro": "Instituição não encontrada"}), 404


# ROTAS POST //////////////////////////////////////////////////////////////////

@app.route("/alimentos", methods=["POST"])
def cadastrar_alimento():
    dados_req = request.json


    if not dados_req:
        return jsonify({"erro": "Corpo da requisição ausente ou inválido"}), 400

  
    if "nome" not in dados_req:
        return jsonify({"erro": "Campo 'nome' é obrigatório"}), 400
    if "quantidade" not in dados_req:
        return jsonify({"erro": "Campo 'quantidade' é obrigatório"}), 400

    
    if not isinstance(dados_req["nome"], str):
        return jsonify({"erro": "Campo 'nome' deve ser uma string"}), 422
    if not isinstance(dados_req["quantidade"], int) or isinstance(dados_req["quantidade"], bool):
        return jsonify({"erro": "Campo 'quantidade' deve ser um número inteiro"}), 422

    novo_id = max((a["id"] for a in alimentos), default=0) + 1
    alimento = {"id": novo_id, "nome": dados_req["nome"], "quantidade": dados_req["quantidade"]}
    alimentos.append(alimento)

    with open("alimentos.json", "w", encoding="utf-8") as f:
        json.dump(alimentos, f, ensure_ascii=False, indent=2)

    return jsonify(alimento), 201


@app.route("/doadores", methods=["POST"])
def cadastrar_doador():
    dados_req = request.json

  
    if not dados_req:
        return jsonify({"erro": "Corpo da requisição ausente ou inválido"}), 400

    
    if "nome" not in dados_req:
        return jsonify({"erro": "Campo 'nome' é obrigatório"}), 400
    if "email" not in dados_req:
        return jsonify({"erro": "Campo 'email' é obrigatório"}), 400

  
    if not isinstance(dados_req["nome"], str):
        return jsonify({"erro": "Campo 'nome' deve ser um texto"}), 422
    if not isinstance(dados_req["email"], str):
        return jsonify({"erro": "Campo 'email' deve ser um texto"}), 422

    novo_id = max((d["id"] for d in doadores), default=0) + 1
    doador = {"id": novo_id, "nome": dados_req["nome"], "email": dados_req["email"]}
    doadores.append(doador)

    with open("doadores.json", "w", encoding="utf-8") as f:
        json.dump(doadores, f, ensure_ascii=False, indent=2)

    return jsonify(doador), 201


@app.route("/instituicoes", methods=["POST"])
def cadastrar_instituicao():
    dados_req = request.json

  
    if not dados_req:
        return jsonify({"erro": "Corpo da requisição ausente ou inválido"}), 400

   
    if "nome" not in dados_req:
        return jsonify({"erro": "Campo 'nome' é obrigatório"}), 400

    if not isinstance(dados_req["nome"], str):
        return jsonify({"erro": "Campo 'nome' deve ser um texto"}), 422

    novo_id = max((i["id"] for i in instituicoes), default=0) + 1
    instituicao = {"id": novo_id, "nome": dados_req["nome"]}
    instituicoes.append(instituicao)

    with open("instituicoes.json", "w", encoding="utf-8") as f:
        json.dump(instituicoes, f, ensure_ascii=False, indent=2)

    return jsonify(instituicao), 201


if __name__ == "__main__":
    app.run(debug=True)