# nutritional_value_recipes
A partir de um banco de dados contendo receitas culinárias, captura ingredientes e retorna o valor nutricional de cada ingrediente da receita e o valor nutricional da receita completa.

## Acessar os docs

Dps de iniciar o servidor visite o endereço:

```
http://127.0.0.1:8000/docs#/
```
---
## Rodar os testes

```
poetry run pytest tests -v -x
```
---
# Informações e documentação
## Passo a passo para primeira utilização de desenvolvimento
------

1. instalar dependências com o poetry
~~~
poetry install
~~~
2. estando no diretório do projeto, subir o container com banco de dados
~~~
docker-compose up -d
~~~
extra: caso queira acompanhar os logs do banco de dados
~~~
docker ps
docker logs -f recipes-postgres
~~~

3. rodar codigo pelo terminal utilizando o poetry e o uvicorn da API
~~~
poetry run uvicorn app.main:app --reload
~~~
4. Abrir navegador em: http://127.0.0.1:8000/docs#/
---

## Mais informações em https://fastapi.tiangolo.com/