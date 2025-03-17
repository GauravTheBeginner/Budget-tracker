
from rn.generate import RNGenerator
from rn.load import RNLoader

class RN:
    def __init__(self, date):
        self.date = date

    def process_operations(self):
        """Extract, generate, and load RN cloud billing data."""
        rn_extractor = RNGenerator(self.date)
        results = rn_extractor.generate_data(days=1)
        # print(results)
        rn_loader = RNLoader(results)
        rn_loader.load_data()
