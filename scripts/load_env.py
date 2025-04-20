from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ID = os.getenv('GCP_PROJECT')
DATASET_ID = os.getenv('BQ_DATASET')
TABLE_ID = os.getenv('BQ_TABLE')