import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

# API ENDPOINTS
BASE_URL = "https://api.usaspending.gov/api/v2"
AWARD_ENDPOINT = f"{BASE_URL}/search/spending_by_award/"
TRANSACTION_ENDPOINT = f"{BASE_URL}/search/spending_by_transaction/"

# 30 day date range for recently recorded new awards
today = date.today()
start_date = today - timedelta(days=30)

# shared filters
filters = {
    "award_type_codes": ["A", "B", "C", "D"],
    "time_period": [
        {
            "start_date": start_date.isoformat(),
            "end_date": today.isoformat(),
            # filter by "base transaction date/base action date" not PoP
            "date_type": "new_awards_only"
        }
    ]
}
    
# --------------------------------------------------
# 2. Retrieve award-level data
# --------------------------------------------------

award_payload = {
    "filters": filters,
    "fields": [
        "Award ID", # unique identifier for the award
        "Recipient Name", # company name
        "Description", # award description (to understand the contracts purpose)
        "Base Obligation Date", # the date of the first funding is being commited to the award
        "Award Amount", # money awarded so far - money the gov has officially locked in and signed away to be spent on this contract so far. (Can incr over time via contract modifications)
        "Last Modified Date" # monitor the latest date of the details of a reported award/transaction record were last updated, processed etc.
    ],
    "limit": 100,
    "page": 1,
    "sort": "Base Obligation Date",
    "order": "desc"
}

award_response = requests.post(
    AWARD_ENDPOINT,
    json=award_payload,
    timeout=60
)
award_response.raise_for_status()

awards = award_response.json().get("results", [])

print(f"Award records retrieved: {len(awards)}")

# --------------------------------------------------
# 2. Retrieve transaction-level data
# --------------------------------------------------

transaction_payload = {
    "filters": filters,
    "fields": [
        "Award ID", # same as the award-level data
        "Recipient Name",
        "Action Date", # date of admin modification 
        "Transaction Amount", # value of each transaction (federal action obligation)
        "Mod", # modification number of the transaction
        "Transaction Description", # understand the nature of the trans
        "Award Type", # type of award (contract, grant, loan, etc.)
    ],
    "limit": 100,
    "page": 1,
    "sort": "Action Date",
    "order": "desc"
}

transaction_response = requests.post(
    TRANSACTION_ENDPOINT,
    json=transaction_payload,
    timeout=60
)
transaction_response.raise_for_status()

transactions = transaction_response.json().get("results", [])

print(f"Transaction records retrieved: {len(transactions)}")


# make steps 1 and 2 cleaner

# --------------------------------------------------
# 3. Save raw API results
# --------------------------------------------------

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

with open(
    output_dir / "awards_raw.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(awards, file, indent=2, ensure_ascii=False)

with open(
    output_dir / "transactions_raw.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(transactions, file, indent=2, ensure_ascii=False)

# --------------------------------------------------
# 4. Convert results to DataFrames
# --------------------------------------------------

awards_df = pd.DataFrame(awards)
transactions_df = pd.DataFrame(transactions)

# Convert transaction amount to numeric
if "Transaction Amount" in transactions_df.columns:
    transactions_df["Transaction Amount"] = pd.to_numeric(
        transactions_df["Transaction Amount"],
        errors="coerce"
    )

# Save CSV files
awards_df.to_csv(
    output_dir / "awards_raw.csv",
    index=False
)

transactions_df.to_csv(
    output_dir / "transactions_raw.csv",
    index=False
)
