from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


#Testes para a rota create_role
def test_sucess_create_new_role():
    """ Teste de sucesso
        Cria um tipo de usuário
    """
    # Cria novo tipo de usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test recipe"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == response.json()['id']

    # Deleta tipo de usuário criado
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/roles/{response.json()['id']}")

def test_failed_already_exists_create_role():
    """ Teste falho
        Cria um novo tipo de usuário que já existe
        no banco de dados.
    """
    # Cria um novo tipo de usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test role"
    }

    # Cria o tipo de usuário novamente garantindo que ele já existe
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 401
    assert invalid_response.detail == "Role já existe"

    # Deleta tipo de usuário criado
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/roles/{response.json()['id']}")

def test_failed_create_role():
    """ Teste falho
        Cria um novo tipo de usuário
    """
    # Cria tipo de usuário sem passar o atributo name
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/roles/",
            json={
                "name": None,
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"

def test_failed_create_role_two():
    """ Teste falho
        Cria uma nova tipo de usuário passando o atributo
        name com tipo inválido
    """
    # Cria tipo de usuário
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/roles/",
            json={
                "name": 1
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"

def test_failed_create_role_tree():
    """ Teste falho
        Cria uma nova receita passando o atributo
        name com tipo inválido
    """
    # Cria tipo de usuário
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/roles/",
            json={
                "name": True
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"

def test_failed_create_role_four():
    """ Teste falho
        Cria uma nova receita passando o atributo
        name com tipo inválido
    """
    # Cria tipo de usuário
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/roles/",
            json={
                "name": 3.5
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"


#Testes para a rota view_role_by_id
def test_sucess_view_role_by_id():
    """ Teste de sucesso
        Busca tipo de usuário pelo id
    """
    # Cria novo tipo de usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == response.json()['id']

    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            f"/api/v1/roles/test/{response.json()['id']}"
        )

    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test"
    }

    # Deleta tipo de usuário criado
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/roles/{response.json()['id']}")

def test_failed_view_role_by_id_not_found():
    """ Teste falho
        Busca tipo de usuário por um id que não existe
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/99999999999999"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_view_role_by_id():
    """ Teste falho
        Busca tipo de usuário por um id inexistente
    """
    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/0"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_view_role_by_id_two():
    """ Teste falho
        Busca tipo de usuário por um id com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/abc"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_view_role_by_id_tree():
    """ Teste falho
        Busca tipo de usuário por um id com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/1.5"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrada"

def test_failed_view_role_by_name_four():
    """ Teste falho
        Busca tipo de usuário por um id com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/True"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrada"


#Testes para a rota view_role_by_name
def test_sucess_view_role_by_name():
    """ Teste de sucesso
        Busca tipo de usuário pelo nome
    """
    # Cria novo tipo de usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test"
    }

    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/test"
        )

    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test"
    }

    # Deleta tipo de usuário criado
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/roles/{response.json()['id']}")

def test_failed_not_found_view_role_by_name():
    """ Teste falho
        Busca tipo de usuário por um name que não existe
    """
    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/invalido"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_view_role_by_name():
    """ Teste falho
        Busca tipo de usuário por um name com tipo diferente
    """
    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/0"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_view_role_by_name_two():
    """ Teste falho
        Busca tipo de usuário por um name com tipo diferente
    """
    # Busca tipo de usuário
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/1.5"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_view_role_by_name_tree():
    """ Teste falho
        Busca tipo de usuário por um name com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/roles/true"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"


# Testes para a rota update_role
def test_sucess_update_role():
    """ Teste de sucesso
        Altera tipo de usuário existente
    """
    # Cria um novo tipo de usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/roles/",
            json={
                "name": "test role"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test role"
    }

    # Altera tipo de usuário criado
    with TestClient(app) as c:
        response = c.update(
            f"/api/v1/roles/{response.json()['id']}",
            json={
                "name": "test role updated"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test role updated"
    }

    # Deleta tipo de usuário criado
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/roles/{response.json()['id']}")

def test_failed_update_role_not_found():
    """ Teste de sucesso
        Tenta atualizar tipo de usuário por um id que não existe
    """
    # Entrada com id inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/roles/0",
            json={
                "name": "test role updated"
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_update_role():
    """ Teste de sucesso
        Tenta atualizar tipo de usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/roles/invalid_id",
            json={
                "name": "test role"
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_update_role_two():
    """ Teste de sucesso
        Tenta atualizar tipo de usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/roles/True",
            json={
                "name": "test role"
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_update_role_tree():
    """ Teste de sucesso
        Tenta atualizar tipo de usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/roles/1.5",
            json={
                "name": "test recipe"
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"


# Testes para a rota delete_recipe
def test_sucess_delete_role():
    """ Teste de sucesso
        Altera tipo de usuário existente
    """
    # Cria um novo tipo de usuário
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/role/",
            json={
                "name": "test role"
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test role"
    }

    # Deleta tipo de usuário criada
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/roles/{response.json()['id']}")
    # Verifica se response corresponde
    assert response.status_code == 204

def test_failed_delete_role_not_found():
    """ Teste de sucesso
        Tenta deletar tipo de usuário por um id que não existe
    """
    # Entrada com id inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/roles/0")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_delete_role():
    """ Teste de sucesso
        Tenta deletar tipo de usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update("/api/v1/roles/invalid_id")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_delete_role_two():
    """ Teste de sucesso
        Tenta deletar tipo de usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/roles/True")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"

def test_failed_delete_role_tree():
    """ Teste de sucesso
        Tenta deletar tipo de usuário por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update("/api/v1/roles/1.5")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Tipo de usuário não encontrado"
