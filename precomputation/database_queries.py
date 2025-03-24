from lib.db_helper import load_df_to_table
import pandas as pd

class DatabaseQueries:

    def __init__(self, db_engine):
        self.db_engine = db_engine

    def create_total_spent_by_account_table(self):
        query = """
        SELECT 
            "Account Name",
            "Vendor",
            SUM("Cost") AS "Cost (Total)"
        FROM 
            summary_table
        GROUP BY 
            "Account Name", 
            "Vendor"
        ORDER BY 
            SUM("Cost") DESC;
        """
        df = pd.read_sql(query, self.db_engine)
        load_df_to_table("total_spent_by_account", df, True)

    def create_daily_usage_cost_by_vendor(self):
        query = """
        SELECT
            "Invoice Date"::date AS "Date", 
            "Vendor",
            SUM("Cost") AS "DailyCost"
        FROM 
            summary_table 
        WHERE
            "Invoice Date"::date >= current_date - interval '90 days'
        GROUP BY
            "Date",
            "Vendor"
        ORDER BY
            "Date";
        """
        df = pd.read_sql(query, self.db_engine)
        load_df_to_table("daily_usage_cost_by_vendor", df, True)

    def create_monthly_estimated_spend(self):
        query = """
        WITH CurrentMonth AS (
            SELECT
                "Vendor",
                SUM("Cost") as "CurrentMonthCost"
            FROM
                summary_table 
            WHERE
                date_trunc('month', "Invoice Date"::date) = date_trunc('month', current_date)
            GROUP BY
                "Vendor"
        ),
        PreviousMonth AS (
            SELECT
                "Vendor",
                SUM("Cost") as "PreviousMonthCost"
            FROM
                summary_table 
            WHERE
                date_trunc('month', "Invoice Date"::date) = date_trunc('month', current_date - interval '1 month')
            GROUP BY
                "Vendor"
        ),
        VendorSpecific AS (
            SELECT
                cm."Vendor",
                cm."CurrentMonthCost",
                pm."PreviousMonthCost",
                CASE
                    WHEN pm."PreviousMonthCost" = 0 THEN NULL
                    ELSE ((cm."CurrentMonthCost" - pm."PreviousMonthCost") / pm."PreviousMonthCost") * 100
                END as "PercentageChange"
            FROM
                CurrentMonth cm
            LEFT JOIN PreviousMonth pm ON cm."Vendor" = pm."Vendor"
        ),
        Total AS (
            SELECT
                'all' as "Vendor",
                SUM(cm."CurrentMonthCost") as "CurrentMonthCost",
                SUM(pm."PreviousMonthCost") as "PreviousMonthCost",
                CASE
                    WHEN SUM(pm."PreviousMonthCost") = 0 THEN NULL
                    ELSE ((SUM(cm."CurrentMonthCost") - SUM(pm."PreviousMonthCost")) / SUM(pm."PreviousMonthCost")) * 100
                END as "PercentageChange"
            FROM
                CurrentMonth cm
            LEFT JOIN PreviousMonth pm ON cm."Vendor" = pm."Vendor"
        )
        SELECT * FROM VendorSpecific
        UNION ALL
        SELECT * FROM Total;
        """
        df = pd.read_sql(query, self.db_engine)
        load_df_to_table("monthly_estimated_spend", df, True)

    def create_top_spending_drivers(self):
        query = """
        SELECT
            "Service Name",
            "Usage Family",
            SUM("Cost") as "TotalCost",
            "Vendor" 
        FROM
            summary_table 
        WHERE
            "Invoice Date"::date > current_date - interval '30 days'
        GROUP BY
            "Service Name", "Usage Family", "Vendor"
        ORDER BY
            "TotalCost" DESC
        LIMIT 100;
        """
        df = pd.read_sql(query, self.db_engine)
        load_df_to_table("top_spending_drivers", df, True)

    def create_daily_compute_usage_cost_trend(self):
        query = """
        SELECT
            "Invoice Date"::date AS "Date",
            SUM("Cost") AS "DailyCost",
            "Vendor"
        FROM 
            summary_table 
        WHERE
            "Invoice Date"::date >= current_date - interval '60 days'
        GROUP BY
            "Date",
            "Vendor"
        ORDER BY
            "Date";
        """
        df = pd.read_sql(query, self.db_engine)
        load_df_to_table("daily_compute_usage_cost_trend", df, True)
