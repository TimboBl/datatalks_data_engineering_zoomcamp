import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Create the SQLAlchemy engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Time the CSV reading
    t_start = time()
    print(f'Reading data from {url}...')
    
    # Check if file is gzipped based on extension
    if url.endswith('.gz'):
        df = pd.read_csv(url, compression='gzip')
    else:
        df = pd.read_csv(url)
        
    t_end = time()
    print(f'Finished reading data. Took {t_end - t_start:.3f} seconds')
    print(f'Read {len(df)} rows')

    # Time the Postgres upload
    t_start = time()
    print(f'Uploading data to Postgres table {table_name}...')
    df.to_sql(name=table_name, con=engine, if_exists='replace')
    t_end = time()
    print(f'Finished uploading data. Took {t_end - t_start:.3f} seconds')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # Add the arguments
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file (can be .csv or .csv.gz)')

    args = parser.parse_args()
    main(args)