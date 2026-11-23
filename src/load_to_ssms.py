# %%
import logging
import urllib
import pandas as pd
import sqlalchemy as sa

# --- CONFIGURATION ---
SERVER_NAME = r"RUSSEL\SQLEXPRESS08"  
DB_NAME = "award_info"               

# Configure logging for load stage
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/load_to_ssms.log"),
        logging.StreamHandler()
    ]
)

def run_load():
    logging.info("--- STARTING DB LOAD STAGE ---")
    
    # 1. READ PROCESSED DATA
    try:
        logging.info("Reading preprocessed data...")
        awards_df = pd.read_csv("../data/processed/awards_processed.csv")
        transactions_df = pd.read_csv("../data/processed/transactions_processed.csv")
    except FileNotFoundError:
        logging.error("Processed files not found. Please run 'preprocess.py' first.")
        return
    except Exception as e:
        logging.error(f"Error reading processed data: {e}")
        return

    # 2. CONNECT TO SSMS
    logging.info(f"Connecting to SSMS Instance: {SERVER_NAME}...")
    connection_string = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={SERVER_NAME};"
        f"Database={DB_NAME};"
        f"Trusted_Connection=yes;"
    )
    params = urllib.parse.quote_plus(connection_string)
    engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    # 3. DUMP DATA TO TABLES
    try:
        # Dump Awards
        logging.info("Dumping awards to table 'dim_awards'...")
        awards_df.to_sql(
            name="dim_awards", 
            con=engine, 
            if_exists="append", 
            index=False, 
            chunksize=1000
        )
        
        # Dump Transactions
        logging.info("Dumping transactions to table 'fact_transactions'...")
        transactions_df.to_sql(
            name="fact_transactions", 
            con=engine, 
            if_exists="append", 
            index=False, 
            chunksize=1000
        )
        
        logging.info("Database load completed successfully! All data sent to SSMS.")

    except Exception as e:
            logging.error(f"Critical database load error: {e}")

if __name__ == "__main__":
    run_load()
# %%