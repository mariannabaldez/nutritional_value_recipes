from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


#Testes para a rota create_recipes
def test_sucess_create_new_recipe():
    """ Teste de sucesso
        Cria receita com ingredients
    """
    # Cria uma nova receita
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/recipes/",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test recipe",
        "descript": "test preparation",
        "ingredients": {
            "test_name_ingredient":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            },
            "test_name_ingredient_2":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            },
            "test_name_ingredient_3":{
                "test_unit_measure": "gramas",
                "test_quantity": 5
            }
        },
        "id": response.json()["id"]
    }

    # Deleta receita criada
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/recipes/{response.json()['id']}")

def test_failed_already_exists_create_recipe():
    """ Teste falho
        Cria uma nova receita que já existe
        obs: A verificação é feita quando os ingredientes,
        unidades de medidas e quantidades da entrada,
        já existem no banco de dados.
    """
    # Cria uma nova receita
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/recipes/",
            json={
                "name": "test recipe already exists",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test recipe already exists",
        "descript": "test preparation",
        "ingredients": {
            "test_name_ingredient":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            },
            "test_name_ingredient_2":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            },
            "test_name_ingredient_3":{
                "test_unit_measure": "gramas",
                "test_quantity": 5
            }
        },
        "id": response.json()["id"]
    }

    # Cria a receita novamente garantindo que ela já existe
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/recipes/",
            json={
                "name": "test recipe already exists",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 401
    assert invalid_response.detail == "Receita já existe"

    # Deleta receita criada
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/recipes/{response.json()['id']}")

def test_failed_create_recipe():
    """ Teste falho
        Cria uma nova receita sem ingredientes listados
    """
    # Cria receita uma nova sem ingredientes
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/recipes/",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {}
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"

def test_failed_create_recipe_two():
    """ Teste falho
        Cria uma nova receita sem nome definido
    """
    # Cria receita uma nova sem ingredientes
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/recipes/",
            json={
                "name": "",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"

def test_failed_create_recipe_tree():
    """ Teste falho
        Cria uma nova receita sem modo de preparo definido
    """
    # Cria receita uma nova sem ingredientes
    with TestClient(app) as c:
        invalid_response = c.post(
            "/api/v1/recipes/",
            json={
                "name": "test recipe",
                "descript": "",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )
    # Verifica se response corresponde
    assert invalid_response.status_code == 400
    assert invalid_response.detail == "Bad Request"


#Testes para a rota view_recipe_by_id
def test_sucess_view_recipe_by_id():
    """ Teste de sucesso
        Busca receita pelo id
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/1"
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "empadao de frango",
        "descript": \
            "Em uma panela, aqueça o azeite e " + \
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
        },
        "id": 1
    }

def test_failed_view_recipe_by_id_not_found():
    """ Teste falho
        Busca receita por um id que não existe
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/99999999999999"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_view_recipe_by_id():
    """ Teste falho
        Busca receita por um id inexistente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/0"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_view_recipe_by_id_two():
    """ Teste falho
        Busca receita por um id com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/abc"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_view_recipe_by_id_tree():
    """ Teste falho
        Busca receita por um id com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/1.5"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_view_recipe_by_name_four():
    """ Teste falho
        Busca receita por um id com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/true"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"


#Testes para a rota view_recipe_by_name
def test_sucess_view_recipe_by_name():
    """ Teste de sucesso
        Busca receita pelo nome
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/arroz"
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "arroz",
        "descript": \
            "Em uma panela, aqueça o azeite e " + \
            "refogue o arroz até que os grãos  " + \
            "estejam esbranquiçados, após " + \
            "acrescente a cebola, o alho e " + \
            "refogue. Adicione a água, " + \
            "acrescente o sal e espere " + \
            "pela fervura para abaixar o fogo " + \
            "para médio. Após a água reduzir e o " + \
            "arroz estiver quase seco, tampe a " + \
            "panela e deixe o fogo no minimo por " + \
            "5 minutos e em segunamea desligue o fogo.",
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
                "measure": "unnameade",
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
        },
        "id": 1
    }

def test_failed_not_found_view_recipe_by_name():
    """ Teste falho
        Busca receita por um name que não existe
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/invalida"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_view_recipe_by_name():
    """ Teste falho
        Busca receita por um name com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/0"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_view_recipe_by_name_two():
    """ Teste falho
        Busca receita por um name com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/1.5"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_view_recipe_by_name_tree():
    """ Teste falho
        Busca receita por um name com tipo diferente
    """
    # Busca receita
    with TestClient(app) as c:
        response = c.get(
            "/api/v1/recipes/true"
        )
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"


# Testes para a rota update_recipe
def test_sucess_update_recipe():
    """ Teste de sucesso
        Altera receita existente
    """
    # Cria uma nova receita
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/recipes/",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test recipe",
        "descript": "test preparation",
        "ingredients": {
            "test_name_ingredient":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            },
            "test_name_ingredient_2":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            },
            "test_name_ingredient_3":{
                "test_unit_measure": "gramas",
                "test_quantity": 5
            }
        },
        "id": response.json()["id"]
    }

    # Altera receita criada
    with TestClient(app) as c:
        response = c.update(
            f"/api/v1/recipes/{response.json()['id']}",
            json={
                "name": "test recipe updated",
                "descript": "test preparation updated",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    }
                }
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test recipe updated",
        "descript": "test preparation updated",
        "ingredients": {
            "test_name_ingredient":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            }
        }
    }

    # Deleta receita criada
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/recipes/{response.json()['id']}")

