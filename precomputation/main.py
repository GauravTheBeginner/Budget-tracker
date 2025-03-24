from precomputation.database_queries import DatabaseQueries
from lib.database import DatabaseHelper


class PrecomputedTable:
    def __init__(self):
        pass

    def process_operations(self):
        # Load Data from All table to Precalculated table
        with DatabaseHelper() as db:
            db_queries = DatabaseQueries(db.engine)
            db_queries.create_total_spent_by_account_table()
            db_queries.create_daily_usage_cost_by_vendor()
            db_queries.create_monthly_estimated_spend()
            db_queries.create_top_spending_drivers()
            db_queries.create_daily_compute_usage_cost_trend()
            
