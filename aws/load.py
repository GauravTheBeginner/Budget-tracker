import pandas as pd
from lib.db_helper import load_df_to_table

class AWSLoader:
    def __init__(self, data):
        self.data = data

    def convert_to_data_frame(self, data):
        """Convert list of dictionaries to a pandas DataFrame with proper data types."""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df.rename(columns={
            "invoice_date": "Invoice Date",
            "cost": "Cost",
            "usage_quantity": "Usage Quantity",
        }, inplace=True)

        if "Invoice Date" in df.columns:
            df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])

        for col in ["Cost", "Usage Quantity"]:
            if col in df.columns:
                df[col] = df[col].astype(float)

        return df

    def load_data(self):
        """Load generated data into respective database tables."""
        results = self.data.get("results", [])
        region_legal_results = self.data.get("region_legal_entity_results", [])
        usage_type_results = self.data.get("usage_type_group_results", [])

        df = self.convert_to_data_frame(results)
        region_legal_df = self.convert_to_data_frame(region_legal_results)
        usage_type_df = self.convert_to_data_frame(usage_type_results)

        if not df.empty:
            load_df_to_table("historical_aws", df)
        if not region_legal_df.empty:
            load_df_to_table("aws_billing_grouped_by_region_entity", region_legal_df)
        if not usage_type_df.empty:
            load_df_to_table("aws_billing_grouped_by_usage_type", usage_type_df)