def test_failed_update_recipe_not_found():
    """ Teste de sucesso
        Tenta atualizar receita por um id que não existe
    """
    # Entrada com id inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/recipes/0",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_update_recipe_not_found_two():
    """ Teste de sucesso
        Tenta atualizar receita por um id que não existe
    """
    # Entrada com id inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/recipes/99999999999999",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_update_recipe():
    """ Teste de sucesso
        Tenta atualizar receita por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/recipes/invalid_id",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_update_recipe_two():
    """ Teste de sucesso
        Tenta atualizar receita por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/recipes/True",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_update_recipe_tree():
    """ Teste de sucesso
        Tenta atualizar receita por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.update(
            "/api/v1/recipes/1.5",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )

    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"


# Testes para a rota delete_recipe
def test_sucess_delete_recipe():
    """ Teste de sucesso
        Altera receita existente
    """
    # Cria uma nova receita
    with TestClient(app) as c:
        response = c.post(
            "/api/v1/recipes/",
            json={
                "name": "test recipe",
                "descript": "test preparation",
                "ingredients": {
                    "test_name_ingredient":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_2":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 1
                    },
                    "test_name_ingredient_3":{
                        "test_unit_measure": "gramas",
                        "test_quantity": 5
                    }
                }
            }
        )
    # Verifica se response corresponde
    assert response.status_code == 200
    assert response.json() == {
        "name": "test recipe",
        "descript": "test preparation",
        "ingredients": {
            "test_name_ingredient":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            },
            "test_name_ingredient_2":{
                "test_unit_measure": "gramas",
                "test_quantity": 1
            },
            "test_name_ingredient_3":{
                "test_unit_measure": "gramas",
                "test_quantity": 5
            }
        },
        "id": response.json()["id"]
    }

    # Deleta receita criada
    with TestClient(app) as c:
        response = c.delete(f"/api/v1/recipes/{response.json()['id']}")
    # Verifica se response corresponde
    assert response.status_code == 204

def test_failed_delete_recipe_not_found():
    """ Teste de sucesso
        Tenta deletar receita por um id que não existe
    """
    # Entrada com id inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/recipes/0")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_delete_recipe_not_found_two():
    """ Teste de sucesso
        Tenta deletar receita por um id que não existe
    """
    # Entrada com id inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/recipes/99999999999999")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_delete_recipe():
    """ Teste de sucesso
        Tenta deletar receita por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/recipes/invalid_id")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_delete_recipe_two():
    """ Teste de sucesso
        Tenta deletar receita por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/recipes/True")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"

def test_failed_delete_recipe_tree():
    """ Teste de sucesso
        Tenta deletar receita por um id com
        tipo invalido que não existe
    """
    # Entrada com id inválido e inexistente
    with TestClient(app) as c:
        response = c.delete("/api/v1/recipes/1.5")
    # Verifica se response corresponde
    assert response.status_code == 404
    assert response.detail == "Receita não encontrada"
