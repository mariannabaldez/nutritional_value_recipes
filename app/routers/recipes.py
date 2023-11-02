from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.recipe import Recipe, RecipeResponse
from app.database import database, recipes, ingredients


recipes_router = APIRouter(prefix="/recipes")

@recipes_router.post("/")
async def create_recipes(
        recipe: Recipe = Body(
            ...,
            **Recipe.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "empadao de frango",
                        "descript": \
                            "Em uma panela, aqueça o óleo e " + \
                            "refogue o arroz até que os grãos  " + \
                            "estejam esbranquiçados, após " + \
                            "acrescente a cebola, o alho e " + \
                            "refogue. Adicione a água, " + \
                            "acrescente o sal e espere " + \
                            "pela fervura para abaixar o fogo " + \
                            "para médio. Após a água reduzir e o " + \
                            "arroz estiver quase seco, tampe a " + \
                            "panela e deixe o fogo no minimo por " + \
                            "5 minutos e em seguida desligue o fogo.",
                        "ingredients": {
                            "farinha de trigo": {"gramas": 300},
                            "ovo": {"unidade": 3},
                            "manteiga": {"colheres": 3},
                            "peito de frango desfiado": {"gramas": 600},
                        }
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "name": "empadao de frango",
                        "descript": "",
                        "ingredients": [
                            "frango",
                            "farinha de trigo"
                        ]
                    },
                },
            }
        )) -> RecipeResponse:
    # Checando se a receita já existe na base
    query = recipes.select().where(
        (recipes.c.name == recipe.name)
    )
    recipe_exists = await database.fetch_one(query)

    if recipe_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Receita já existe",
        )

    # Cria comando SQL para inserir nome e
    # descrição de preparo na tabela recipes e executa
    query_recipe = recipes.insert().values(
        name=recipe.name, descript=recipe.descript)
    last_record_id = await database.execute(query_recipe)

    # Cria comando SQL executar a inserção do id da receita,
    # dos nomes, quantidades e unidade de medida dos
    # ingredientes da receita na tabela ingredients
    for name, value in recipe.ingredients.items():
        for measure, quantity in value.items():
            await database.execute(
                ingredients.insert().values(
                    id_recipe=last_record_id,
                    name=name,
                    measure=measure,
                    quantity=quantity,
                )
            )

    return RecipeResponse(id=last_record_id)
