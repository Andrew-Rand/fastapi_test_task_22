from pydantic import BaseModel


class BaseErrorResponse(BaseModel):
    detail: str