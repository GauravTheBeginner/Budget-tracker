import pandas as pd
from lib.db_helper import load_df_to_table

class GCPLoader:
    def __init__(self, data):
        self.data = data

    def convert_to_data_frame(self, data):
        """Convert list of dictionaries to a pandas DataFrame with proper data types."""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        df.rename(columns={
            "Invoice Date": "invoice_date",
            "Usage Unit": "usage_unit",
            "Usage Amount": "usage_amount",
            "Cost": "cost",
            "Project Number": "project_number",
            "Country": "country",
            "Region": "region",
            "Account Number": "account_number",
            "SKU Description": "sku_description",
            "Seller Name": "seller_name",
            "SKU Id": "sku_id",
            "Usage Family": "usage_family",
            "Project ID": "project_id",
            "Project Name": "project_name",
        }, inplace=True)

        if "invoice_date" in df.columns:
            df["invoice_date"] = pd.to_datetime(df["invoice_date"])
        
        for col in ["cost", "usage_amount"]:
            if col in df.columns:
                df[col] = df[col].astype(float)

        return df

    def load_data(self):
        """Load generated GCP data into the database."""
        results = self.data.get("results", [])

        df = self.convert_to_data_frame(results)

        if not df.empty:
            load_df_to_table("historical_gcp", df)
            print(f"✅ Loaded {len(df)} records into 'historical_gcp' table.")
        else:
            print("⚠ No data to load for GCP.")
