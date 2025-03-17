import pandas as pd
from lib.db_helper import load_df_to_table

class AzureLoader:
    def __init__(self, data):
        self.data = data

    def convert_to_data_frame(self, data):
        """Convert list of dictionaries to a pandas DataFrame with proper data types."""
        if data is None or len(data) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df.rename(columns={
            "Invoice Date": "Invoice Date",
            "Cost": "Cost",
            "Usage Quantity": "Usage Quantity",
            "Account Number": "Account Number",
            "Account Name": "Account Name",
            "Service Name": "Service Name",
            "Resource Location": "Resource Location",
            "Meter": "Meter",
            "Meter Category": "Meter Category",
            "Meter Sub Category": "Meter Sub Category",
            "Resource Type": "Resource Type",
            "Resource Group": "Resource Group",
        }, inplace=True)

        if "Invoice Date" in df.columns:
            df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])

        for col in ["Cost", "Usage Quantity"]:
            if col in df.columns:
                df[col] = df[col].astype(float)

        return df

    def load_data(self):
        """Load generated Azure billing data into respective database tables."""
        if self.data is None or isinstance(self.data, pd.DataFrame) and self.data.empty:
            print("No Azure data to load.")
            return

        df = self.convert_to_data_frame(self.data)

        if df.empty:
            print("Converted DataFrame is empty. Skipping database load.")
            return

        load_df_to_table("historical_azure", df)
        print("✅ Azure data loaded successfully!")
