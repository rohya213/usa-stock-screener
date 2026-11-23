# %%
import os
import logging
import pandas as pd

# Configure logging for preprocessing stage
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/preprocess.log"),
        logging.StreamHandler()
    ]
)

def run_preprocessing():
    logging.info("--- STARTING PREPROCESSING STAGE ---")
    
    # 1. EXTRACT
    try:
        logging.info("Loading raw data from CSVs...")
        awards_raw = pd.read_csv("../data/raw/awards_raw.csv")
        transactions_raw = pd.read_csv("../data/raw/transactions_raw.csv")
    except Exception as e:
        logging.error(f"Failed to load raw data: {e}")
        return

    # 2. TRANSFORM
    logging.info("Transforming datasets...")
    
    # Drop unnecessary columns
    awards_raw = awards_raw.drop(columns=["internal_id", "generated_internal_id"], errors='ignore')
    transactions_raw = transactions_raw.drop(columns=["internal_id", "generated_internal_id"], errors='ignore')

    # Date formatting
    transactions_raw["Action Date"] = pd.to_datetime(transactions_raw["Action Date"], errors="coerce")
    awards_raw["Base Obligation Date"] = pd.to_datetime(awards_raw["Base Obligation Date"], errors="coerce")
    awards_raw["Last Modified Date"] = pd.to_datetime(awards_raw["Last Modified Date"], errors="coerce")

    # Standardize column names (lowercase and snake_case)
    transactions_raw.columns = transactions_raw.columns.str.lower().str.replace(" ", "_")
    awards_raw.columns = awards_raw.columns.str.lower().str.replace(" ", "_")

    # String cleaning and case validation
    transactions_raw['recipient_name'] = transactions_raw['recipient_name'].astype(str).str.strip().str.title()
    awards_raw['recipient_name'] = awards_raw['recipient_name'].astype(str).str.strip().str.title()
    transactions_raw['award_type'] = transactions_raw['award_type'].str.upper()

    # 3. SAVE PROCESSED DATA
    try:
        os.makedirs("../data/processed", exist_ok=True)
        logging.info("Saving preprocessed data to '../data/processed/'...")
        
        awards_raw.to_csv("../data/processed/awards_processed.csv", index=False)
        transactions_raw.to_csv("../data/processed/transactions_processed.csv", index=False)
        
        logging.info("Preprocessing completed successfully!")
    except Exception as e:
        logging.error(f"Failed to save processed data: {e}")

if __name__ == "__main__":
    run_preprocessing()
# %%
