from fastapi import (
    Query, Path, Body, Response, status, HTTPException, APIRouter
)
from typing import List
from app.schemas.role import Role, RoleResponse
from app.database import database, roles


roles_router = APIRouter(prefix="/roles")

@roles_router.post("/")
async def create_role(
        role: Role = Body(
            ...,
            **Role.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "cliente",
                    }
                }
            }
        )) -> RoleResponse:
    """
    Cria tipo de usuário (role).
    Returns:
        Id do role criado.
    """
    # Levanta exeção se tipo de usuário ja estiver cadastrado
    if roles.select().where(
            roles.c.name == role.name):
        raise HTTPException(
            status_code=401,
            detail="Tipo de úsuario já existe"
        )

    # Cria comando SQL para inserir tipo de
    # usuário na tabela e executa
    query = roles.insert().values(
        **role.model_dump(exclude_unset=True))
    last_record_id = await database.execute(query)

    # Retorna tipo de úsuario inserido e id correspondente
    return RoleResponse(
        id=last_record_id, **role.model_dump()
    )

@roles_router.get(
    "/{role_id}",
    summary="Mostra tipo de usuário pelo id",
    response_model=RoleResponse,
)
async def view_role_by_id(
    role_id: int = Path(..., title="id da entrada")
) -> RoleResponse:
    """
    Mostra um tipo de usuário pelo id.
    Returns:
        Detalhes do tipo de usúario.
    """
    # Consultar o banco de dados para obter
    # o tipo de usuário com base no id
    role_exists = await database.fetch_one(
        roles.select().where(
            roles.c.id == role_id)
    )

    # Se o ingrediente não for encontrado,levanta uma exceção
    if not role_exists:
        raise HTTPException(
            status_code=404,
            detail="Tipo de usuário não encontrado",
        )

    # Seleciona receita no banco de dados e a retorna
    query = roles.select().where(
        roles.c.id == role_id
    )
    return await database.fetch_one(query)

@roles_router.get(
    "/{role_name}",
    summary="Mostra tipo de usuário pelo nome",
    response_model=RoleResponse,
)
async def view_role_by_name(
    role: int = Path(..., title="nome da entrada")
) -> RoleResponse:
    """
    Mostra um tipo de usuário pelo nome.
    Returns:
        Detalhes do tipo de usúario.
    """
    # Consultar o banco de dados para obter
    # o tipo de usuário com base no nome
    role_exists = await database.fetch_one(
        roles.select().where(
            roles.c.id == role)
    )

    # Se o ingrediente não for encontrado,levanta uma exceção
    if not role_exists:
        raise HTTPException(
            status_code=404,
            detail="Tipo de usuário não encontrado",
        )

    # Seleciona receita no banco de dados e a retorna
    query = roles.select().where(
        roles.c.id == role
    )
    return await database.fetch_one(query)

@roles_router.get(
    "/",
    summary="Mostra tipos de úsuario",
    response_description="Tipos de úsuarios registradas",
    response_model=List[RoleResponse],
)
async def view_roles(
    query: list = Query(
        default_factory=list,
        title="Tipos de úsuarios",
        description="Tipos de úsuarios cadastrados",
        alias="abc",
    ),
    limit: int = Query(default=10, ge=1, le=50),
):
    """
    Return:
        Mostra tipos de úsuarios cadastrados
        de acordo com o limite de quantidade.
    """
    # Seleciona e retorna tipos de úsuarios
    # baseado no limite passado e retorna
    query = roles.select().order_by(
        roles.c.id).limit(limit)
    return await database.fetch_all(query)

@roles_router.put("/{role_id}")
async def update_role(
    role_id: int = Path(..., title="id da entrada"),
    role: Role = Body(
        ..., **Role.model_config
)) -> RoleResponse:
    """
    Altera tipo de usuário pelo id
    Returns:
        Tipo de usuário com as alterações realizadas
        e id correspondente
    """
    # Verifica se o tipo de usuário com id de entrada
    # existe para ser modificado
    role_exists = await database.fetch_one(
        roles.select().where(
            roles.c.id == role_id)
    )
    # Caso não exista levanta uma exceção
    if not role_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de usuário não encontrado",
        )

    # Executa a alteração e a retorna junto ao id correspondente
    await database.execute(
        roles.update().where(
            roles.c.id == role_id).values(
                **role.model_dump(exclude_unset=True))
    )
    return RoleResponse(
        id=role_id, **role.model_dump()
    )

@roles_router.delete("/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
        role_id: int = Path(..., title="id do tipo de usuário"),
):
    """
    Deleta tipo de usuário pelo id
    Returns:
        Status da execução
    """
    # Verifica pelo id de entrada se o tipo de
    # usuário existe para ser modificado
    role_exists = await database.fetch_one(
        roles.select().where(
            roles.c.id == role_id)
    )

    # Caso não exista levanta uma exceção
    if not role_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de usuário não existe",
        )

    # Executa e retorna a alteração
    await database.execute(
        roles.delete().where(
            roles.c.id == role_id)
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


