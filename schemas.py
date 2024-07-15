from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
import re

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class ClienteBase(BaseModel):
    nome: str = Field(..., example="João Silva")
    cpf: str = Field(..., min_length=11, max_length=11, regex="^[0-9]{11}$")
    data_nascimento: str = Field(..., example="01/01/1990")
    endereco: str = Field(..., example="Rua das Flores 123, Bairro Jardim, SP")

    @validator('nome')
    def nome_valido(cls, v):
        if not re.match(r"^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$", v):
            raise ValueError('O nome deve conter apenas letras e espaços.')
        return v

    @validator('data_nascimento')
    def data_valida(cls, v):
        try:
            datetime.strptime(v, '%d/%m/%Y')
            return v
        except ValueError:
            raise ValueError('Data inválida. Formato esperado dd/mm/aaaa')

    @validator('endereco')
    def endereco_valido(cls, v):
        if not re.match(r"^[0-9a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ,.-]+$", v):
            raise ValueError('O endereço deve conter apenas letras, números e os caracteres , . -')
        return v

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    contas: List['Conta'] = []  # Usando uma string forward declaration para evitar problemas de dependência circular

    class Config:
        orm_mode = True

class ContaBase(BaseModel):
    numero: int = Field(..., example=123456)
    saldo: float = Field(default=0.0, example=100.0)

    @validator('numero')
    def numero_valido(cls, v):
        if not isinstance(v, int):
            raise ValueError('O número da conta deve ser um inteiro.')
        return v

class ContaCreate(ContaBase):
    pass

class Conta(ContaBase):
    id: int
    cliente_id: int
    transacoes: List['Transacao'] = []

    class Config:
        orm_mode = True

class TransacaoBase(BaseModel):
    tipo: str = Field(..., example="Depósito")
    valor: float = Field(..., example=50.0)
    data: datetime = Field(default_factory=datetime.now)

    @validator('valor')
    def valor_valido(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('O valor deve ser um número.')
        if v <= 0:
            raise ValueError('O valor deve ser maior que zero.')
        return v

class DepositoCreate(TransacaoBase):
    cpf: str = Field(..., example="12345678901")

class SaqueCreate(TransacaoBase):
    cpf: str = Field(..., example="12345678901")

class Transacao(TransacaoBase):
    id: int
    conta_id: int

    class Config:
        orm_mode = True

# A declaração abaixo é para resolver as declarações forward no Pydantic
Cliente.update_forward_refs()
Conta.update_forward_refs()
