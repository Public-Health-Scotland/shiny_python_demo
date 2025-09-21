import polars as pl
import plotly.express as px
from shiny import App, render, reactive, ui
import faicons as fa
from pathlib import Path

assets_folder = Path(__file__).parent / 'static'

happiness_data = pl.read_csv('data/WHR2024.csv', columns = ['Year', 'Country name', 'Ladder score', 'Explained by: Log GDP per capita'])

list_years = sorted(happiness_data['Year'].unique())
dict_years = {str(year): str(year) for year in list_years}
happiness_data = happiness_data.with_columns(
    pl.col("Country name").cast(pl.Categorical)
)
country_list = happiness_data["Country name"].unique().to_list()

def my_dropdown_year(id):
    return ui.input_select(id, "Select a Year:", dict_years)

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
                f"from {min(list_years)} to {max(list_years)}",
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
            ui.card(ui.card_header("Scatter plot"), 
                    ui.output_ui("scatterplot"), 
                    full_screen=True),
            col_widths=[6, 6]
        ),

        # Second row: 1 card centered
        ui.layout_columns(
            ui.card(ui.card_header("time happiness",
                    ui.popover(
                        ui.span(
                            fa.icon_svg("ellipsis"),
                            style="position:absolute; top: 5px; right: 7px;",),
                        "Select a country",
                        ui.input_selectize("ddCountry", "country", country_list))),
                    ui.output_ui("linecountry"),
                    full_screen=True),
            col_widths=[12]
        )
    ),
    ui.nav_panel("Bar plot", 
        ui.h2("Bar plot happiness"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("World Happiness top 10"),
                my_dropdown_year("year")
            ),
            ui.output_ui("top10_bar")
        )
    ),
    ui.nav_panel("Geodata", 
        ui.h2("Cloropleth happiness"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("Map plot"),
                my_dropdown_year("mapyear")
            ),
            ui.output_ui("happiness_map")
        )
    ),
    ui.nav_menu(
        "More data",
        ui.nav_panel("Database", ui.h2("Information from db")),
        ui.nav_panel("Contact", ui.h2("Contact us")),
        ui.nav_panel("Help", ui.h2("Help Page"))
    ),
    ui.nav_spacer(), 
    ui.nav_control(ui.input_dark_mode(id="dark_mode_switch")),
    title=ui.tags.a(
        ui.tags.img(src="static/logo.png", height="45px"), "",
        href="https://www.publichealthscotland.scot/",
        target="_blank",
        class_="navbar-brand d-flex align-items-center"
    ),
    lang="en",
    navbar_options=ui.navbar_options(position="fixed-top")
)

def server(input, output, session):
    @reactive.Calc
    def current_theme():
        if input.dark_mode_switch() == "dark":
            template = "plotly_dark"
        else:
            template = "ggplot2"
        return template
    
    @reactive.effect
    @reactive.event(input.dark_mode_switch)
    def _():
        ui.remove_ui("header_color")
        color_gridheader = 'grey' if input.dark_mode_switch() == 'dark' else 'white'
        css_gridheader = f" shiny-data-frame {{ --shiny-datagrid-grid-header-bgcolor: {color_gridheader} !important }}"
        
        if css_gridheader:
            style = ui.tags.style(css_gridheader, id='header_color')
            ui.insert_ui(style, selector='head')
    
    @output
    @render.data_frame
    def df_table():
        return render.DataGrid(happiness_data, width="fit-content", height=350, filters=True)

    @output
    @render.ui
    async def top10_bar():
        data = happiness_data.filter(pl.col("Year") == int(input.mapyear()))
        data = data.sort(by='Ladder score', descending=True).head(10)
        fig = px.bar(
            data,
            x='Ladder score',
            y='Country name',
            orientation='h',
            title=f'Top 10 Happiest Countries in {input.year()}',
            labels={'Ladder score': 'Happiness Score', 'Country name': 'Country'}
        )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template = current_theme())
        return ui.HTML(fig.to_html(full_html=False))

    @output
    @render.ui
    async def happiness_map():
        data = happiness_data.filter(pl.col("Year") == int(input.mapyear()))
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
        return ui.HTML(fig.to_html(full_html=False))

    @output
    @render.ui
    async def scatterplot():
        fig = px.scatter(
                happiness_data,
                x="Ladder score",
                y="Explained by: Log GDP per capita",
                trendline="lowess")
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template = current_theme())
        return ui.HTML(fig.to_html(full_html=True))

    @output
    @render.ui
    async def linecountry():
        data = happiness_data.filter(pl.col("Country name") == input.ddCountry())
        data = data.sort(by='Year')
        
        fig = px.area(data, x = 'Year',y = 'Ladder score', color = "Country name")
        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            title= f"Area Graph Example {input.ddCountry()}",
            xaxis_title='Date',
            yaxis_title='Value',
            template=current_theme()
        )
        return ui.HTML(fig.to_html(full_html=True))

app = App(app_ui, server, static_assets={"/static": assets_folder})