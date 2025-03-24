import random
import datetime
from lib.consts import USAGE_FAM_MAPPING
from lib.faker_helper import FakerClient

class AWSGenerator:
    def __init__(self, date: datetime.date):
        """Initialize with a datetime.date object."""
        self.date = date
        self.fake = FakerClient()
        self.service_names = list(USAGE_FAM_MAPPING.keys())

    def get_random_service(self):
        """Returns a random AWS service and its usage family."""
        service_name = random.choice(self.service_names)
        return service_name, USAGE_FAM_MAPPING.get(service_name)

    def generate_data(self, days: int):
        """Generates AWS cost data for the given number of days."""
        data = []

        for i in range(days):
            daily_date = self.date - datetime.timedelta(days=i) 
            daily_data, total_cost = [], 0

            while len(daily_data) < 50 or total_cost < 5000:
                service_name, usage_family = self.get_random_service()
                cost, quantity = self.fake.get_random_cost(100, 500), self.fake.get_random_usage(1, 100)
                total_cost += cost

                daily_data.append({
                    "invoice_date": daily_date.strftime("%Y-%m-%d"),
                    "cost": cost,
                    "usage_quantity": quantity,
                    "account_number": self.fake.get_random_account_number(),
                    "usage_family": usage_family,
                    "service_name": service_name,
                    "account_name": self.fake.get_random_company(),
                    "vendor": "AWS"
                })

                if total_cost >= 8000:
                    break 

            data.extend(daily_data)

        print(f"✅ Generated {len(data)} records for {days} days starting from {self.date}.")
        return {"results": data}
