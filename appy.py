from shiny import App, ui, reactive
import plotly.express as px
import json
from helper.functs import get_my_www_folder

# ---------------------------------------------------------------------
# Python Helper to send any Plotly figure to a specific HTML container
# ---------------------------------------------------------------------
async def send_plotly(session, output_id: str, fig):
    chart_dict = json.loads(fig.to_json())
    chart_dict["target"] = output_id
    await session.send_custom_message("render_plotly_chart", chart_dict)


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
    # Chart 1
    @reactive.Effect
    async def _():
        df_medals = px.data.medals_long()
        fig1 = px.bar(df_medals, x="nation", y="count", color="medal", title="Medals by Nation")
        await send_plotly(session, "chart_medals", fig1)

    # Chart 2
    @reactive.Effect
    async def _():
        df_iris = px.data.iris()
        fig2 = px.scatter(df_iris, x="sepal_length", y="sepal_width", color="species", title="Iris Dataset")
        await send_plotly(session, "chart_iris", fig2)

    # Chart 3
    @reactive.Effect
    async def _():
        df_gap = px.data.gapminder().query("year == 2007")
        fig3 = px.scatter(df_gap, x="gdpPercap", y="lifeExp", size="pop", color="continent", log_x=True, title="GDP vs Life Expectancy")
        await send_plotly(session, "chart_gapminder", fig3)

app = App(app_ui, server, static_assets={"/www": get_my_www_folder()})
