from collections import Counter
from fastapi import HTTPException
from app.repositories.bob_csv_repository import BOBCSVRepository


class BOBService:
    def __init__(self, repository: BOBCSVRepository):
        self.repository = repository

    def get_advisor_book(self, advisor_id: str) -> dict:
        records = self.repository.find_by_advisor(advisor_id)
        if not records:
            raise HTTPException(status_code=404, detail="No BOB records found for this advisor.")

        statuses = Counter(r["status"] for r in records)
        products = Counter(r["product_type"] for r in records)
        return {
            "advisor_id": advisor_id,
            "summary": {
                "client_count": len(records),
                "in_force_count": statuses.get("In Force", 0),
                "pending_count": statuses.get("Pending", 0),
                "lapsed_count": statuses.get("Lapsed", 0),
                "total_aum": round(sum(r["account_value"] for r in records), 2),
                "total_annual_premium": round(sum(r["annual_premium"] for r in records), 2),
                "total_face_amount": round(sum(r["face_amount"] for r in records), 2),
            },
            "product_mix": [{"name": k, "count": v} for k, v in sorted(products.items())],
            "status_mix": [{"name": k, "count": v} for k, v in sorted(statuses.items())],
            "records": records,
            "data_notice": "Fictional synthetic sample data for development and testing only.",
        }
