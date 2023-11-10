from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.nutritional_value_recipe import (
    NutritionalValueRecipe, NutritionalValueRecipeResponse
)
from app.database import (
    database, recipes, nutritional_value_recipes
)
import sqlalchemy as sa
import re
import json

nutritional_value_recipes_router = \
    APIRouter(prefix="/nutritional_value")

@nutritional_value_recipes_router.post("/")
async def create_nutritional_value_recipe(
    nutritional_value_recipe: NutritionalValueRecipe = Body(
        ...,
        **NutritionalValueRecipe.model_config,
        openapi_examples={
            "normal": {
            "summary": "Um exemplo normal",
            "description": "Um exemplo normal",
            "value": {
                "id_recipe": 1,
                "nutritional_value_ingredients": {
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
                }
            }
        }}
)) -> NutritionalValueRecipeResponse:

    # Verifica se o id da receita de entrada passado
    # em id_recipe existe na tabela recipes
    recipe_exists = await database.fetch_one(
        recipes.select().where(
            recipes.c.id == nutritional_value_recipe.id_recipe)
    )

    if not recipe_exists:
        raise HTTPException(
            status_code=404,
            detail="Receita não encontrada para ser" + \
                "calculado valores nutricionais",
        )

    # Captura ingredientes da receita de entrada
    ingredientes = await database.fetch_one(
        recipes.select(recipes.c.ingredients).where(
            recipes.c.id == nutritional_value_recipe.id_recipe)
    )

    #  Busca os valores nutricionais de cada ingrediente



    # Cria comando SQL para inserir valor nutricional
    # dos ingredientes da receita passada pelo id_recipe
    # e executa salvando id da query
    query = nutritional_value_recipes.insert()