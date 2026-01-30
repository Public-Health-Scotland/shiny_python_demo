# from helper.functs import sort_colors_by_brightness
import plotly.express as px
# import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

list_color = ['#3F3685', '#0078D4', '#C73918', '#1E7F84', '#6B5C85', '#9B4393', '#655E9D', '#3393DD', '#AF69A9', '#948DA3']
# Load the built-in template
pio.templates["plotly_dark"]["layout"].update({
    # from ligther to darker
    'colorway': list_color
})
pio.templates["ggplot2"]["layout"].update({
    # from darker to ligther
    'colorway': list_color
})

class PlotBuilder():
    def __init__(self):
        self.margin = dict(t=40, b=0, l=0, r=0)

    async def build_top10_bar(self, data: pd.DataFrame, my_theme: str, year: int) -> tuple[str, str]:
        description = f"This bar plot shows the top 10 in {year}"
        fig = px.bar(
            data,
            x='Ladder score',
            y='Country name',
            orientation='h',
            title=f'Top 10 Happiest Countries in {year}',
            labels={'Ladder score': 'Happiness Score', 'Country name': 'Country'}, 
            template = my_theme
        )
        fig.update_layout(margin=self.margin)
        return fig.to_html(full_html=False, include_plotlyjs=False), description

    async def build_happiness_map(self, data: pd.DataFrame, my_theme: str, year: int) -> tuple[str, str]:
        description = f"Heat map about Ladder score by country in {year}"
        fig = px.choropleth(
            data,
            locations='Country name',  # Use country names for locations
            locationmode='country names',  # Specify that we're using country names
            color='Ladder score',  # Use 'Life Ladder' for happiness values
            hover_name='Country name',  # Use 'Country name' for the hover information
            color_discrete_sequence=px.colors.sequential.YlGnBu,
            labels={'Ladder score': 'Life Ladder Score'},
            title=f'World Happiness in {year}', 
            template = my_theme
        )
        fig.update_layout(margin=self.margin)
        return fig.to_html(full_html=False, include_plotlyjs=False), description
    
    async def build_scatterplot(self, data: pd.DataFrame, my_theme: str) -> tuple[str, str]:
        description = "Scatterplot between Ladder score and GDP per capita"
        fig = px.scatter(
            data,
            x="Ladder score",
            y="Explained by: Log GDP per capita",
            trendline="lowess", 
            template = my_theme
        )
        fig.update_layout(margin=self.margin)
        return fig.to_html(full_html=False, include_plotlyjs=False), description

    async def build_linecountry(self, data: pd.DataFrame, my_theme: str, selected_country: str) -> tuple[str, str]:
        description = f"Area plot based on Ladder score per year for {selected_country}"
        fig = px.area(
            data, 
            x = 'Year', 
            y = 'Ladder score', 
            color = "Country name",
            title= f"Area Graph Example {selected_country}",
            template=my_theme
        )
        fig.update_layout(
            margin=self.margin, 
            xaxis_title='Date',
            yaxis_title='Value'
        )
        return fig.to_html(full_html=False, include_plotlyjs=False), description

    async def build_pietop3(self, data: pd.DataFrame, my_theme: str, year: int, top: int) -> tuple[str, str]:
        description = f"Pie chart showing the distribution of the top {top} happiest countries in {year}"
        fig = px.pie(
            data,
            names='Country name',
            values='Ladder score',
            title=f'Top {top} Happiest Countries Distribution in {year}',
            template=my_theme
        )
        fig.update_layout(margin=self.margin)
        return fig.to_html(full_html=False, include_plotlyjs=False), description