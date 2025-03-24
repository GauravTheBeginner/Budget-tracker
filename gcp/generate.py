import random
import datetime
from lib.faker_helper import FakerClient
from lib.consts import GCP_REGIONS, GCP_COUNTRIES, GCP_SELLERS, PROJECT_NAME_MAPPING

class GCPGenerator:
    def __init__(self, date: datetime.date):
        """Initialize with a datetime.date object."""
        self.date = date
        self.fake = FakerClient()
        self.regions = list(GCP_REGIONS.keys())
        self.country = list(GCP_COUNTRIES.keys())
        self.seller = list(GCP_SELLERS.keys())
        self.project_name = list(PROJECT_NAME_MAPPING.keys())

    def generate_sku(self):
        """Generate a random SKU ID and description."""
        sku_id = f"SKU-{random.randint(100000, 999999)}"
        sku_description = self.fake.faker.sentence(nb_words=5)
        return sku_id, sku_description

    def generate_data(self, days: int):
        """Generate fake GCP billing data for the given number of days."""
        data = []

        for i in range(days):
            daily_date = self.date - datetime.timedelta(days=i) 
            daily_data, total_cost = [], 0

            while len(daily_data) < 50 or total_cost < 5000:
                sku_id, sku_description = self.generate_sku()
                usage_unit = random.randint(1, 100000)
                region = random.choice(self.regions)
                country = random.choice(self.country)
                seller = random.choice(self.seller)
                project_id = f"proj-{random.randint(1000, 9999)}"
                project_name = random.choice(self.project_name)
                account_number = self.fake.get_random_account_number()

                usage_amount = self.fake.get_random_usage(1, 500)
                cost = self.fake.get_random_cost(10, 1000)
                total_cost += cost

                row = {
                    "Invoice Date": daily_date.strftime("%Y-%m-%d"), 
                    "Usage Unit": usage_unit,
                    "Usage Amount": usage_amount,
                    "Cost": cost,
                    "Project Number": random.randint(100000, 999999),
                    "Country": country,
                    "Region": region,
                    "Account Number": account_number,
                    "SKU Description": sku_description,
                    "Seller Name": seller,
                    "SKU Id": sku_id,
                    "Usage Family": self.fake.faker.word(),
                    "Project ID": project_id,
                    "Project Name": project_name,
                }
                daily_data.append(row)

                if total_cost >= 8000:
                    break  

            data.extend(daily_data)

        print(f"✅ Generated {len(data)} records for {days} days starting from {self.date}.")
        return {"results": data}
