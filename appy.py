from shiny import App, ui, reactive
import plotly.express as px
import json
from helper.functs import get_my_www_folder

# ---------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------
app_ui = ui.page_fluid(
    ui.layout_columns(
        ui.input_dark_mode(id="mode"),
        title="Multi-Plotly Dark Mode App",
        col_widths=[12]
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Medals by Nation"),
            ui.div(id="chart_medals", style="height: 380px; width: 100%;"),
            full_screen=True
        ),
        ui.card(
            ui.card_header("Iris Sepal Width vs Length"),
            ui.div(id="chart_iris", style="height: 380px; width: 100%;"),
            full_screen=True
        ),
        col_widths=[6, 6]
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Gapminder Life Expectancy"),
            ui.div(id="chart_gapminder", style="height: 380px; width: 100%;"),
            full_screen=True
        ),
        col_widths=[12]
    ),
    ui.head_content(
        ui.tags.script(src="www/js/plotly-4.1.1.min.js"),
        ui.tags.script(src="www/js/plotly-theme.js")
    ),
    window_title="Multi-Plotly Shiny App"
)

# ---------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------
def server(input, output, session):
    async def send_plotly(output_id: str, fig, description: str):
        """Send a Plotly figure to a target HTML container for rendering."""
        chart_dict = json.loads(fig.to_json())
        chart_dict["target"] = output_id
        if description:
            chart_dict["aria-label"] = description
        await session.send_custom_message("render_plotly_chart", chart_dict)

    # Chart 1
    @reactive.Effect
    async def _():
        """Send 'Medals by Nation' Plotly figure for screen readers."""
        df_medals = px.data.medals_long()
        fig1 = px.bar(df_medals, x="nation", y="count", color="medal", title="Medals by Nation")
        description = "Bar chart showing the count of medals by nation, with different colors representing gold, silver, and bronze medals."
        await send_plotly("chart_medals", fig1, description)

    # Chart 2
    @reactive.Effect
    async def _():
        """Send 'Iris Sepal Width vs Length' Plotly figure for screen readers."""
        df_iris = px.data.iris()
        fig2 = px.scatter(df_iris, x="sepal_length", y="sepal_width", color="species", title="Iris Dataset")
        description = "Scatter plot showing the relationship between sepal length and width for different species of iris flowers."
        await send_plotly("chart_iris", fig2, description)

    # Chart 3
    @reactive.Effect
    async def _():
        """Send 'Gapminder Life Expectancy' Plotly figure for screen readers."""
        df_gap = px.data.gapminder().query("year == 2007")
        fig3 = px.scatter(df_gap, x="gdpPercap", y="lifeExp", size="pop", color="continent", log_x=True, title="GDP vs Life Expectancy")
        description = "Scatter plot showing the relationship between GDP per capita and life expectancy for different continents."
        await send_plotly("chart_gapminder", fig3, description)

app = App(app_ui, server, static_assets={"/www": get_my_www_folder()})
