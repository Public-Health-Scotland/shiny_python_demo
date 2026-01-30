import pandas as pd
import asyncio

class DataLoader:
    def __init__(self):
        # This is the file path to the CSV data
        self.path: str = 'data/WHR2024.csv'
        # Ensure we load at least the columns we need for the app
        self.read_csv_kwargs = {
            "usecols": [
                "Year",
                "Country name",
                "Ladder score",
                "Explained by: Log GDP per capita",
            ]
        }
        self.happiness_data: pd.DataFrame = None
        self.country_list: list[str] = []
        self.dict_years: dict = {}

    async def load_data(self) -> pd.DataFrame:
        self.happiness_data = await asyncio.to_thread(
            pd.read_csv,
            self.path,
            **self.read_csv_kwargs,
        )
        
        # pd.read_csv('data/WHR2024.csv', usecols = ['Year', 'Country name', 'Ladder score', 'Explained by: Log GDP per capita'])
        if self.happiness_data is not None:
            self.country_list = self.happiness_data["Country name"].unique().tolist()
            self.dict_years = {str(year): str(year) for year in sorted(self.happiness_data['Year'].unique())}
        
        return self.happiness_data

    async def get_top10_happiest_countries(self, year: int, top: int) -> pd.DataFrame:
        if self.happiness_data is not None:
            data = self.happiness_data[self.happiness_data['Year'] == year]
            data = data.sort_values(by='Ladder score', ascending=False).head(top)
            return data
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
    
    async def get_data_by_year(self, year: int) -> pd.DataFrame:
        if self.happiness_data is not None:
            return self.happiness_data[self.happiness_data['Year'] == year]
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
        
    async def get_data_by_country(self, country: str) -> pd.DataFrame:
        if self.happiness_data is not None:
            return self.happiness_data[self.happiness_data["Country name"] == country].sort_values(by='Year', ascending=True)
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")

    async def get_clean_data_for_scatter(self) -> pd.DataFrame:
        if self.happiness_data is not None:
            return self.happiness_data[["Ladder score", "Explained by: Log GDP per capita"]].dropna()
        else:
            raise ValueError("Data not loaded. Please call load_data() first.")
