from google.cloud import bigquery
from load_env import DATASET_ID, TABLE_ID

def delete_table(dataset_id, table_id):
    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)
    client.delete_table(table_ref, not_found_ok=True)
    print(f'Table {table_id} deleted from dataset {dataset_id}.')

delete_table(DATASET_ID, TABLE_ID)
