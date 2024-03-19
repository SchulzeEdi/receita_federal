from . import app, db
from flask import request, make_response, render_template, jsonify
import http.client
from .models import Empresa
import json

@app.route('/', methods=['GET'])
def cadastro_empresa():
    return render_template('index.html')

@app.route('/alterar_empresa_form/', methods=['GET'])
def alterar_empresa_form():
  empresa_id = request.args.get('id')
  empresa = Empresa.query.filter_by(id=empresa_id).first()
  return render_template('alterar_empresa.html', empresa=empresa)

@app.route('/consulta_empresa', methods=['GET'])
def consulta_empresa():
  empresas = Empresa.query.all()
  return render_template('consulta_empresa.html', empresas=empresas)

@app.route('/consulta_empresa_filter', methods=['POST'])
def consulta_empresa_filter():
  vendedor_responsavel = request.form['vendedor_responsavel']
  if vendedor_responsavel:
    empresas = Empresa.query.filter_by(vendedor_responsavel=vendedor_responsavel).all()
  else:
    empresas = Empresa.query.all()
  return render_template('consulta_empresa.html', empresas=empresas)

@app.route("/incluir_empresa", methods=["POST"])
def incluir_empresa():
  cnpj = request.form['cnpj'].replace(".", "").replace("/", "").replace("-", "")
  validaCnpj = len(cnpj)
  if  validaCnpj != 14:
    return make_response(
      {"message": "Cnpj inválido"}
    )
  empresa = Empresa.query.filter_by(cnpj=cnpj).first()
  if empresa:
    return make_response(
      {"message": "CNPJ cadastrado, consulte"}, 200
    )
  else:
    conn = http.client.HTTPSConnection("receitaws.com.br")
    headers = { 'Accept': "application/json" }
    conn.request("GET", f"/v1/cnpj/{cnpj}", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    situacao = 1
    print(data)
    if data:
      if data['status'] == "ERROR":
        return make_response(
        {"message": "Cnpj nao existe"},
        500
      )
      if data['situacao'] == "INAPTA":
        situacao = 0

      telefone = None
      if data['telefone']:
        telefone = data['telefone'].replace("(", "").replace(")", "").replace(" ", "").replace("-", "").replace("/", "")
      
      empresa = Empresa(
        cnpj = cnpj,
        situacao = situacao,
        tipo = data['tipo'],
        nome = data['nome'],
        fantasia = data['fantasia'],
        uf = data['uf'],
        municipio = data['municipio'],
        endereco = data['logradouro'],
        natureza_juridica = data['natureza_juridica'],
        porte = data['porte'],
        atividade_principal = data['atividade_principal'][0]['text'],
        telefone = telefone,
        num_funcionarios = None,
        faturamento_anual = None,
        vendedor_responsavel = None
      )
      db.session.add(empresa)
      db.session.commit()
      return make_response(
        {"message": "Empresa criada"},
        201
      )

@app.route("/alterar_empresa_dados/<cnpj>", methods=["POST"])
def alterar_empresa_dados(cnpj):
  empresa_update = Empresa.query.filter_by(cnpj=cnpj).first()
  if not empresa_update:
      return jsonify({"message": "Empresa não encontrada"}), 404
  for campo, valor in request.form.items():
    if campo == "situacao":
      valor = valor == '1'
    if campo == "num_funcionarios":
      valor = None if valor == "None" else valor
    if campo == "faturamento_anual":
      valor = None if valor == "None" else valor
    if campo == "vendedor_responsavel":
      valor = None if valor == "None" else valor
    setattr(empresa_update, campo, valor)
  db.session.commit()
  return jsonify({"message": "Empresa atualizada com sucesso."}), 200