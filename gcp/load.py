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

        if "Invoice Date" in df.columns:
            df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])
        
        for col in ["Cost", "Usage Amount"]:
            if col in df.columns:
                df[col] = df[col].astype(float)

        return df

    def load_data(self):
        """Load generated GCP data into the database."""
        results = self.data.get("results", [])

        df = self.convert_to_data_frame(results)

        if not df.empty:
            load_df_to_table("gcp", df)
            print(f"✅ Loaded {len(df)} records into 'gcp' table.")
        else:
            print("⚠ No data to load for GCP.")
