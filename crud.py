from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from fastapi import HTTPException

# Cliente
def get_cliente_by_cpf(db: Session, cpf: str):
    return db.query(models.Cliente).filter(models.Cliente.cpf == cpf).first()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(
        nome=cliente.nome,
        cpf=cliente.cpf,
        data_nascimento=cliente.data_nascimento,
        endereco=cliente.endereco
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Conta
def get_contas_cliente(db: Session, cliente_id: int):
    return db.query(models.Conta).filter(models.Conta.cliente_id == cliente_id).all()

def create_conta(db: Session, conta: schemas.ContaCreate, cliente_id: int):
    if not isinstance(conta.numero, int):
        raise HTTPException(status_code=400, detail="O número da conta deve ser um inteiro.")
    db_conta = models.Conta(
        numero=conta.numero,
        saldo=conta.saldo,
        cliente_id=cliente_id
    )
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta

# Transações
def depositar(db: Session, cliente_id: int, valor: float):
    if not isinstance(valor, (int, float)):
        raise HTTPException(status_code=400, detail="O valor deve ser um número.")
    conta = db.query(models.Conta).filter(models.Conta.cliente_id == cliente_id).first()
    if conta:
        if valor <= 0:
            raise HTTPException(status_code=400, detail="O valor do depósito deve ser maior que zero.")
        nova_transacao = models.Transacao(tipo="Depósito", valor=valor, data=datetime.now(), conta_id=conta.id)
        conta.saldo += valor
        db.add(nova_transacao)
        db.commit()
        db.refresh(nova_transacao)
        return nova_transacao
    raise HTTPException(status_code=404, detail="Conta não encontrada")

def sacar(db: Session, cliente_id: int, valor: float):
    if not isinstance(valor, (int, float)):
        raise HTTPException(status_code=400, detail="O valor deve ser um número.")
    conta = db.query(models.Conta).filter(models.Conta.cliente_id == cliente_id).first()
    if conta:
        if conta.saldo < valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        if valor <= 0:
            raise HTTPException(status_code=400, detail="O valor do saque deve ser maior que zero.")
        nova_transacao = models.Transacao(tipo="Saque", valor=valor, data=datetime.now(), conta_id=conta.id)
        conta.saldo -= valor
        db.add(nova_transacao)
        db.commit()
        db.refresh(nova_transacao)
        return nova_transacao
    raise HTTPException(status_code=404, detail="Conta não encontrada")

def get_extrato(db: Session, cliente_id: int):
    conta = db.query(models.Conta).filter(models.Conta.cliente_id == cliente_id).first()
    if conta:
        return db.query(models.Transacao).filter(models.Transacao.conta_id == conta.id).all()
    raise HTTPException(status_code=404, detail="Conta não encontrada")

