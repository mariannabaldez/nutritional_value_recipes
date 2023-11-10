from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


#Testes para a rota create_user
def test_sucess_create_and_delete_new_user():
    """ Teste de sucesso
        Cria um usuário e o deleta
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria novo usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/users/",
            json={
                "username": "test user",
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == response.json()['id']

    # Deleta tipo de usuário e usuário criados
    with TestClient(app) as c:
        role_response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )
        response = c.delete(
            f"/api/v1/users/{response.json()['id']}"
        )

def test_failed_already_exists_create_user():
    """ Teste falho
        Cria um novo usuário que já
        existe no banco de dados.
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria novo usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/users/",
            json={
                "username": "test user",
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == response.json()['id']

    # Cria o usuário novamente garantindo que ele já existe
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/users/",
            json={
                "username": "test user",
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )

    # Verifica se response corresponde
    assert invalid_response.status_code == 401
    assert invalid_response.detail == "Usuário já existe"

    # Deleta tipo de usuário e usuário criados
    with TestClient(app) as c:
        role_response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )
        response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )

def test_failed_create_user():
    """ Teste falho
        Cria um novo usuário
    """
    # Cria usuário sem passar o atributo id_role
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/users/",
            json={
                "username": "test user",
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": None
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"

def test_failed_create_user_two():
    """ Teste falho
        Cria um novo usuário passando o atributo
        username com tipo inválido
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria tipo de usuário
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/users/",
            json={
                "username": 2,
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"

def test_failed_create_user_tree():
    """ Teste falho
        Cria um novo usuário passando o atributo
        name com tipo inválido
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria tipo de usuário
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/users/",
            json={
                "username": True,
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"

def test_failed_create_user_four():
    """ Teste falho
        Cria um novo usuário passando o atributo
        name com tipo inválido
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria tipo de usuário
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/users/",
            json={
                "username": 4.8,
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"


#Testes para a rota view_user_by_id
def test_sucess_view_user_by_id():
    """ Teste de sucesso
        Busca usuário pelo id
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria novo usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/users/",
            json={
                "username": "test user",
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == response.json()['id']

    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            f"/api/v1/users/{response.json()['id']}"
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "username": "test user",
        "hashed_password": "testpassword",
        "full_name": "test name complete",
        "email": "email@test.com",
        "desable": False,
        "id_role": test_role_id
    }

    # Deleta tipo de usuário criado
    with TestClient(app) as c:
        role_response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )
        response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )

def test_failed_view_user_by_id_not_found():
    """ Teste falho
        Busca usuário por um id que não existe
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/users/99999999999999"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_view_role_by_id():
    """ Teste falho
        Busca usuário por um id inexistente
    """
    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/users/0"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_view_role_by_id_two():
    """ Teste falho
        Busca usuário por um id com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/users/True"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_view_role_by_id_tree():
    """ Teste falho
        Busca usuário por um id com tipo diferente
    """
    # Busca usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/users/1.5"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"


#Testes para a rota view_user_by_name
def test_sucess_view_user_by_name():
    """ Teste de sucesso
        Busca usuário pelo username
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria novo usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/users/",
            json={
                "username": "test_user",
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == response.json()['id']

    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/users/test_user"
        )

    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "username": "test_user",
        "hashed_password": "testpassword",
        "full_name": "test name complete",
        "email": "email@test.com",
        "desable": False,
        "id_role": test_role_id
    }

    # Deleta tipo de usuário criado
    with TestClient(app) as c:
        role_response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )
        response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )

def test_failed_not_found_view_user_by_name():
    """ Teste falho
        Busca usuário por um username que não existe
    """
    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/users/invalido"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"


# Testes para a rota update_user
def test_sucess_update_user():
    """ Teste de sucesso
        Altera usuário existente
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria novo usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/users/",
            json={
                "username": "test user",
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == response.json()['id']

    # Altera tipo de usuário criado
    with TestClient(app) as c:
        response = c.update(
            f"/api/v1/users/{response.json()['id']}",
            json={
                "username": "test user updated"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "username": "test user updated",
        "hashed_password": "testpassword",
        "full_name": "test name complete",
        "email": "email@test.com",
        "desable": False,
        "id_role": test_role_id
    }

    # Deleta tipo de usuário criado
    with TestClient(app) as c:
        role_response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )
        response = c.delete(
            f"/api/v1/roles/{response.json()['id']}"
        )

def test_failed_update_user_not_found():
    """ Teste de sucesso
        Tenta atualizar usuário por um id que não existe
    """
    # Entrada com id inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/users/0",
            json={
                "username": "test user updated"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_update_user():
    """ Teste de sucesso
        Tenta atualizar usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/users/invalid_id",
            json={
                "username": "test user updated"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_update_user_two():
    """ Teste de sucesso
        Tenta atualizar usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/users/True",
            json={
                "username": "test user updated"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_update_user_tree():
    """ Teste de sucesso
        Tenta atualizar usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/users/1.5",
            json={
                "username": "test user updated"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"


# Testes para a rota delete_user
def test_sucess_delete_role():
    """ Teste de sucesso
        Altera tipo de usuário existente
    """
    # Cria novo tipo de usuário que será
    # usado para criar novo usuário
    with TestClient(app) as c:
        role_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )

    test_role_id = role_response.json()['id']
    # Verifica se response corresponde
    assert role_response.status_code == 200
    assert role_response.json() == role_response.json()['id']

    # Cria novo usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/users/",
            json={
                "username": "test user",
                "hashed_password": "testpassword",
                "full_name": "test name complete",
                "email": "email@test.com",
                "desable": False,
                "id_role": test_role_id
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == response.json()['id']

    with TestClient(app) as c:
        delete_response = c.delete(
            f"/api/v1/users/{response.json()['id']}"
        )
    # Verifica se response corresponde
    assert delete_response.status_code == 204

def test_failed_delete_role_not_found():
    """ Teste de sucesso
        Tenta deletar usuário por um id que não existe
    """
    # Entrada com id inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/users/0")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_delete_role():
    """ Teste de sucesso
        Tenta deletar usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/users/invalid_id")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_delete_role_two():
    """ Teste de sucesso
        Tenta deletar usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/users/True")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"

def test_failed_delete_role_tree():
    """ Teste de sucesso
        Tenta deletar usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update("/api/v1/users/1.5")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Usuário não encontrado"
