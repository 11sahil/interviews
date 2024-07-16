import pandas as pd

class DataStore:
    def __init__(self):
        self.data = pd.DataFrame()

    def process_and_save_data(self, data):
        df = pd.DataFrame(data)
        self.data = pd.concat([self.data, df], ignore_index=True) #self.data.append(df, ignore_index=True)
        self.data['rating'] = 0

    def get_info_by_filter(self,**filters):
        if self.data.empty:
            return pd.DataFrame()
        
        query_df = self.data.copy()
        for key, value in filters.items():
            query_df = query_df[query_df[key] == value]
        
        return query_df

    def update_field(self, key: str, value, **filters):
        if self.data.empty:
            return []

        mask = pd.Series([True] * len(self.data))
        print(mask)
        for f_key, f_value in filters.items():
            mask &= (self.data[f_key] == f_value)
        print(mask)
        self.data.loc[mask, key] = value
        
        return self.data.loc[mask]