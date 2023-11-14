from pydantic import BaseModel


class NoCashValuteModel(BaseModel):
    name: str
    code_name: str
    type_valute: str


class CurrentDirection(BaseModel):
    name: str
    partner_link: str | None
    valute_from: str
    valute_to: str
    in_count: float
    out_count: float
    min_amount: str
    max_amount: str
    # rating: str