from aws.load import AWSLoader
from aws.generate import AWSGenerator


class AWS:
    def __init__(self, date):
        self.date = date

    def process_operations(self):
        aws_extractor = AWSGenerator(self.date)
        results = aws_extractor.generate_data(days=1)
        # print(results)
        aws_loader = AWSLoader(results)
        aws_loader.load_data()
