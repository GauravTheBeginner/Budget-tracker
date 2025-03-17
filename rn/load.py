import pandas as pd
from lib.db_helper import load_df_to_table

class RNLoader:
    def __init__(self, data):
        self.data = data

    def convert_to_data_frame(self, data):
        """Convert list of dictionaries to a pandas DataFrame with proper data types."""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        if "UsageEndDate" in df.columns:
            df["UsageEndDate"] = pd.to_datetime(df["UsageEndDate"])

        if "MonthYear" in df.columns:
            df["MonthYear"] = pd.to_datetime(df["MonthYear"])  

        for col in ["Cost", "Usage Amount", "BlendedRate"]:
            if col in df.columns:
                df[col] = df[col].astype(float)

        return df

    def load_data(self):
        """Load generated RN data into the database."""
        results = self.data.get("results", [])

        df = self.convert_to_data_frame(results)

        if not df.empty:
            load_df_to_table("historical_rn", df)
            print(f"✅ Loaded {len(df)} records into 'historical_rn' table.")
        else:
            print("⚠ No data to load for RN.")
