from pydantic import BaseModel, ConfigDict


class BOBRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    advisor_id: str
    client_id: str
    client_name: str
    product_type: str
    status: str
    annual_premium: float
    face_amount: float
    account_value: float
    next_review_date: str | None = None


class MetricSummary(BaseModel):
    client_count: int
    in_force_count: int
    pending_count: int
    lapsed_count: int
    total_aum: float
    total_annual_premium: float
    total_face_amount: float


class MixItem(BaseModel):
    name: str
    count: int


class BOBResponse(BaseModel):
    advisor_id: str
    summary: MetricSummary
    product_mix: list[MixItem]
    status_mix: list[MixItem]
    records: list[BOBRecord]
    data_notice: str
