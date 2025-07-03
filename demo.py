import plotly.express as px
import pandas as pd
from shiny import App, ui, render
import plotly.io as pio

pio.templates.default = "plotly_dark"
# Sample data
df = pd.DataFrame({
    "year": [2020, 2020, 2021, 2021],
    "category": ["A", "B", "A", "B"],
    "value": [100, 150, 200, 250]
})
app_ui = ui.page_navbar(
    ui.nav_panel(
        "Bar Chart",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select(
                    "year", "Select a Year:",
                    {str(year): str(year) for year in sorted(df['year'].unique())}
                )
            ),
            ui.output_ui("bar_plot")
        )
    )
)


def server(input, output, session):
    @output
    @render.ui
    def bar_plot():
        selected_year = int(input.year())
        filtered_df = df[df["year"] == selected_year]
        # filtered_df = df.copy()
        fig = px.bar(filtered_df, x="category", y="value", title=f"Data for {selected_year}")
        return ui.HTML(fig.to_html(full_html=True))

app = App(app_ui, server)
