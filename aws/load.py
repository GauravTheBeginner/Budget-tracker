import pandas as pd
from lib.db_helper import load_df_to_table
from summary.load import SummaryTableLoader
import logging

class AWSLoader:
    def __init__(self, data):
        self.data = data

    def convert_to_data_frame(self, data):
        """Convert list of dictionaries to a pandas DataFrame with proper data types."""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        
        # Rename columns for consistency
        df.rename(columns={
            "invoice_date": "Invoice Date",
            "cost": "Cost",
            "usage_quantity": "Usage Quantity",
            "account_number": "Account Number",
            "usage_family": "Usage Family",
            "service_name": "Service Name",
            "account_name": "Account Name",
        }, inplace=True)

        # Convert date columns
        if "Invoice Date" in df.columns:
            df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])

        # Convert numeric columns to float
        for col in ["Cost", "Usage Quantity"]:
            if col in df.columns:
                df[col] = df[col].astype(float)

        return df

    def load_data(self):
        """Load generated data into respective database tables."""
        data_mappings = {
            "results": {
                "table": "historical_aws",
                "warning": "AWS doesn't have any data.",
                "extra_processing": lambda df: self._load_summary_table(df)
            },
            "region_legal_entity_results": {
                "table": "aws_billing_grouped_by_region_entity",
                "warning": "AWS billing group by region and legal entity doesn't have any data.",
                "extra_processing": None
            },
            "usage_type_group_results": {
                "table": "aws_billing_grouped_by_usage_type",
                "warning": "AWS billing group by usage type doesn't have any data.",
                "extra_processing": None
            }
        }

        for key, config in data_mappings.items():
            data_list = self.data.get(key, [])

            if data_list:
                df = self.convert_to_data_frame(data_list)

                if not df.empty:
                    load_df_to_table(config["table"], df)
                    
                    # Call extra processing for summary table if applicable
                    if config["extra_processing"]:
                        config["extra_processing"](df)
                else:
                    logging.warning(f"{config['table']} has no data to load.")
            else:
                logging.warning(config["warning"])

    def _load_summary_table(self, df):
        """Load data into the summary table."""
        if not df.empty:
            # Ensure date conversion
            aws_df = df.copy()
            aws_df["Invoice Date"] = pd.to_datetime(aws_df["Invoice Date"])
            aws_df["Vendor"] = "AWS"
            aws_df = aws_df[
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

            aws_df["Service Name"] = aws_df["Usage Family"]

            # Load the data to the Summary Table
            summary_loader = SummaryTableLoader(aws_df)
            summary_loader.load_data()
            logging.info("✅ Summary table loaded successfully.")
