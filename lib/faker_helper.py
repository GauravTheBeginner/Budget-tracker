from faker import Faker
import random

class FakerClient:
    faker = Faker()

    @staticmethod
    def get_random_choice(choices: list):
        """Returns a random item from the given list."""
        return random.choice(choices) if choices else None

    @staticmethod
    def get_random_cost(min_cost=50, max_cost=200):
        """Generates a random cost value within the given range."""
        return round(random.uniform(min_cost, max_cost), 2)

    @staticmethod
    def get_random_usage(min_usage=0.1, max_usage=10):
        """Generates a random usage quantity within the given range."""
        return round(random.uniform(min_usage, max_usage), 2)

    @staticmethod
    def get_random_account_number():
        """Generates a random account number using Faker."""
        return FakerClient.faker.uuid4()

    @staticmethod
    def get_random_company():
        """Generates a random company name."""
        return FakerClient.faker.company()

    @staticmethod
    def get_random_date(start_days_ago=30, end_days_ago=0):
        """Generates a random date between the given range in the past."""
        return FakerClient.faker.date_between(start_date=f"-{start_days_ago}d", end_date=f"-{end_days_ago}d")

