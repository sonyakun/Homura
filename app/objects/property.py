import base64
from typing import Union

import orjson
from pydantic import BaseModel
from pydantic_core import PydanticCustomError


class Property(BaseModel):
    name: str
    value: Union[str, dict]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = orjson.loads(base64.decodebytes(self.value.encode()))
