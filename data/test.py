# data_layer.py
from __future__ import annotations
import asyncio
import os
import pandas as pd
from typing import List, Optional

class DataLoader:
    """
    Async CSV loader for happiness.csv.
    - Caches the DataFrame in self.happiness_data
    - Keeps a country list in self.country_list (unique 'Country name' values)
    - Reloads only if the file changes (mtime) or when force=True
    """

    def __init__(self):
        self.path = 'data/WHR2024.csv'

        # Ensure we load at least the columns we need for the app
        self.read_csv_kwargs = {
            "usecols": [
                "Year",
                "Country name",
                "Ladder score",
                "Explained by: Log GDP per capita",
            ]
        }


        self.happiness_data: Optional[pd.DataFrame] = None
        self.country_list: List[str] = []  # populated after successful load
        self._mtime: Optional[float] = None
        self.dict_years = None

    # ---------------------------
    # Helpers
    # ---------------------------
    def _get_mtime(self) -> float:
        try:
            return os.path.getmtime(self.path)
        except FileNotFoundError:
            return -1.0

    async def _read_csv_async(self) -> pd.DataFrame:
        """Read CSV in a background thread to avoid blocking the event loop."""
        return await asyncio.to_thread(
            pd.read_csv,
            self.path,
            **self.read_csv_kwargs,
        )

    def _rebuild_country_list(self) -> None:
        """
        Refresh self.country_list from self.happiness_data.
        - Drops NaNs
        - Strips whitespace
        - Deduplicates
        - Sorts case-insensitively for predictable UI
        """

        col = "Country name"
        if self.happiness_data is None or col not in self.happiness_data.columns:
            # Keep predictable behavior if column missing (e.g., bad CSV)
            self.country_list = []
            return

        series = (
            self.happiness_data[col]
            .astype(str)
            .replace({"": pd.NA})
            .dropna()
        )

        unique_sorted = sorted(series.unique(), key=lambda s: s.casefold())
        self.country_list = unique_sorted

    # ---------------------------
    # Public API
    # ---------------------------
    async def load_data(self, force: bool = False) -> None:
        """
        Loads CSV into self.happiness_data, and refreshes self.country_list.
        Reload conditions:
          - first call,
          - file changed (mtime),
          - force=True
        """
        mtime = self._get_mtime()

        # Fast path: cached and unchanged
        if (not force) and (self.happiness_data is not None) and (mtime == self._mtime):
            return self.happiness_data

        if mtime < 0:
            raise FileNotFoundError(f"CSV not found: {self.path}")

        df = await self._read_csv_async()

        # Update cache + metadata
        self.happiness_data = df
        self._mtime = mtime

        # Update derived attributes
        self._rebuild_country_list()
        self.dict_years = {str(year): str(year) for year in sorted(self.happiness_data['Year'].unique())}

    def metadata(self) -> dict:
        """Return metadata about the loaded CSV."""
        size = os.path.getsize(self.path) if os.path.exists(self.path) else 0
        return {
            "path": self.path,
            "mtime": self._mtime,
            "size_bytes": size,
        }

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
