from faker import Faker
from datetime import datetime, timedelta
import pandas as pd
import random
import time
from lib.faker_helper import FakerClient 

class AzureExtractor:
    def __init__(self, date):
        self.date = date

    def get_subscriptions(self):
        """Generate fake subscription data."""
        return [
            {
                "subscription_id": FakerClient.get_random_account_number(),
                "subscription_name": FakerClient.get_random_company()
            }
            for _ in range(5)
        ]

    def get_cost_data(self, subscription_id):
        """Generate fake cost data for a subscription."""
        data = []
        for _ in range(random.randint(5, 10)): 
            row = [
                FakerClient.get_random_cost(10, 500),     # Cost
                FakerClient.get_random_usage(1, 100),     # Usage Quantity
                self.date.strftime("%Y-%m-%d"),           # Invoice Date
                subscription_id,                          # Account Number
                FakerClient.get_random_company(),         # Account Name
                FakerClient.faker.word(),                 # Service Name
                FakerClient.faker.city(),                 # Resource Location
                FakerClient.faker.word(),                 # Meter
                FakerClient.faker.word(),                 # Meter Category
                FakerClient.faker.word(),                 # Meter Sub Category
                FakerClient.faker.word(),                 # Resource Type
                FakerClient.faker.word()                  # Resource Group
            ]
            data.append(row)
        return data

    def extract_data(self):
        """Extract fake cost data for all subscriptions."""
        columns = [
            "Cost", "Usage Quantity", "Invoice Date", "Account Number", "Account Name", 
            "Service Name", "Resource Location", "Meter", "Meter Category", "Meter Sub Category", 
            "Resource Type", "Resource Group"
        ]
        data = []
        
        subscriptions = self.get_subscriptions()
        print(f"Generated {len(subscriptions)} subscriptions.")
        
        for idx, sub in enumerate(subscriptions):
            print(f"Processing subscription {idx + 1}/{len(subscriptions)}: {sub['subscription_id']}")
            rows = self.get_cost_data(sub['subscription_id'])

            for row in rows:
                row[4] = row[4].split("(")[0].strip()  
                data.append(row)
            
            time.sleep(1)  
        
        df = pd.DataFrame(data, columns=columns)
        print(df)
        return df
