import csv
from pathlib import Path
from fastapi import HTTPException


# CSV header -> stable API field mapping.
FIELD_MAP = {
    "Advisor ID": "advisor_id",
    "Client ID (Sample)": "client_id",
    "Client Name (Fictional)": "client_name",
    "Product Type": "product_type",
    "Status": "status",
    "Annual Premium (USD)": "annual_premium",
    "Face Amount (USD)": "face_amount",
    "AUM / Account Value (USD)": "account_value",
    "Next Review Date": "next_review_date",
}


class BOBCSVRepository:
    """Loads the mock file once at startup; filters in memory for demo scale."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._rows: list[dict] = []

    def load(self) -> None:
        if not self.file_path.is_file():
            raise RuntimeError(f"BOB data file not found: {self.file_path}")
        with self.file_path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            required = set(FIELD_MAP)
            actual = set(reader.fieldnames or [])
            missing = required - actual
            if missing:
                raise RuntimeError(f"BOB CSV missing required columns: {sorted(missing)}")

            rows = []
            for raw in reader:
                item = {api_key: raw.get(csv_key, "") for csv_key, api_key in FIELD_MAP.items()}
                try:
                    item["annual_premium"] = float(item["annual_premium"] or 0)
                    item["face_amount"] = float(item["face_amount"] or 0)
                    item["account_value"] = float(item["account_value"] or 0)
                except (TypeError, ValueError) as exc:
                    raise RuntimeError("BOB CSV contains a non-numeric financial value") from exc
                item["advisor_id"] = str(item["advisor_id"]).strip()
                item["status"] = str(item["status"]).strip()
                rows.append(item)
        self._rows = rows

    def find_by_advisor(self, advisor_id: str) -> list[dict]:
        normalized = advisor_id.strip().casefold()
        return [row.copy() for row in self._rows if row["advisor_id"].casefold() == normalized]

    @property
    def record_count(self) -> int:
        return len(self._rows)
