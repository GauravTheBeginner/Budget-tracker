from lib.db_helper import load_df_to_table


class SummaryTableLoader:
    def __init__(self, df):
        self.df = df

    def load_data(self):
        load_df_to_table("summary_table", self.df)
