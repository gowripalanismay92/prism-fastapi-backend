from fastapi import APIRouter, HTTPException, Request
from app.schemas.bob import BOBResponse

router = APIRouter(prefix="/advisors", tags=["Book of Business"])


def get_service(request: Request):
    return request.app.state.bob_service


@router.get("/{advisor_id}/bob", response_model=BOBResponse)
def get_advisor_bob(advisor_id: str, request: Request):
    # Authentication is enforced by the Databricks Apps OAuth ingress.
    # The frontend must resolve the signed-in employee on its server and call
    # this API with that employee/advisor ID. Never accept an ID from browser JS.
    if not advisor_id.strip():
        raise HTTPException(status_code=400, detail="advisor_id is required.")
    return get_service(request).get_advisor_book(advisor_id)
