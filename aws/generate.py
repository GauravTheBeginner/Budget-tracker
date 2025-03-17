import random
import datetime
from lib.consts import USAGE_FAM_MAPPING
from lib.faker_helper import FakerClient

class AWSGenerator:
    def __init__(self, date):
        self.date = date
        self.fake = FakerClient() 
        self.service_names = list(USAGE_FAM_MAPPING.keys()) 

    def get_random_service(self):
        """Returns a random AWS service and its usage family."""
        service_name = random.choice(self.service_names)
        usage_family = USAGE_FAM_MAPPING.get(service_name)
        return service_name, usage_family

    def generate_data(self, days):
        data = []
        start_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        for i in range(days):
            daily_date = start_date + datetime.timedelta(days=i)
            total_cost = 0
            daily_data = []
            
            while len(daily_data) < 50 or total_cost < 5000:
                service_name, usage_family = self.get_random_service()
                cost = FakerClient.get_random_cost(100, 500)  
                quantity = FakerClient.get_random_usage(1, 100) 
                total_cost += cost

                row = {
                    "invoice_date": daily_date.strftime("%Y-%m-%d"),
                    "cost": cost,
                    "usage_quantity": quantity,
                    "account_number": FakerClient.get_random_account_number(), 
                    "usage_family": usage_family,
                    "service_name": service_name,
                    "account_name": FakerClient.get_random_company(), 
                    "vendor": "AWS"
                }
                daily_data.append(row)

                if total_cost >= 8000:
                    break

            data.extend(daily_data)

        print(f"Generated {len(data)} records for {days} days.")    
        return {"results": data}
