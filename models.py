from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    data_nascimento = Column(String)
    endereco = Column(String)

    contas = relationship("Conta", back_populates="cliente")

class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, index=True)
    saldo = Column(Float, default=0.0)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="contas")
    transacoes = relationship("Transacao", back_populates="conta")

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    valor = Column(Float)
    data = Column(DateTime)
    conta_id = Column(Integer, ForeignKey("contas.id"))

    conta = relationship("Conta", back_populates="transacoes")
