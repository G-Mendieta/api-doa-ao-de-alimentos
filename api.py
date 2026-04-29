from flask import Flask, request, jsonify
import json

app = Flask(__name__)


# FUNÇÕES DE CARREGAR E SALVAR ////////////////////////////////////////////////

def carregar_alimentos():
    with open("alimentos.json", "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_alimentos(alimentos):
    with open("alimentos.json", "w", encoding="utf-8") as f:
        json.dump(alimentos, f, ensure_ascii=False, indent=2)

def carregar_doadores():
    with open("doadores.json", "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_doadores(doadores):
    with open("doadores.json", "w", encoding="utf-8") as f:
        json.dump(doadores, f, ensure_ascii=False, indent=2)

def carregar_instituicoes():
    with open("instituicoes.json", "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_instituicoes(instituicoes):
    with open("instituicoes.json", "w", encoding="utf-8") as f:
        json.dump(instituicoes, f, ensure_ascii=False, indent=2)

# ROTAS GET - ALIMENTOS ///////////////////////////////////////////////////////

@app.get("/alimentos")
def listar_alimentos():
    alimentos = carregar_alimentos()
    nome = request.args.get("nome", "").strip().lower()
    quantidade = request.args.get("quantidade", "").strip()
    resultado = alimentos
    if nome:
        resultado = [a for a in resultado if nome in a["nome"].lower()]
    if quantidade:
        resultado = [a for a in resultado if str(a["quantidade"]) == quantidade]
    if not resultado:
        return jsonify({"erro": "nenhum alimento encontrado"})   
    return jsonify(resultado), 200

@app.get("/alimentos/<int:id>")
def obter_alimento(id):
    alimentos = carregar_alimentos()
    for alimento in alimentos:
        if alimento["id"] == id:
            return jsonify(alimento), 200
    return jsonify({"erro": "Alimento não encontrado"}), 404

# ROTAS GET - DOADORES ////////////////////////////////////////////////////////

@app.get("/doadores")
def listar_doadores():
    doadores = carregar_doadores()
    nome = request.args.get("nome", "").strip().lower()
    email = request.args.get("email", "").strip().lower()
    resultado = doadores
    if nome:
        resultado = [d for d in resultado if nome in d["nome"].lower()]
    if email:
        resultado = [d for d in resultado if email in d["email"].lower()]
    if not resultado:
        return jsonify({"erro": "nenhum doador encontrado"})   
    return jsonify(resultado), 200

@app.get("/doadores/<int:id>")
def obter_doador(id):
    doadores = carregar_doadores()
    for doador in doadores:
        if doador["id"] == id:
            return jsonify(doador), 200
        
    return jsonify({"erro": "Doador não encontrado"}), 404

# ROTAS GET - INSTITUIÇÕES ////////////////////////////////////////////////////

@app.get("/instituicoes")
def listar_instituicoes():
    instituicoes = carregar_instituicoes()
    nome = request.args.get("nome", "").strip().lower()
    resultado = instituicoes
    if nome:
        resultado = [i for i in resultado if nome in i["nome"].lower()]
    if not resultado:
        return jsonify({"erro": "Nenhuma instituição encontrada"}), 404
    return jsonify(resultado), 200

@app.get("/instituicoes/<int:id>")
def obter_instituicao(id):
    instituicoes = carregar_instituicoes()
    for instituicao in instituicoes:
        if instituicao["id"] == id:
            return jsonify(instituicao), 200
    return jsonify({"erro": "Instituição não encontrada"}), 404

# ROTAS POST - ALIMENTOS //////////////////////////////////////////////////////

@app.post("/alimentos")
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
    alimentos = carregar_alimentos()
    novo_id = max((a["id"] for a in alimentos), default=0) + 1
    alimento = {"id": novo_id, "nome": dados_req["nome"], "quantidade": dados_req["quantidade"]}
    alimentos.append(alimento)
    salvar_alimentos(alimentos)
    return jsonify(alimento), 201

# ROTAS POST - DOADORES ///////////////////////////////////////////////////////
@app.post("/doadores")
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
    doadores = carregar_doadores()
    novo_id = max((d["id"] for d in doadores), default=0) + 1
    doador = {"id": novo_id, "nome": dados_req["nome"], "email": dados_req["email"]}
    doadores.append(doador)
    salvar_doadores(doadores)
    return jsonify(doador), 201

# ROTAS POST - INSTITUIÇÕES ///////////////////////////////////////////////////

@app.post("/instituicoes")
def cadastrar_instituicao():
    dados_req = request.json
    if not dados_req:
        return jsonify({"erro": "Corpo da requisição ausente ou inválido"}), 400
    if "nome" not in dados_req:
        return jsonify({"erro": "Campo 'nome' é obrigatório"}), 400
    if not isinstance(dados_req["nome"], str):
        return jsonify({"erro": "Campo 'nome' deve ser um texto"}), 422
    instituicoes = carregar_instituicoes()
    novo_id = max((i["id"] for i in instituicoes), default=0) + 1
    instituicao = {"id": novo_id, "nome": dados_req["nome"]}
    instituicoes.append(instituicao)
    salvar_instituicoes(instituicoes)
    return jsonify(instituicao), 201

# ROTAS PUT - ALIMENTOS ///////////////////////////////////////////////////////

@app.put("/alimentos/<int:id>")
def atualizar_alimento(id):
    dados_req = request.json
    if not dados_req:
        return jsonify({"erro": "Corpo da requisição ausente ou inválido"}), 400
    alimentos = carregar_alimentos()
    for alimento in alimentos:
        if alimento["id"] == id:
            if "nome" in dados_req:
                alimento["nome"] = dados_req["nome"]
            if "quantidade" in dados_req:
                alimento["quantidade"] = dados_req["quantidade"]
            salvar_alimentos(alimentos)
            return jsonify(alimento), 200
    return jsonify({"erro": "Alimento não encontrado"}), 404

# ROTAS PUT - DOADORES ////////////////////////////////////////////////////////

@app.put("/doadores/<int:id>")
def atualizar_doador(id):
    dados_req = request.json
    if not dados_req:
        return jsonify({"erro": "Corpo da requisição ausente ou inválido"}), 400
    doadores = carregar_doadores()
    for doador in doadores:
        if doador["id"] == id:
            if "nome" in dados_req:
                doador["nome"] = dados_req["nome"]
            if "email" in dados_req:
                doador["email"] = dados_req["email"]
            salvar_doadores(doadores)
            return jsonify(doador), 200

    return jsonify({"erro": "Doador não encontrado"}), 404

# ROTAS PUT - INSTITUIÇÕES ////////////////////////////////////////////////////

@app.put("/instituicoes/<int:id>")
def atualizar_instituicao(id):
    dados_req = request.json
    if not dados_req:
        return jsonify({"erro": "Corpo da requisição ausente ou inválido"}), 400
    instituicoes = carregar_instituicoes()
    for instituicao in instituicoes:
        if instituicao["id"] == id:
            if "nome" in dados_req:
                instituicao["nome"] = dados_req["nome"]
            salvar_instituicoes(instituicoes)
            return jsonify(instituicao), 200
    return jsonify({"erro": "Instituição não encontrada"}), 404

# ROTAS DELETE - ALIMENTOS ////////////////////////////////////////////////////

@app.delete("/alimentos/<int:id>")
def deletar_alimento(id):
    alimentos = carregar_alimentos()
    for alimento in alimentos:
        if alimento["id"] == id:
            alimentos.remove(alimento)
            salvar_alimentos(alimentos)
            return jsonify({"mensagem": "Alimento deletado com sucesso"}), 200
    return jsonify({"erro": "Alimento não encontrado"}), 404

# ROTAS DELETE - DOADORES /////////////////////////////////////////////////////

@app.delete("/doadores/<int:id>")
def deletar_doador(id):
    doadores = carregar_doadores()
    for doador in doadores:
        if doador["id"] == id:
            doadores.remove(doador)
            salvar_doadores(doadores)
            return jsonify({"mensagem": "Doador deletado com sucesso"}), 200
    return jsonify({"erro": "Doador não encontrado"}), 404

# ROTAS DELETE - INSTITUIÇÕES /////////////////////////////////////////////////
@app.delete("/instituicoes/<int:id>")
def deletar_instituicao(id):
    instituicoes = carregar_instituicoes()
    for instituicao in instituicoes:
        if instituicao["id"] == id:
            instituicoes.remove(instituicao)
            salvar_instituicoes(instituicoes)
            return jsonify({"mensagem": "Instituição deletada com sucesso"}), 200
    return jsonify({"erro": "Instituição não encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)