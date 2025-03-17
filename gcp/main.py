from gcp.generate import GCPGenerator
from gcp.load import GCPLoader

class GCP:
    def __init__(self, date):
        self.date = date

    def process_operations(self):
        """Generate and load GCP billing data."""
        gcp_generator = GCPGenerator(self.date)
        results = gcp_generator.generate_data(days=1)
        # print(results)
        gcp_loader = GCPLoader(results)
        gcp_loader.load_data()
