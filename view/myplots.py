# from helper.functs import sort_colors_by_brightness
import plotly.express as px
import pandas as pd
import json

class PlotBuilder():
    def _to_html(self, fig) -> dict:
        return json.loads(fig.to_json())

    def build_top10_bar(self, data: pd.DataFrame, year: int) -> tuple[dict, str]:
        description = f"This bar plot shows the top 10 in {year}"
        fig = px.bar(
            data,
            x='Ladder score',
            y='Country name',
            orientation='h',
            title=f'Top 10 Happiest Countries in {year}',
            labels={'Ladder score': 'Happiness Score', 'Country name': 'Country'}
        )
        return self._to_html(fig), description

    def build_happiness_map(self, data: pd.DataFrame, year: int) -> tuple[dict, str]:
        description = f"Heat map about Ladder score by country in {year}"
        fig = px.choropleth(
            data,
            locations='Country name',  # Use country names for locations
            locationmode='country names',  # Specify that we're using country names
            color='Ladder score',  # Use 'Life Ladder' for happiness values
            hover_name='Country name',  # Use 'Country name' for the hover information
            labels={'Ladder score': 'Life Ladder Score'},
            title=f'World Happiness in {year}'
        )
        return self._to_html(fig), description
    
    def build_scatterplot(self, data: pd.DataFrame, trendline: str | None = "lowess") -> tuple[dict, str]:
        description = "Scatterplot between Ladder score and GDP per capita"
        fig = px.scatter(
            data,
            x="Ladder score",
            y="Explained by: Log GDP per capita",
            trendline=trendline
        )
        return self._to_html(fig), description

    def build_linecountry(self, data: pd.DataFrame, selected_country: str) -> tuple[dict, str]:
        description = f"Area plot based on Ladder score per year for {selected_country}"
        fig = px.area(
            data, 
            x = 'Year', 
            y = 'Ladder score', 
            color = "Country name",
            title= f"Area Graph Example {selected_country}"
        )
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Value'
        )
        return self._to_html(fig), description

    def build_pietop3(self, data: pd.DataFrame, year: int, top: int) -> tuple[dict, str]:
        description = f"Pie chart showing the distribution of the top {top} happiest countries in {year}"
        fig = px.pie(
            data,
            names='Country name',
            values='Ladder score',
            title=f'Top {top} Happiest Countries Distribution in {year}'
        )
        return self._to_html(fig), description
