from pydantic import BaseModel


class CrProduct(BaseModel):
    seller: str
    price: float
