# automate the entire pipeline
import logging
from pathlib import Path
# Import the functions from your src package
from src.preprocess import run_preprocessing  
from src.load_to_ssms import run_load           

# Set up global pipeline logging
PROJECT_ROOT = Path(__file__).resolve().parent
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=PROJECT_ROOT / "logs" / "pipeline.log",
    filemode="a"
)

def main():
    logging.info("================ STARTING ETL PIPELINE ================")
    
    # Step 1: Extract & Transform
    logging.info("Step 1: Commencing Preprocessing...")
    run_preprocessing()
    
    # Step 2: Load into SSMS (award_info database)
    logging.info("Step 2: Commencing Database Load...")
    run_load()
    
    logging.info("================ ETL PIPELINE COMPLETED ================")

if __name__ == "__main__":
    main()