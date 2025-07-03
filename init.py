import pandas as pd
import plotly.express as px
from shiny import App, render, reactive, ui
import faicons as fa

file_path = 'data/WHR2024.csv'  # Ensure this is the correct path to your CSV file
happiness_data = pd.read_csv(file_path, delimiter=',')
dict_years = {str(year): str(year) for year in sorted(happiness_data['Year'].unique())}
country_list = happiness_data["Country name"].unique()

app_ui = ui.page_navbar(
    ui.nav_panel("Home", 
        ui.h2("General info"),
        ui.layout_column_wrap(
            ui.value_box(
                "KPI number of records",
                f"Rows {happiness_data.shape[0]} cols {happiness_data.shape[1]}",
                "source: dataset",
                showcase = fa.icon_svg("database")
            ),
            ui.value_box(
                "KPI happiness scale",
                f"from {min(happiness_data.Year)} to {max(happiness_data.Year)}",
                "source: dataset",
                showcase=fa.icon_svg("calendar")
            ),
            ui.value_box(
                "KPI Title",
                f"from {round(min(happiness_data['Ladder score']),1)} to {round(max(happiness_data['Ladder score']), 1)}",
                "source: dataset",
                showcase=fa.icon_svg("face-smile")
            )
        ),
        
        # First row: 2 cards side by side
        ui.layout_columns(
            ui.card(ui.card_header("happiness data"),
                    ui.output_data_frame("df_table"),
                    full_screen=True
            ),
            ui.card(ui.card_header("Scatter plot"), ui.output_ui("scatterplot"), full_screen=True),
            col_widths=[6, 6]
        ),

        # Second row: 1 card centered
        ui.layout_columns(
            ui.card(ui.card_header("time happiness",
                    ui.popover(
                        ui.span(
                            fa.icon_svg("ellipsis"),
                            style="position:absolute; top: 5px; right: 7px;",
                        ),
                        "Select a country",
                        ui.input_selectize("ddCountry", "country", country_list.tolist()),
                        id="card_popover"
                    ),
                    ui.output_ui("linecountry"),
                    full_screen=True
                )
            ),
            col_widths=[12],
            col_gutters=True,
            row_gutters=True
        )

    ),
    ui.nav_panel("Bar", 
        ui.h2("Bar plot happiness"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("World Happiness top 10"),
                ui.input_select("year", "Select a Year:", dict_years)
            ),
            ui.output_ui("top10_bar")
        )
    ),
    ui.nav_panel("Map", 
        ui.h2("Cloropleth happiness"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("Map plot"),
                ui.input_select("mapyear", "Select a Year:", dict_years)
            ),
            ui.output_ui("happiness_map")
        )
    ),
    ui.nav_menu(
        "More",
        ui.nav_panel("Contact", ui.h2("Contact us")),
        ui.nav_panel("Help", ui.h2("Help Page"))
    ),# Dropdown menu
    ui.nav_spacer(), 
    ui.nav_control(ui.input_dark_mode(id="dark_mode_switch"))
)

def server(input, output, session):
    @reactive.Calc
    def current_theme():
        if input.dark_mode_switch() == "dark":
            template = "plotly_dark"
        else:
            template = "plotly_white"
        return template
    
    
    @output
    @render.data_frame
    def df_table():
        return render.DataGrid(happiness_data, width="fit-content", height=350)

    @output
    @render.ui
    def top10_bar():
        data = happiness_data[happiness_data['Year'] == int(input.year())]
        data = data.sort_values(by='Ladder score', ascending=False).head(10)
        fig = px.bar(
            data,
            x='Ladder score',
            y='Country name',
            orientation='h',
            title=f'Top 10 Happiest Countries in {input.year()}',
            labels={'Ladder score': 'Happiness Score', 'Country name': 'Country'}
        )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template = current_theme())
        return ui.HTML(fig.to_html(full_html=True))

    @output
    @render.ui
    def happiness_map():
        data = happiness_data[happiness_data['Year'] == int(input.mapyear())]
        fig = px.choropleth(
            data,
            locations='Country name',  # Use country names for locations
            locationmode='country names',  # Specify that we're using country names
            color='Ladder score',  # Use 'Life Ladder' for happiness values
            hover_name='Country name',  # Use 'Country name' for the hover information
            color_continuous_scale=px.colors.sequential.YlGnBu,
            labels={'Ladder score': 'Life Ladder Score'},
            title=f'World Happiness in {input.year()}'
        )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template = current_theme())
        fig_html = fig.to_html(full_html=True)
        return ui.HTML(fig_html)

    @output
    @render.ui
    def scatterplot():
        fig = px.scatter(
                happiness_data,
                x="Ladder score",
                y="Explained by: Log GDP per capita",
                # color=None if color == "none" else color,
                trendline="lowess")
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template = current_theme())
        return ui.HTML(fig.to_html(full_html=True))

app = App(app_ui, server)
