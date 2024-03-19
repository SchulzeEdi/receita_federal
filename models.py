from . import db
from sqlalchemy.sql import func

class Empresa(db.Model):
  __tablename__ = "Empresa"
  id = db.Column(db.BigInteger, primary_key=True)
  cnpj = db.Column(db.String(14), nullable=False)
  situacao = db.Column(db.Boolean, default=True)
  tipo = db.Column(db.String)
  nome = db.Column(db.String, nullable=True)
  fantasia = db.Column(db.String, nullable=True)
  uf = db.Column(db.String, nullable=True)
  municipio = db.Column(db.String, nullable=True)
  endereco = db.Column(db.String, nullable=True) 
  natureza_juridica = db.Column(db.String, nullable=True)
  porte = db.Column(db.String, nullable=True)
  atividade_principal = db.Column(db.String, nullable=True)
  telefone = db.Column(db.BigInteger, nullable=True)
  num_funcionarios = db.Column(db.Integer, nullable=True)
  faturamento_anual = db.Column(db.Float, nullable=True)
  vendedor_responsavel = db.Column(db.String, nullable=True)
  data_criacao = db.Column(db.DateTime(timezone=True), server_default=func.now())

  def __repr__(self):
    return f'<Empresa {self.cnpj} {self.id}>'
