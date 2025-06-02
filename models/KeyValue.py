from pydantic import BaseModel


class KeyValueModel(BaseModel):
    key: str
    value: int
