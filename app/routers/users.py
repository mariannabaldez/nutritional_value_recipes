from fastapi import (
    Query, Path, Body, Response, status, HTTPException, APIRouter
)
from typing import List
from app.schemas.user import User, UserResponse
from app.database import database, roles, users


users_router = APIRouter(prefix="/roles")

@users_router.post("/")
async def create_user(
        user: User = Body(
            ...,
            **User.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "username": "Willy",
                        "hashed_password": "chocolate",
                        "full_name": "Willy Wonka",
                        "email": "wonka@abc.com",
                        "disable": False,
                        "id_role": 1
                    }
                }
            }
        )) -> UserResponse:
    """
    Cria usuário
    Returns:
        Id do usuário criado.
    """
    # Levanta exeção se tipo de usuário não for encontrado
    role_exists = await database.fetch_one(
        roles.select().where(
            roles.c.id == user.id_role)
    )
    if not role_exists:
        raise HTTPException(
            status_code=404,
            detail="Tipo de úsuario inválido"
        )

    # Cria comando SQL para inserir usuário na tabela e executa
    query = users.insert().values(
        **user.model_dump(exclude_unset=True))
    last_record_id = await database.execute(query)

    # Retorna úsuario inserido e id correspondente
    return UserResponse(
        id=last_record_id, **user.model_dump()
    )

@users_router.get(
    "/{user_id}",
    summary="Mostra usuário pelo id",
    response_model=UserResponse,
)
async def view_user_by_id(
    user_id: int = Path(..., title="id da entrada")
) -> UserResponse:
    """
    Mostra um usuário pelo id.
    Returns:
        Detalhes do usúario.
    """
    # Consultar o banco de dados para obter
    # o usuário com base no id
    user_exists = await database.fetch_one(
        users.select().where(
            users.c.id == user_id)
    )

    # Se o usuário não for encontrado, levanta uma exceção
    if not user_exists:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado",
        )

    # Seleciona usuário no banco de dados e a retorna
    query = users.select().where(
        users.c.id == user_id
    )
    return await database.fetch_one(query)

@users_router.get(
    "/{role_name}",
    summary="Mostra um usuário pelo nome",
    response_model=UserResponse,
)
async def view_user_by_name(
    user: int = Path(..., title="nome da entrada")
) -> UserResponse:
    """
    Mostra um usuário pelo nome.
    Returns:
        Detalhes do usúario.
    """
    # Consultar o banco de dados para obter
    # o usuário com base no nome
    user_exists = await database.fetch_one(
        users.select().where(
            users.c.id == user)
    )

    # Se o ingrediente não for encontrado,levanta uma exceção
    if not user_exists:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado",
        )

    # Seleciona receita no banco de dados e a retorna
    query = users.select().where(
        users.c.name == user
    )
    return await database.fetch_one(query)

@users_router.get(
    "/",
    summary="Mostra usuários",
    response_description="Usuários registradas",
    response_model=List[UserResponse],
)
async def view_users(
    query: list = Query(
        default_factory=list,
        title="Usuários",
        description="Usuários cadastrados",
        alias="abc",
    ),
    limit: int = Query(default=10, ge=1, le=50),
):
    """
    Return:
        Mostra úsuarios cadastrados de acordo
        com o limite de quantidade.
    """
    # Seleciona úsuarios
    # baseado no limite passado e retorna
    query = users.select().order_by(
        users.c.id).limit(limit)
    return await database.fetch_all(query)

@users_router.put("/{user_id}")
async def update_user(
    user_id: int = Path(..., title="id da entrada"),
    user: User = Body(
        ..., **User.model_config
)) -> UserResponse:
    """
    Altera usuário pelo id passado
    Returns:
        Usuário com as alterações realizadas
        e id correspondente
    """
    # Verifica se o usuário com id de entrada
    # existe para ser modificado
    user_exists = await database.fetch_one(
        users.select().where(
            users.c.id == user_id)
    )
    # Caso não exista levanta uma exceção
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    # Executa a alteração e a retorna junto ao id correspondente
    await database.execute(
        users.update().where(
            users.c.id == user_id).values(
                **user.model_dump(exclude_unset=True))
    )
    return UserResponse(
        id=user_id, **user.model_dump()
    )

@users_router.delete("/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int = Path(..., title="id do usuário"),
):
    """
    Deleta usuário pelo id passado
    Returns:
        Status da execução
    """
    # Verifica pelo id de entrada se o usuário
    # existe para ser modificado
    user_exists = await database.fetch_one(
        users.select().where(
            users.c.id == user_id)
    )

    # Caso não exista levanta uma exceção
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não existe",
        )

    # Executa e retorna a alteração
    await database.execute(
        users.delete().where(
            users.c.id == user_id)
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


