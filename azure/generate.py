from faker import Faker
from datetime import datetime, timedelta
import pandas as pd
import random
import time
from lib.consts import USAGE_FAM_MAPPING, RESOURCE_MAPPING, METER_SUB_CATEGORY, RESOURCE_LOCATION_MAPPING, METER_CATEGORY_MAPPING
from lib.faker_helper import FakerClient 

class AzureExtractor:
    def __init__(self, date):
        self.date = date
        self.service_names = list(USAGE_FAM_MAPPING.keys()) 
        self.resource_type = list(RESOURCE_MAPPING.keys())
        self.meter_sub_category = list(METER_SUB_CATEGORY.keys())
        self.resource_location_mapping = list(RESOURCE_LOCATION_MAPPING.keys())
        self.meter_category = list(METER_CATEGORY_MAPPING.keys())

    def get_subscriptions(self):
        """Generate fake subscription data."""
        return [
            {
                "subscription_id": FakerClient.get_random_account_number(),
                "subscription_name": FakerClient.get_random_company()
            }
            for _ in range(5)
        ]
    def get_random_service(self):
        """Returns a random Azure service and its usage family."""
        service_name = random.choice(self.service_names)
        return service_name
    def get_random_resource_type(self):
        """Returns a random Azure resource type."""
        return random.choice(self.resource_type)
    def get_random_meter_sub_category(self):
        """Returns a random Azure meter sub category."""
        return random.choice(self.meter_sub_category)
    def get_random_resource_location(self):
        """Returns a random Azure resource location."""
        return random.choice(self.resource_location_mapping)
    def get_meter_category(self):
        """Returns a random Azure meter category."""
        return random.choice(self.meter_category)

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
                self.get_random_service(),                # Service Name
                self.get_random_resource_location(),                # Resource Location
                FakerClient.faker.word(),                 # Meter
                self.get_meter_category(),                # Meter Category
                self.get_random_meter_sub_category(),                 # Meter Sub Category
                self.get_random_resource_type(),            # Resource Type
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
        return df
