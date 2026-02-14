from pydantic import BaseModel


class RedirectTokenSchema(BaseModel):
    token: str
    