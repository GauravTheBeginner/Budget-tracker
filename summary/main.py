from summary.load import SummaryTableLoader
from summary.extract import SummaryTableExtractor


class SummaryTable:
    def __init__(self):
        pass

    def process_operations(self):
        # Extract data from AWS & GCP Table
        self.summary_extractor = SummaryTableExtractor()
        df = self.summary_extractor.extract_data()

        # Load the DF to the Summary Table
        summary_loader = SummaryTableLoader(df)
        summary_loader.load_data()
