from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from . import crud, models, schemas, database
from .auth import authenticate_user, create_access_token, get_current_active_user

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=database.engine)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API Bancário de Maeli!"}

# Rotas protegidas para clientes
@app.post("/clientes/", response_model=schemas.Cliente, tags=["Clientes"])
def create_cliente_endpoint(cliente: schemas.ClienteCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_cliente = crud.get_cliente_by_cpf(db, cpf=cliente.cpf)
    if db_cliente:
        raise HTTPException(status_code=400, detail="CPF já registrado")
    return crud.create_cliente(db, cliente=cliente)

@app.get("/clientes/{cpf}", response_model=schemas.Cliente, tags=["Clientes"])
def read_cliente(cpf: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_cliente = crud.get_cliente_by_cpf(db, cpf=cpf)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

# Rotas protegidas para transações
@app.post("/depositar/", response_model=schemas.Transacao, tags=["Transações"])
def depositar_endpoint(deposito: schemas.DepositoCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_active_user)):
    cliente = crud.get_cliente_by_cpf(db, cpf=deposito.cpf)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.depositar(db, cliente_id=cliente.id, valor=deposito.valor)

@app.post("/sacar/", response_model=schemas.Transacao, tags=["Transações"])
def sacar_endpoint(saque: schemas.SaqueCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_active_user)):
    cliente = crud.get_cliente_by_cpf(db, cpf=saque.cpf)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.sacar(db, cliente_id=cliente.id, valor=saque.valor)

@app.get("/contas/{cpf}", response_model=List[schemas.Conta], tags=["Contas"])
def listar_contas(cpf: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_active_user)):
    cliente = crud.get_cliente_by_cpf(db, cpf=cpf)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.get_contas_cliente(db, cliente_id=cliente.id)

@app.get("/extrato/{cpf}", response_model=List[schemas.Transacao], tags=["Transações"])
def extrato_endpoint(cpf: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_active_user)):
    cliente = crud.get_cliente_by_cpf(db, cpf=cpf)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.get_extrato(db, cliente_id=cliente.id)
