from pydantic import BaseModel


class FraudInput(BaseModel):
    features: list