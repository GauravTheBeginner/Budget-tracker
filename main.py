from datetime import datetime, timedelta
import logging
from aws.main import AWS
from gcp.main import GCP
from azure.main import Azure
from rn.main import RN
from precomputation.main import PrecomputedTable

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CloudDataProcessor:
    """Handles cost data extraction and processing for multiple cloud providers."""

    def __init__(self, date):
        self.date = date
        self.services = [
            ("AWS", lambda: AWS(self.date)),
            ("Azure", lambda: Azure(self.date)),
            ("GCP", lambda: GCP(self.date)),
            ("RN", lambda: RN(self.date)),
            ("Precomputation", PrecomputedTable)
        ]
        self.errors = []

    def process_data(self):
        """Processes data for all registered cloud services."""
        for service_name, service_class in self.services:
            try:
                logging.info(f"Processing {service_name} data for {self.date}")
                service = service_class()
                service.process_operations()
                logging.info(f"✅ Successfully processed {service_name} data for {self.date}")
            except Exception as e:
                logging.error(f"❌ Failed to process {service_name} data: {e}")
                self.errors.append((service_name, e))

def main(date):
    """Runs data processing for a single date."""
    processor = CloudDataProcessor(date)
    processor.process_data()

def run_for_days(start_day, end_day):
    """Runs processing for multiple past days."""
    for day in range(start_day, end_day + 1):
        date = datetime.now().date() - timedelta(days=day)
        logging.info(f"📅 Processing Date: {date} (Day {day})")
        # main(date)
    logging.info(f"✅ Finished processing for {start_day}-{end_day} days.")

if __name__ == "__main__":
    # run_for_days(7, 23)
    date = datetime.now().date() - timedelta(days=1)
    logging.info(f"🚀 Starting processing for Date: {date}")
    main(date)
    logging.info(f"✅ Finished processing for Date: {date}")
