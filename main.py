import argparse
import logging
from datetime import datetime, timedelta

from aws.main import AWS
from azure.main import Azure
from gcp.main import GCP
from precomputation.main import PrecomputedTable
from rn.main import RN

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CloudDataProcessor:
    """Handles cost data extraction and processing for multiple cloud providers."""

    def __init__(self, date, include_precomputation=True):
        self.date = date
        self.services = [
            ("AWS", lambda: AWS(self.date)),
            ("Azure", lambda: Azure(self.date)),
            ("GCP", lambda: GCP(self.date)),
            ("RN", lambda: RN(self.date)),
        ]
        if include_precomputation:
            self.services.append(("Precomputation", PrecomputedTable))
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

def main(date, include_precomputation=True):
    """Runs data processing for a single date."""
    processor = CloudDataProcessor(date, include_precomputation)
    processor.process_data()

def run_for_days(start_day, end_day):
    """Backfills data for each day from `end_day` days ago up to `start_day` days ago (oldest first).

    Precomputed tables are rebuilt from the full summary table, so they are refreshed once at the end
    instead of after every day.
    """
    for day in range(end_day, start_day - 1, -1):
        date = datetime.now().date() - timedelta(days=day)
        logging.info(f"📅 Processing Date: {date} (Day {day})")
        main(date, include_precomputation=False)

    logging.info("Rebuilding precomputed tables")
    PrecomputedTable().process_operations()
    logging.info(f"✅ Finished processing for {start_day}-{end_day} days.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and load cloud cost data.")
    parser.add_argument(
        "--days",
        type=int,
        default=None,
        help="Backfill the last N days (e.g. 180 for ~6 months). Omit to process only yesterday.",
    )
    args = parser.parse_args()

    if args.days:
        logging.info(f"🚀 Backfilling the last {args.days} days")
        run_for_days(1, args.days)
    else:
        date = datetime.now().date() - timedelta(days=1)
        logging.info(f"🚀 Starting processing for Date: {date}")
        main(date)
        logging.info(f"✅ Finished processing for Date: {date}")
