import plotly.express as px
import plotly.io as pio
from shiny import App, render, reactive, ui
import faicons as fa
from pathlib import Path
from datetime import datetime
from data.data_con import DataLoader

assets_folder = Path(__file__).parent / 'static'

my_data_loader = DataLoader()
my_data_loader.load_data()

# Load the built-in template
colour_list = ["#3F3685", "#9B4393", "#0078D4", "#83BB26", "#948DA3", "#1E7F84", "#6B5C85", "#C73918",
                "#655E9D", "#9F9BC2", "#AF69A9", "#CDA1C9", "#3393DD", "#80BCEA", "#9CC951", "#C1DD93"]

pio.templates["plotly_dark"]["layout"].update({
    'colorway': colour_list
})
pio.templates["ggplot2"]["layout"].update({
    'colorway': colour_list
})

def my_dropdown_year(id):
    dict_years = my_data_loader.get_dict_years()
    return ui.input_select(id, "Select a Year:", dict_years)

app_ui = ui.page_fillable(
    ui.page_navbar(
        ui.nav_panel("Home", 
            ui.h3("General info"),
            ui.layout_column_wrap(
                ui.value_box(
                    "KPI number of records",
                    my_data_loader.get_shape(),
                    "source: dataset",
                    showcase = fa.icon_svg("database", width="50px", fill="#9B4393 !important")
                ),
                ui.value_box(
                    "KPI happiness scale",
                    my_data_loader.get_range_years(),
                    "source: dataset",
                    showcase=fa.icon_svg("calendar", width="50px", fill="#9B4393 !important")
                ),
                ui.value_box(
                    "KPI Title",
                    my_data_loader.get_range_ladder_score(),
                    "source: dataset",
                    showcase=fa.icon_svg("face-smile", width="50px", fill="#9B4393 !important")
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
                            ui.input_selectize("ddCountry", "country", my_data_loader.get_country_list() ))),
                        ui.output_ui("linecountry"),
                        full_screen=True),
                col_widths=[12]
            )
        ),
        ui.nav_panel("Bar plot", 
            ui.h3("Bar plot happiness"),
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h3("World Happiness top 10"),
                    my_dropdown_year("year")
                ),
                ui.output_ui("top10_bar")
            )
        ),
        ui.nav_panel("Geodata", 
            ui.h3("Cloropleth happiness"),
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
        # Inject Plotly JS globally
        ui.head_content(
            ui.tags.link(rel="icon", href="static/logo.png", type="image/x-icon"),
            ui.tags.script(src="https://cdn.plot.ly/plotly-3.1.0.min.js")
        ),
        title=ui.tags.a(
            ui.tags.img(src="static/logo.png", height="45px"), "",
            href="https://www.publichealthscotland.scot/",
            target="_blank",
            class_="navbar-brand d-flex align-items-center"
        ),
        lang="en",
        navbar_options=ui.navbar_options(position="fixed-top"),
        footer=ui.h6(
            f"Made by G FO © {datetime.now().year}",
            style="color: white !important; text-align: center; line-height: 1.6; margin-bottom: 3em; margin-top: 2em;"
        ),
        window_title="World happyness"
    )
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
        color_gridheader = '#4c4a4b' if input.dark_mode_switch() == 'dark' else 'white'
        css_gridheader = f" shiny-data-frame {{ --shiny-datagrid-grid-header-bgcolor: {color_gridheader} !important }}"
        
        if css_gridheader:
            style = ui.tags.style(css_gridheader, id='header_color')
            ui.insert_ui(style, selector='head')
    
    @output
    @render.data_frame
    def df_table():
        return render.DataGrid(my_data_loader.happiness_data, width="fit-content", height=430, filters=True)

    @output
    @render.ui
    async def top10_bar():
        data = await my_data_loader.get_top10_happiest_countries(int(input.year()))
        fig = px.bar(
            data,
            x='Ladder score',
            y='Country name',
            orientation='h',
            title=f'Top 10 Happiest Countries in {input.year()}',
            labels={'Ladder score': 'Happiness Score', 'Country name': 'Country'}, 
            template = current_theme()
        )
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @output
    @render.ui
    async def happiness_map():
        data = await my_data_loader.get_data_by_year(int(input.mapyear()))
        fig = px.choropleth(
            data,
            locations='Country name',  # Use country names for locations
            locationmode='country names',  # Specify that we're using country names
            color='Ladder score',  # Use 'Life Ladder' for happiness values
            hover_name='Country name',  # Use 'Country name' for the hover information
            color_discrete_sequence=px.colors.sequential.YlGnBu,
            labels={'Ladder score': 'Life Ladder Score'},
            title=f'World Happiness in {input.year()}', 
            template = current_theme()
        )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @output
    @render.ui
    async def scatterplot():
        fig = px.scatter(
                my_data_loader.happiness_data,
                x="Ladder score",
                y="Explained by: Log GDP per capita",
                trendline="lowess", 
                template = current_theme()
        )
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @output
    @render.ui
    async def linecountry():
        data = await my_data_loader.get_data_by_country(input.ddCountry())
        
        fig = px.area(data, x = 'Year', y = 'Ladder score', color = "Country name", template=current_theme())
        fig.update_layout(
            margin=dict(t=40, b=0, l=0, r=0),
            title= f"Area Graph Example {input.ddCountry()}",
            xaxis_title='Date',
            yaxis_title='Value'
        )
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

app = App(app_ui, server, static_assets={"/static": assets_folder})