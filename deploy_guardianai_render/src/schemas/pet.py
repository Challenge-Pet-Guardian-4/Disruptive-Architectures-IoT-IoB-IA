"""
Schemas Pydantic: Contexto do Animal de Estimação
"""
from typing import Optional, Union
from pydantic import BaseModel, Field

class PetContextPayload(BaseModel):
    id: Optional[int] = Field(default=None, description="Identificador único do pet")
    nome: Optional[str] = Field(default=None, description="Nome do pet")
    raca: Optional[str] = Field(default=None, description="Raça do pet")
    porte: Optional[str] = Field(default=None, description="Porte do pet: 'pequeno', 'medio' ou 'grande'")
    dataNasc: Optional[str] = Field(default=None, description="Data de nascimento do pet")
    idade: Optional[int] = Field(default=None, description="Idade em anos do pet")
    sexo: Optional[str] = Field(default=None, description="Sexo do pet: 'macho' ou 'femea'")
    castrado: Optional[bool] = Field(default=None, description="Indicador de castração")
    peso: Optional[Union[str, float, int]] = Field(default=None, description="Peso do pet em kg")
    alergias: Optional[str] = Field(default=None, description="Histórico de alergias conhecidas")
    medicamentos: Optional[str] = Field(default=None, description="Medicamentos de uso contínuo")
    ultimaVacina: Optional[str] = Field(default=None, description="Data da última vacinação administrada")
    ultimaConsulta: Optional[str] = Field(default=None, description="Data do último atendimento veterinário")
