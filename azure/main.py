from azure.load import AzureLoader
from azure.generate import AzureExtractor

class Azure:
    def __init__(self, date):
        self.date = date

    def process_operations(self):
        azure_extractor = AzureExtractor(self.date)
        results = azure_extractor.extract_data()
        print(results)
        azure_loader = AzureLoader(results)
        azure_loader.load_data()
