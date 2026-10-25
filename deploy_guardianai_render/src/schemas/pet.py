"""
Schemas Pydantic: Contexto do Animal de Estimação e Prontuário Clínico Oficial
"""
from typing import Optional, List
from pydantic import BaseModel, Field

class PetHistoricoItem(BaseModel):
    id: Optional[int] = Field(default=None, description="Identificador do histórico no banco")
    tipoHist: str = Field(description="Tipo de histórico: vacina, consulta, exame ou procedimento")
    dataHist: str = Field(description="Data do registro em formato ISO ou textual")

class PetContextPayload(BaseModel):
    id: Optional[int] = Field(default=None, description="Identificador único do pet")
    nome: Optional[str] = Field(default=None, description="Nome do pet")
    raca: Optional[str] = Field(default=None, description="Raça do pet")
    porte: Optional[str] = Field(default=None, description="Porte do pet: 'pequeno', 'medio' ou 'grande'")
    dataNasc: Optional[str] = Field(default=None, description="Data de nascimento do pet")
    idade: Optional[int] = Field(default=None, description="Idade em anos do pet")
    sexo: Optional[str] = Field(default=None, description="Sexo do pet: 'macho' ou 'femea'")
    castrado: Optional[bool] = Field(default=None, description="Indicador de castração")
    historicos: Optional[List[PetHistoricoItem]] = Field(default=None, description="Histórico de eventos clínicos (vacinas, consultas, exames)")
