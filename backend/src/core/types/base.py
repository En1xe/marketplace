from typing import TypedDict, Type

from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import orm


SqlAlchemyModel = DeclarativeMeta | orm.DeclarativeMeta

class SchemaDict(TypedDict):
    admin: Type[BaseModel]
    public: Type[BaseModel]
    owner: Type[BaseModel]
