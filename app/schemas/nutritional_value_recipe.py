#pylint: disable=E0213

import re
from pydantic import BaseModel, Field
from typing import Dict, Union, Optional


class NutritionalValueRecipe(BaseModel):
    """
        Modelo de valor nutricional de todos
        os ingredientes da receita
    """
    id_recipe: int

    nutritionl_value_ingredients: Optional[
        Dict[str, Dict[str, Union[str, float]]]
    ] = Field(..., example={
        "arroz": {
            "calories": 600,
            "protein": 29,
            "carbo": 120,
            "saturated_fat": 12,
            "polyunsaturated_fat": 0,
            "monounsaturated_fat": 0,
            "fiber": 35,
            "sugar": 9,
            "sodium": 0.120,
            "potassium": 0.355
        },
        "alho": {
            "calories": 15,
            "protein": 0.1,
            "carbo": 0,
            "saturated_fat": 0,
            "polyunsaturated_fat": 0,
            "monounsaturated_fat": 0,
            "fiber": 0,
            "sugar": 0,
            "sodium": 0,
            "potassium": 0.3
        },
        "cebola": {
            "calories": 22,
            "protein": 0.1,
            "carbo": 0,
            "saturated_fat": 0,
            "polyunsaturated_fat": 0,
            "monounsaturated_fat": 0,
            "fiber": 0,
            "sugar": 0,
            "sodium": 0,
            "potassium": 0.3
        },
        "azeite": {
            "calories": 100,
            "protein": 2,
            "carbo": 0,
            "saturated_fat": 9.3,
            "polyunsaturated_fat": 1,
            "monounsaturated_fat": 2,
            "fiber": 0,
            "sugar": 0,
            "sodium": 0.523,
            "potassium": 0.3
        },
        "sal": {
            "calories": 2,
            "protein": 0,
            "carbo": 0,
            "saturated_fat": 0,
            "polyunsaturated_fat": 0,
            "monounsaturated_fat": 0,
            "fiber": 0,
            "sugar": 0,
            "sodium": 1.222,
            "potassium": 0
        }
    })


class NutritionalValueRecipeResponse(NutritionalValueRecipe):
    """
        Modelo de resposta de de valor nutricional
        de todos os ingredientes da receita
    """
    id: int