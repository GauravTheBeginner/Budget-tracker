import pandas as pd
from lib.database import DatabaseHelper

class SummaryTableExtractor:
    def __init__(self):
        pass

    def extract_data(self):
        gcp_query = "SELECT * FROM gcp;"
        aws_query = "SELECT * FROM historical_aws;"
        azure_query = "SELECT * FROM historical_azure;"

        with DatabaseHelper() as db:
            # Fetch data from GCP table
            gcp_df = pd.read_sql(gcp_query, db.engine)

            # Fetch data from historical AWS table
            aws_df = pd.read_sql(aws_query, db.engine)

            # Fetch data from historical Azure table
            azure_df = pd.read_sql(azure_query, db.engine)

            gcp_df = gcp_df.rename(
                columns={
                    "project.number": "Account Number",
                    "project.name": "Account Name",
                    "usage_end_time": "Invoice Date",
                    "sku.description": "Service Name",
                    "service.description": "Usage Family",
                    "cost_at_list": "Cost",
                    "usage.amount": "Usage Quantity",
                }
            )

            # Select only the necessary columns from GCP DataFrame
            gcp_df["Vendor"] = "GCP"
            gcp_df = gcp_df[
                [
                    "Account Number",
                    "Account Name",
                    "Vendor",
                    "Invoice Date",
                    "Service Name",
                    "Usage Family",
                    "Cost",
                    "Usage Quantity",
                ]
            ]
            gcp_df["Invoice Date"] = pd.to_datetime(gcp_df["Invoice Date"])
            aws_df["Invoice Date"] = pd.to_datetime(aws_df["Invoice Date"])

            # Return Merged GCP and AWS DataFrames
            return pd.concat([aws_df, gcp_df])