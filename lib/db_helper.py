import logging
import csv
from io import StringIO
from lib.database import DatabaseHelper

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Old Way of Insertion data into table

# def load_df_to_table(table_name, df, overwrite=False):
#     """
#     Todo: adjust this function to validate before appending
#     if the has been loaded for the same day then we have to delete all the old items of that day
#     and load the new data. otherwise there will be inconsistent data
#     """

#     with DatabaseHelper() as dbHelper:
#         if not dbHelper.engine:
#             logging.error("Engine creation failed.")
#             return
    
#         df.to_sql(table_name, con=dbHelper.engine, if_exists="append" if not overwrite else "replace", index=False)
#         logging.info(f"Data from {table_name} loaded into table {table_name}..!")


def psql_insert_copy(table, conn, keys, data_iter):
    """
    Execute bulk insert using PostgreSQL's COPY method.
    """
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        table_name = table.name if not table.schema else f'{table.schema}.{table.name}'

        sql = f'COPY {table_name} ({columns}) FROM STDIN WITH CSV'
        cur.copy_expert(sql=sql, file=s_buf)

def load_df_to_table(table_name, df, overwrite=False):
    """
    Load DataFrame into a PostgreSQL table using the COPY method for efficient bulk insert.
    """
    logging.info(f"Data from DataFrame loading into table {table_name} started!")
    with DatabaseHelper() as dbHelper:
        if not dbHelper.engine:
            logging.error("Engine creation failed.")
            return

        con = dbHelper.engine.connect()

        # Use COPY method for bulk insert
        df.to_sql(
            name=table_name,
            con=con,
            if_exists="replace" if overwrite else "append",
            index=False,
            # method=psql_insert_copy
        )

        logging.info(f"Data from DataFrame loaded into table {table_name} successfully!")
