import re
from pydantic import BaseModel, constr, Field, HttpUrl, validator
from unidecode import unidecode

class Role(BaseModel):
    """ Modelo de tipo de usuario """
    name: constr(
        max_length=50,
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        ) = Field(..., example="cliente")

    @validator("name")
    def apply_unidecode(cls, v):
        """ Aplica unidecode no nome """
        return re.sub(r'[^\w\s]', '', unidecode(v))


class RoleResponse(Role):
    """ Modelo de resposta de tipo de usuario """
    id: int