from shiny import App, render, reactive, ui
import faicons as fa
import getpass
from pathlib import Path
from data.data_con import DataLoader
from view.myplots import PlotBuilder

assets_folder = Path(__file__).parent / 'www'

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
            ui.card(ui.card_header("Top 3 happiness data distribution",
                    ui.popover(
                        ui.span(
                            fa.icon_svg("ellipsis"),
                            style="position:absolute; top: 5px; right: 7px;",),
                        "Year",
                        ui.input_selectize("ddpieyear", "Choose", choices=[] ))
                    ),
                    ui.output_ui("pietop3"),
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
                        ui.input_selectize("ddCountry", "country", choices=[] ))),
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
                ui.input_selectize("byear", "Choose", choices=[])
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
                ui.input_selectize("mapyear", "Choose", choices=[])
            ),
            ui.output_ui("happiness_map")
        )
    ),
    ui.nav_spacer(),
    ui.nav_menu(
        # Name and icon
        ui.TagList(fa.icon_svg("arrow-up-right-dots"), "More"),
        ui.nav_control(
            ui.div(
                fa.icon_svg("person-circle-check"),
                ui.span(ui.output_text("welcome"), id="welcome_text"),
                id="welcome_div"
            )
        ),
        # ui.nav_control(ui.output_text("welcome")), 
        ui.nav_control(ui.input_dark_mode(id="dark_mode_switch")),
        ui.nav_panel(
            # Name and icon
            ui.TagList(fa.icon_svg("database"), "Database"),
            ui.layout_columns(
                ui.card(ui.card_header("happiness data"),
                        ui.output_data_frame("df_table"),
                        full_screen=True
                ),
                col_widths=[12]
            )
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
    # Inject Plotly JS globally
    ui.head_content(
        ui.tags.link(rel="icon", href="www/img/phs-logo.svg", type="image/x-icon"),
        # ui.tags.script(src="https://cdn.plot.ly/plotly-3.3.1.min.js"), # online version
        ui.tags.script(src="www/javascript/plotly-3.3.1.min.js"),
        ui.tags.script(src="www/javascript/functs.js"),
        ui.tags.link(rel="stylesheet", href="www/styles/phs.css"),
        ui.tags.link(rel="stylesheet", href="www/styles/_footer.css")
    ),
    title=ui.tags.a(
        ui.tags.img(id="app-logo", alt="PHS logo"), "",
        href="https://www.publichealthscotland.scot/",
        target="_blank",
        class_="navbar-brand d-flex align-items-center"
    ),
    lang="en",
    navbar_options=ui.navbar_options(position="fixed-top"),
    # footer=ui.tags.footer(id="app-footer"),
    footer=ui.tags.footer(
        ui.div(
            ui.span("Left content 1", class_="left"),
            ui.span("Right content 1", class_="right"),
            class_="footer-row",
        ),
        ui.div(
            ui.span("Left content 2", class_="left"),
            ui.span("Right content 2", class_="right"),
            class_="footer-row",
        ),
        ui.div(
            ui.span("Left content 3", class_="left"),
            ui.span(id="app-footer", class_="phs-footer-copyright"),
            class_="footer-row",
        ),
        class_="phs-footer",
        role="contentinfo"
    ),
    window_title="World happyness"
)

def server(input, output, session):
    my_data = DataLoader()
    myplots = PlotBuilder()

    df_val = reactive.Value(None)

    @output
    @render.text
    async def welcome():
        # get current user
        user_name = session.user
        if user_name is None:
            user_name = getpass.getuser()
        return f"Welcome {user_name}"

    # Load data ONCE at session start
    @reactive.effect
    async def _load_data():
        df = await my_data.load_data()
        df_val.set(df)
        
        # Now the country list is ready!
        ui.update_selectize("byear", choices=my_data.dict_years)
        ui.update_selectize("mapyear", choices=my_data.dict_years)
        ui.update_selectize("ddpieyear", choices=my_data.dict_years)
        ui.update_selectize("ddCountry", choices=my_data.country_list)


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
    
    async def kpi_value_box(title: str, icon_name: str, message: str, current: float, historical: float):
        # get colour for your icon and current value
        my_kpi_color = "#9B4393"
        return ui.value_box(
            title=title,
            value = ui.div(
                ui.div(
                    *filter(None, [ui.strong(f"{historical}") if historical is not None else None]),
                    ui.span(
                        f"/{current}", class_ = "span_current",
                        style=f"color:{my_kpi_color};"
                    ),
                    # ui.span(f"{mydata.last_date}", class_ = "span_week")
                ),
                ui.div("(Historical / Current)", class_ = "div_hist_curr")
            ),
            showcase=fa.icon_svg(icon_name, fill=f"{my_kpi_color} !important")
        )

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
        year = int(input.byear())
        data = await my_data.get_top10_happiest_countries(year, 10)
        plot, descript = await myplots.build_top10_bar(data, current_theme(), year)
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def happiness_map():
        if input.mapyear() != '':
            year = int(input.mapyear())
            data = await my_data.get_data_by_year(year)
            plot, descript = await myplots.build_happiness_map(data, current_theme(), year)
            return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def pietop3():
        if input.ddpieyear() != '':
            year = int(input.ddpieyear())
            data = await my_data.get_top10_happiest_countries(year=year, top=3)
            plot, descript = await myplots.build_pietop3(data, current_theme(), year, 3)
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
        if input.ddCountry() != '':
            selected_country = input.ddCountry()
            data = await my_data.get_data_by_country(selected_country)
            plot, descript = await myplots.build_linecountry(data, current_theme(), selected_country)
            return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

app = App(app_ui, server, static_assets={"/www": assets_folder})