#pylint: disable=E0213

import re
from pydantic import BaseModel, constr, Field, validator
from unidecode import unidecode


class User(BaseModel):
    username: constr(
        max_length=16,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        ) = Field(..., example="zecolmeia")
    hashed_password: constr(
        max_length=14,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        ) = Field(..., example="amigocatatau")
    full_name: constr(
        max_length=30,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        ) = Field(..., example="ze colmeia da silva")
    email: constr(
        max_length=20,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        ) = Field(..., example="zecolmeia@abc.com")
    desable: bool
    role: int

    @validator("username")
    def apply_unidecode(cls, v):
        """ Aplica unidecode no nome de úsuario """
        return re.sub(r'[^\w\s]', '', unidecode(v))


class UserResponse(User):
    """ Modelo de resposta de usuario """
    id: int
