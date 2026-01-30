from shiny import App, render, reactive, ui
import faicons as fa
import getpass
from pathlib import Path
from data.data_con import DataLoader
from view.myplots import PlotBuilder

assets_folder = Path(__file__).parent / 'static'

my_data = DataLoader()
my_data.load_data()

def my_dropdown_year(id):
    return ui.input_select(id, "Select a Year:", my_data.dict_years)

app_ui = ui.page_navbar(
    ui.nav_panel(
        # Name and icon
        ui.TagList(fa.icon_svg("house"), "Home"),

        ui.layout_column_wrap(
            ui.output_ui("kpi_records"),
            ui.output_ui("kpi_scale"),
            ui.output_ui("kpi_other")
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
                        ui.input_selectize("ddCountry", "country", my_data.country_list ))),
                    ui.output_ui("linecountry"),
                    full_screen=True),
            col_widths=[12]
        )
    ),
    ui.nav_panel(
        # Name and icon
        ui.TagList(fa.icon_svg("chart-line"), "Bar plot"),

        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("World Happiness top 10"),
                my_dropdown_year("year")
            ),
            ui.output_ui("top10_bar")
        )
    ),
    ui.nav_panel(
        # Name and icon
        ui.TagList(fa.icon_svg("map"), "Geodata"),

        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("Map plot"),
                my_dropdown_year("mapyear")
            ),
            ui.output_ui("happiness_map")
        )
    ),
    ui.nav_menu(
        # Name and icon
        ui.TagList(fa.icon_svg("plus"), "More data"),

        ui.nav_panel(
            # Name and icon
            ui.TagList(fa.icon_svg("database"), "Database"),
            ui.h2("Information from db")
        ),
        ui.nav_panel(
            # Name and icon
            ui.TagList(fa.icon_svg("codepen"), "Contact"),
            ui.h2("Contact us")
        ),
        ui.nav_panel(
            # Name and icon
            ui.TagList(fa.icon_svg("people-carry-box"), "Help"),
            ui.h2("Help Page")
        )
    ),
    ui.nav_spacer(),
    ui.nav_control(
        ui.div(
            fa.icon_svg("person-circle-check"),
            ui.span(ui.output_text("welcome"), style="margin-left: 6px;"),
            style="display: flex; align-items: center; padding-right: 15px;"
        )
    ),
    # ui.nav_control(ui.output_text("welcome")), 
    ui.nav_control(ui.input_dark_mode(id="dark_mode_switch")),
    # Inject Plotly JS globally
    ui.head_content(
        ui.tags.link(rel="icon", href="static/logo.png", type="image/x-icon"),
        ui.tags.script(src="https://cdn.plot.ly/plotly-3.3.1.min.js"),
        ui.tags.style("body { padding-top: 70px; }")
    ),
    title=ui.tags.a(
        ui.tags.img(src="static/logo.png", alt="PHS logo", height="45px"), "",
        href="https://www.publichealthscotland.scot/",
        target="_blank",
        class_="navbar-brand d-flex align-items-center"
    ),
    lang="en",
    navbar_options=ui.navbar_options(position="fixed-top"),
    footer=ui.tags.footer(
        ui.tags.span("© Developed by Data science team - "),
        ui.tags.script("document.write(new Date().getFullYear());"),
        class_="text-center p-2",
        role="contentinfo"
    ),
    window_title="World happyness"
)

def server(input, output, session):
    myplots = PlotBuilder()

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
    @render.text
    async def welcome():
        # get current user
        user_name = session.user
        if user_name is None:
            user_name = getpass.getuser()
        return f"Welcome {user_name}"
    
    async def kpi_value_box(title: str, icon_name: str, message: str, current: float, historical: float):
        # get colour for your icon and current value
        my_kpi_color = "#9B4393"
        # build your icon with the color
        icon = fa.icon_svg(icon_name, width="50px", fill=f"{my_kpi_color} !important")
        
        value_block = ui.div(
            *filter(None, [ui.strong(f"{historical}") if historical is not None else None]),
            ui.span(
                f"/ {current}",
                style=f"margin-left:8px;color:{my_kpi_color};font-weight:600;"
            ),
            ui.br(),
            ui.span(
                f"{message}",
                style="font-size:0.40em;font-weight:100;"
            )
        )

        return ui.value_box(title=title, value=value_block, showcase=icon)

    @output
    @render.ui
    async def kpi_records():
        return await kpi_value_box("KPI number of records", "database", 
                                    "(Columns - Rows)", my_data.happiness_data.shape[0], my_data.happiness_data.shape[1])

    @output
    @render.ui
    async def kpi_scale():
        return await kpi_value_box("KPI happiness scale", "calendar", 
                                    "Year (Min - Max)", my_data.happiness_data.Year.max(), my_data.happiness_data.Year.min())

    @output
    @render.ui
    async def kpi_other():
        return await kpi_value_box("KPI Title", "face-smile", 
                                    "Score (Min - max)", round(my_data.happiness_data['Ladder score'].max(), 2), round(my_data.happiness_data['Ladder score'].min(), 2))
    
    @output
    @render.data_frame
    def df_table():
        return render.DataGrid(my_data.happiness_data, width="fit-content", height=430, filters=True)

    @output
    @render.ui
    async def top10_bar():
        year = int(input.year())
        data = await my_data.get_top10_happiest_countries(year)
        plot, descript = await myplots.build_top10_bar(data, current_theme(), year)
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def happiness_map():
        year = int(input.mapyear())
        data = await my_data.get_data_by_year(year)
        plot, descript = await myplots.build_happiness_map(data, current_theme(), year)
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def scatterplot():
        data = await my_data.get_clean_data_for_scatter()
        plot, descript = await myplots.build_scatterplot(data, current_theme())
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def linecountry():
        selected_country = input.ddCountry()
        data = await my_data.get_data_by_country(selected_country)
        plot, descript = await myplots.build_linecountry(data, current_theme(), selected_country)
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

app = App(app_ui, server, static_assets={"/static": assets_folder})