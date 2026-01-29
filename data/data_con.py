import pandas as pd

class DataLoader:
    def __init__(self):
        self.happiness_data = None
        self.country_list = None
        self.dict_years = None

    def load_data(self):
        self.happiness_data = pd.read_csv('data/WHR2024.csv', 
                                          usecols = ['Year', 'Country name', 'Ladder score', 'Explained by: Log GDP per capita'])
        
        self.country_list = self.happiness_data["Country name"].unique().tolist()
        self.dict_years = {str(year): str(year) for year in sorted(self.happiness_data['Year'].unique())}

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

    async def get_clean_data_for_scatter(self):
        if self.happiness_data is not None:
            return self.happiness_data[["Ladder score", "Explained by: Log GDP per capita"]].dropna()
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
