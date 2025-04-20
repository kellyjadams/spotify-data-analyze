from google.cloud import bigquery
from load_env import DATASET_ID, TABLE_ID

def create_table(dataset_id, table_id):
    client = bigquery.Client()

    schema = [
        bigquery.SchemaField('timestamp', 'TIMESTAMP'),
        bigquery.SchemaField('track', 'STRING'),
        bigquery.SchemaField('artists', 'STRING'),
        bigquery.SchemaField('album', 'STRING'),
        bigquery.SchemaField('duration_ms', 'INTEGER'),
        bigquery.SchemaField('genre', 'STRING'),
        bigquery.SchemaField('popularity', 'INTEGER'),
        bigquery.SchemaField('explicit', 'BOOLEAN'),
    ]

    table_ref = client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref, schema=schema)

    try:
        client.create_table(table)
        print(f'Table {table_id} created in dataset {dataset_id}.')
    except Exception as e:
        print(f'Error creating table: {e}')

create_table(DATASET_ID, TABLE_ID)
