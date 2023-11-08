from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.recipe import Recipe, RecipeResponse
from app.database import database, recipes
import sqlalchemy as sa
import re
import json

recipes_router = APIRouter(prefix="/recipes")

@recipes_router.post("/")
async def create_recipe(
    recipe: Recipe = Body(
        ...,
        **Recipe.model_config,
        openapi_examples={
            "normal": {
                "summary": "Um exemplo normal",
                "description": "Um exemplo normal",
                "value": {
                    "name": "arroz",
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
                    }
                }
            }}
)) -> RecipeResponse:

    # Transforma ingredients da entrada em JSON
    ingredients_json = json.dumps(recipe.ingredients)

    # Verifica se receita já existe verificando se
    # os ingredientes, unidades de medidas e
    # quantidades deles são os mesmos
    ingredients_exists = await database.fetch_one(
        recipes.select().where(
            recipes.c.ingredients == ingredients_json)
    )
    if ingredients_exists:
        raise HTTPException(
            status_code=401,
            detail="Receita já existe",
        )

    # Cria comando SQL para inserir receita
    # na tabela recipes se todos os dados
    # estiverem preenchidos perante ao modelo e executa
    if recipe.name and recipe.descript and recipe.ingredients:
        query_recipe = recipes.insert().values(
            name=recipe.name,
            descript=recipe.descript,
            ingredients=recipe.ingredients)
        last_record_id = await database.execute(query_recipe)

    else: raise HTTPException(
            status_code=400,
            detail="Bad Request",
        )

    # Retorna detalhes da receita criada e id correspondente
    return RecipeResponse(id=last_record_id, **recipe.model_dump())

@recipes_router.get(
    "/{recipe_id}",
    summary="Mostra uma unica receita pelo id",
    response_description="Detalhes da receita",
    response_model=RecipeResponse,
)
async def view_recipe_by_id(
    recipe_id: int = Path(..., title="id da entrada"),
) -> RecipeResponse:
    """
    Mostra os detalhes de uma receita.
    Returns:
        Detalhes da receita.
    """
    # Consultar o banco de dados para obter
    # a receita com base no id
    recipe_exists = await database.fetch_one(
        recipes.select().where(
        recipes.c.id == recipe_id)
    )

    # Se a receita não for encontrada,levanta uma exceção
    if not recipe_exists:
        raise HTTPException(
            status_code=404,
            detail="Receita não encontrada",
        )

    # Seleciona receita no banco de dados e a retorna
    query = recipes.select().where(
        recipes.c.id == recipe_id
    )
    return await database.fetch_one(query)

@recipes_router.get(
    "/{recipe_name}",
    summary="Mostra uma unica receita pelo nome",
    response_description="Detalhes da receita",
    response_model=RecipeResponse,
)
async def view_recipe_by_name(
    recipe: int = Path(..., title="nome da entrada"),
) -> RecipeResponse:
    """
    Mostra os detalhes de uma receita.
    Returns:
        Detalhes da receita.
    """
    # Consultar o banco de dados para obter
    # a receita com base no nome
    recipe_exists = await database.fetch_one(
        recipes.select().where(
        recipes.c.name == recipe)
    )

    # Se o ingrediente não for encontrado,levanta uma exceção
    if not recipe_exists:
        raise HTTPException(
            status_code=404,
            detail="Receita não encontrada",
        )

    # Seleciona receita no banco de dados e a retorna
    query = recipes.select().where(
        recipes.c.name == recipe
    )
    return await database.fetch_one(query)

@recipes_router.get(
    "/",
    summary="Mostra receitas",
    response_description="Receitas registradas",
    response_model=List[RecipeResponse],
)
async def view_recipes(
    query: list = Query(
        default_factory=list,
        title="Query string",
        description="Query string para filtrar os items",
        alias="abc",
    ),
    limit: int = Query(default=10, ge=1, le=50),
):
    """
    Mostra receitas
    """
    # Seleciona e retorna receitas baseado
    # no limite passado de forma decrescente
    query = recipes.select().order_by(
            recipes.c.id.desc()).limit(limit)

    return await database.fetch_all(query)

@recipes_router.put("/{recipe_id}")
async def update_recipe(
    recipe_id: int = Path(..., title="id da receita"),
    recipe: Recipe = Body(
        ...,
        **Recipe.model_config
)) -> RecipeResponse:
    """
    Altera receita pelo id
    Returns:
        Receita com as alterações realizadas e id correspondente
    """
    # Verifica se a receita com id de entrada
    # existe para ser modificada
    recipe_exists = await database.fetch_one(
        recipes.select().where(
            recipes.c.id == recipe_id)
    )
    # Caso não exista levanta uma exceção
    if not recipe_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receita não encontrada",
        )

    # Executa e retorna a alteração
    await database.execute(
        recipes.update().where(
            recipes.c.id == recipe_id).values(
                **recipe.model_dump(exclude_unset=True))
    )
    return RecipeResponse(
        id=recipe_id, **recipe.model_dump()
    )

@recipes_router.delete("/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
        recipe_id: int = Path(..., title="id da receita"),
):
    """
    Deleta receita pelo id
    Returns:
        Status da execução
    """
    # Verifica se a receita com id de entrada
    # existe para ser modificada
    recipe_exists = await database.fetch_one(
        recipes.select().where(
            recipes.c.id == recipe_id)
    )

    # Caso não exista levanta uma exceção
    if not recipe_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receita não existe",
        )

    # Executa e retorna a alteração
    await database.execute(
        recipes.delete().where(
            recipes.c.id == recipe_id)
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
