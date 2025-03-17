import random
import datetime
import pandas as pd
from lib.faker_helper import FakerClient  

class RNGenerator:
    def __init__(self, date):
        self.date = date
        self.fake = FakerClient()

    def generate_data(self, days):
        """Generate random RN cloud billing data for the given number of days."""
        data = []
        start_date = datetime.datetime.now() - datetime.timedelta(days=days)

        for i in range(days):
            daily_date = start_date + datetime.timedelta(days=i)
            month_year_timestamp = datetime.datetime(daily_date.year, daily_date.month, 1)  

            daily_data = []
            total_cost = 0

            while len(daily_data) < 50 or total_cost < 5000:
                cost = FakerClient.get_random_cost(100, 500)
                usage_amount = FakerClient.get_random_usage(1, 100)
                total_cost += cost

                row = {
                    "UsageEndDate": daily_date.strftime("%Y-%m-%d"),
                    "MonthYear": month_year_timestamp,  
                    "BlendedRate": round(random.uniform(0.01, 1.0), 4),
                    "SellerOfRecord": FakerClient.get_random_company(),
                    "Environment": random.choice(["Production", "Staging", "Development"]),
                    "UnitOfMeasure": random.choice(["GB", "TB", "Hours"]),
                    "CurrencyCode": random.choice(["USD", "EUR", "INR"]),
                    "user:termstartdate": (daily_date - datetime.timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                    "user:termenddate": (daily_date + datetime.timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
                    "InvoiceID": random.randint(100000, 999999),
                    "Business Unit": random.choice(["CloudOps", "Finance", "Marketing"]),
                    "LinkedAccountName": FakerClient.get_random_company(),
                    "ProductCode": f"RN-{random.randint(1000, 9999)}",
                    "ProductName": FakerClient.faker.word(),
                    "ResourceId": FakerClient.get_random_account_number(),
                    "UsageType": FakerClient.faker.word(),
                    "ItemDescription": FakerClient.faker.sentence(),
                    "AvailabilityZone": random.choice(["us-east-1a", "us-west-2b", "eu-central-1c"]),
                    "Cost": cost,
                    "Usage Amount": usage_amount
                }
                daily_data.append(row)

                if total_cost >= 8000:
                    break

            data.extend(daily_data)

        print(f"Generated {len(data)} records for {days} days.")    
        return {"results": data}
