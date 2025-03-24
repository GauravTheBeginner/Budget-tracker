import pandas as pd
from lib.db_helper import load_df_to_table
from summary.load import SummaryTableLoader  

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
        """Load generated GCP data into the database and summary table."""
        results = self.data.get("results", [])

        df = self.convert_to_data_frame(results)

        if not df.empty:
            # ✅ Load to main GCP table
            load_df_to_table("gcp", df)
            print(f"✅ Loaded {len(df)} records into 'gcp' table.")

            # ✅ Prepare summary DataFrame
            gcp_df = df.copy()
            gcp_df["Vendor"] = "GCP"
            gcp_df["Usage Quantity"] = gcp_df["Usage Amount"]
            gcp_df["Account Name"] = gcp_df["Project Name"]
            gcp_df = gcp_df[
                [
                    "Account Number",
                    "Account Name",
                    "Vendor",
                    "Usage Family",
                    "Usage Quantity",
                    "Cost",
                    "Invoice Date"
                ]
            ]

            gcp_df["Service Name"] = gcp_df["Usage Family"]

            # Load the data to the Summary Table
            summary_loader = SummaryTableLoader(gcp_df)
            summary_loader.load_data()
            print(f"✅ Loaded {len(gcp_df)} records into summary table.")
        else:
            print("⚠ No data to load for GCP.")
