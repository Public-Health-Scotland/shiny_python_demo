import pandas as pd

class DataLoader:
    def __init__(self):
        self.happiness_data = None

    def load_data(self):
        self.happiness_data = pd.read_csv('data/WHR2024.csv', 
                                          usecols = ['Year', 'Country name', 'Ladder score', 'Explained by: Log GDP per capita'])
        return self.happiness_data
    
    def get_country_list(self):
        if self.happiness_data is not None:
            return self.happiness_data["Country name"].unique().tolist()
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
    
    def get_dict_years(self):
        if self.happiness_data is not None:
            return {str(year): str(year) for year in sorted(self.happiness_data['Year'].unique())}
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
        
    def get_shape(self):
        if self.happiness_data is not None:
            return f"Rows {self.happiness_data.shape[0]} cols {self.happiness_data.shape[1]}"
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
    
    def get_range_years(self):
        if self.happiness_data is not None:
            years = sorted(self.happiness_data['Year'].unique())
            return f"from {min(years)} to {max(years)}"
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
        
    def get_range_ladder_score(self):
        if self.happiness_data is not None:
            scores = self.happiness_data['Ladder score']
            # return f"from {scores.min():.2f} to {scores.max():.2f}"
            return f"from {round(scores.min(), 2)} to {round(scores.max(), 2)}"
            
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
    
    async def get_top10_happiest_countries(self, year: int):
        if self.happiness_data is not None:
            data = self.happiness_data[self.happiness_data['Year'] == year]
            data = data.sort_values(by='Ladder score', ascending=False).head(10)
            return data
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
    
    async def get_data_by_year(self, year: int):
        if self.happiness_data is not None:
            return self.happiness_data[self.happiness_data['Year'] == year]
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
        
    async def get_data_by_country(self, country: str):
        if self.happiness_data is not None:
            return self.happiness_data[self.happiness_data["Country name"] == country].sort_values(by='Year', ascending=True)
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
