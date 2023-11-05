#pylint: disable=E0213

import re
from pydantic import BaseModel, constr, Field, validator
from typing import Dict, Optional
from unidecode import unidecode

class IngredientsDetails(BaseModel):
    measure: str
    quantity: float

class Recipe(BaseModel):
    """ Modelo de receita culinária """
    name: constr(
        max_length=50,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
    ) = Field(..., example="empadao de frango")

    descript: Optional[constr(
        max_length=4000,
        strip_whitespace=True,
        min_length=1,
    )] = Field(None, example= \
            "Em uma panela, aqueça o óleo e refogue o arroz " + \
            "até que os grãos estejam esbranquiçados, após " + \
            "acrescente a cebola, o alho e refogue. " + \
            "Adicione a água, acrescente o sal e espere " + \
            "pela fervura para abaixar o fogo para médio. " + \
            "Após a água reduzir e o arroz estiver quase " + \
            "seco, tampe a panela e deixe o fogo no minimo " + \
            "por 5 minutos e em seguida desligue o fogo."
        )

    ingredients: Optional[
        Dict[str, IngredientsDetails]
    ] = Field(..., example={
            "arroz": {
                "measure": "gramas",
                "quantity": 150
            },
            "alho": {
                "measure": "dentes",
                "quantity": 3
            },
            "cebola": {
                "measure": "unidade",
                "quantity": 0.5
            },
            "azeite": {
                "measure": "ml",
                "quantity": 10
            },
            "sal": {
                "measure": "gramas",
                "quantity": 5
            }
        })

    @validator("name")
    def apply_unidecode(cls, v):
        """ Aplica unidecode no nome """
        return re.sub(r'[^\w\s]', '', unidecode(v))

class RecipeResponse(Recipe):
    """ Modelo de resposta de receita culinária """
    id: int
