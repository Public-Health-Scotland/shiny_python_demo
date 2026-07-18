from shiny import App, render, reactive, ui
import faicons as fa
import getpass
from pathlib import Path
from data.data_con import DataLoader
from view.myplots import PlotBuilder
from helper.functs import phs_config_get, get_social_urls, get_phs_url, get_ogl_url, get_compliance_list, get_my_www_folder

# important settings
assets_folder = Path(__file__).parent / 'www'
cfg = phs_config_get(assets_folder / "config" / "default-config.json")

# Define the UI
app_ui = ui.page_navbar(
    ui.nav_panel(
        # Name and icon
        ui.TagList(fa.icon_svg("house"), "Home"),
        
        ui.layout_column_wrap(
            ui.output_ui("kpi_records"),
            ui.output_ui("kpi_scale"),
            ui.output_ui("kpi_other"),
            class_="phs-kpi-row"
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
                    ui.output_ui("pietop3", class_="phs-plot-container"),
                    full_screen=True
            ),
            ui.card(ui.card_header("Scatter plot"), 
                    ui.output_ui("scatterplot", class_="phs-plot-container"), 
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
                    ui.output_ui("linecountry", class_="phs-plot-container"),
                    full_screen=True),
            col_widths=[12]
        ),
        value="home"
    ),
    ui.nav_panel(
        # Name and icon
        ui.TagList(fa.icon_svg("chart-line"), "Bar plot"),

        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("World Happiness top 10"),
                ui.input_selectize("byear", "Choose", choices=[])
            ),
            ui.output_ui("top10_bar", class_="phs-plot-container")
        ),
        value="bar_plots"
    ),
    ui.nav_panel(
        # Name and icon
        ui.TagList(fa.icon_svg("map"), "Geodata"),

        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("Map plot"),
                ui.input_selectize("mapyear", "Choose", choices=[])
            ),
            ui.output_ui("happiness_map", class_="phs-plot-container")
        ),
        value="geodata"
    ),
    ui.nav_spacer(),
    ui.nav_menu(
        # Name and icon
        ui.TagList(fa.icon_svg("ellipsis"), "More"),
        ui.nav_control(
            ui.div(
                ui.span("User:"),
                ui.div(
                    fa.icon_svg("person-circle-check"),
                    ui.output_text("welcome", inline=True)
                )
            )
        ),
        ui.nav_control(
            ui.div(
                ui.span("theme:"),
                ui.div(
                    ui.input_dark_mode(id="theme_mode"),
                    ui.span(id="theme-label")
                )
            )
        ),
        ui.nav_panel(
            # Name and icon
            ui.TagList(fa.icon_svg("database"), "Database"),
            ui.layout_columns(
                ui.card(ui.card_header("happiness data"),
                        ui.output_data_frame("df_table"),
                        full_screen=True
                ),
                col_widths=[12]
            ),
            value="database"
        ),
        ui.nav_panel(
            # Name and icon
            ui.TagList(fa.icon_svg("codepen"), "Contact"),
            ui.h2("Contact us"),
            value="contact"
        ),
        ui.nav_panel(
            # Name and icon
            ui.TagList(fa.icon_svg("people-carry-box"), "Help"),
            ui.h2("Help Page"),
            value="help"
        )
    ),
    # Inject Plotly JS globally
    ui.head_content(
        ui.tags.link(rel="icon", href="www/img/phs-logo.svg", type="image/x-icon"),
        # ui.tags.script(src="https://cdn.plot.ly/plotly-3.6.0.min.js"), # online version
        ui.tags.script(src="www/js/plotly-3.6.0.min.js"),
        ui.tags.script(src="www/js/phs-footer.js"),
        ui.tags.script(src="www/js/phs-router.js"),
        ui.tags.script(src="www/js/phs-thene-mode.js"),
        ui.tags.script(src="www/js/_navbar.js"),
        ui.tags.link(rel="stylesheet", href="www/styles/phs.css"),
        ui.tags.link(rel="stylesheet", href="www/styles/_navbar.css"),
        ui.tags.link(rel="stylesheet", href="www/styles/_footer.css"),
        ui.tags.link(rel="stylesheet", href="www/styles/_value_box.css"),
        ui.tags.link(rel="stylesheet", href="www/styles/_datagrid.css"),
        ui.tags.link(rel="stylesheet", href="www/styles/_spinner.css")
    ),
    title=ui.tags.a(
        ui.tags.img(class_ = "phs-navbar-logo", alt="PHS logo"), "",
        href = get_phs_url(cfg),
        target = "_blank",
        class_="navbar-brand"
    ),
    lang="en",
    navbar_options=ui.navbar_options(position="fixed-top"),
    footer=ui.tags.footer(
        ui.div(
            ui.div(
                ui.div("Shiny Python demo", class_ = "phs-footer-row1-left"),
                ui.div(
                    *[
                        ui.tags.a(section.get('name_en'), href="#")
                        for name, section in get_compliance_list(cfg).items() if section.get('enabled') is True and section.get('name_en') is not None
                    ], class_="phs-footer-row1-right"),
                class_="phs-footer-row phs-footer-row1",
            ),
            ui.div(
                ui.span(
                    ui.tags.a(
                        "publichealthscotland.scot",
                        href = get_phs_url(cfg),
                        target = "_blank",
                        rel = "noopener noreferrer",
                        class_="phs-footer-phs-link"
                    ), class_="left"),
                ui.span(
                    *[
                        ui.tags.a(fa.icon_svg(name), href=url, target="_blank", class_ = "phs-footer-social-icon")
                        for name, url in get_social_urls(cfg).items()
                    ], class_="phs-footer-row2-right"),
                class_="phs-footer-row phs-footer-row2",
            ),
            ui.div(
                ui.div(
                    ui.tags.img(class_="ogl-logo", alt="Open Government Licence logo"),
                    ui.span("All content is available under the ", 
                            ui.tags.a("Open Government Licence",
                                        href = get_ogl_url(cfg),
                                        target = "_blank",
                                        rel = "noopener noreferrer",
                                        class_ = "phs-footer-ogl-link"),
                            ", except where otherwise stated",
                            class_="phs-footer-ogl-text"),
                    class_ = "phs-footer-row3-left"
                ),
                ui.div(
                    ui.span(id="app-footer", class_="phs-footer-copyright"),
                    class_ = "phs-footer-row3-right",
                ),
                class_="phs-footer-row phs-footer-row3",
            ), class_ = "phs-footer-inner"
        ),
        class_="phs-footer",
        role="contentinfo"
    ),
    id="selected_tab",
    window_title="World Happiness"
)

def server(input, output, session):
    my_data = DataLoader()
    myplots = PlotBuilder()

    df_val = reactive.Value(None)
    kpi_cache = reactive.Value(None)  # cache KPI stats after load

    @reactive.effect
    @reactive.event(input.selected_tab)
    async def _():
        # Add tab value to the URL
        tab = input.selected_tab()
        await session.send_custom_message("update_hash", tab)

    @output
    @render.text
    async def welcome():
        # get current user
        user_name = session.user
        if user_name is None:
            user_name = getpass.getuser()
        return user_name

    # @reactive.effect
    # async def _expire_session():
    #     await asyncio.sleep(180)  # wait 1200s, then continue
    #     await session.close()

    # Load data ONCE at session start
    @reactive.effect
    async def _load_data():
        df = await my_data.load_data()
        df_val.set(df)
        
        # Cache KPI values once
        kpi_cache.set({
            "n_rows":   my_data.happiness_data.shape[0],
            "n_cols":   my_data.happiness_data.shape[1],
            "year_max": my_data.happiness_data["Year"].max(),
            "year_min": my_data.happiness_data["Year"].min(),
            "score_max": round(my_data.happiness_data["Ladder score"].max(), 2),
            "score_min": round(my_data.happiness_data["Ladder score"].min(), 2),
        })

        # Now the country list is ready!
        ui.update_selectize("byear", choices=my_data.dict_years)
        ui.update_selectize("mapyear", choices=my_data.dict_years)
        ui.update_selectize("ddpieyear", choices=my_data.dict_years)
        ui.update_selectize("ddCountry", choices=my_data.country_list)

    @reactive.Calc
    def current_theme():
        template = "plotly_dark" if input.theme_mode() == "dark" else "ggplot2"
        return template
    
    def kpi_value_box(title: str, icon_name: str, message: str, current: float, historical: float):
        # get colour for your icon and current value
        my_kpi_color = "#9B4393"
        return ui.value_box(
            title=title,
            value = ui.div(
                ui.div(
                    *filter(None, [ui.span(f"{historical}") if historical is not None else None]),
                    ui.span(
                        f"/{current}", class_ = "span_current",
                        style=f"color:{my_kpi_color};"
                    ),
                ),
                ui.div("(Historical / Current)", class_ = "div_hist_curr")
            ),
            showcase=fa.icon_svg(icon_name, fill=f"{my_kpi_color} !important"),
            class_="phs-kpi-box",
        )

    @output
    @render.ui
    def kpi_records():
        kpi = kpi_cache()
        if kpi is None:
            return
        return kpi_value_box("KPI number of records", "database", "(Columns - Rows)", kpi["n_rows"], kpi["n_cols"])

    @output
    @render.ui
    def kpi_scale():
        kpi = kpi_cache()
        if kpi is None:
            return
        return kpi_value_box("KPI happiness scale", "calendar", "Year (Min - Max)", kpi["year_max"], kpi["year_min"])

    @output
    @render.ui
    def kpi_other():
        kpi = kpi_cache()
        if kpi is None:
            return
        return kpi_value_box("KPI Title", "face-smile",
                                    "Score (Min - max)", kpi["score_max"], kpi["score_min"])
    
    @output
    @render.data_frame
    def df_table():
        return render.DataGrid(my_data.happiness_data, 
                                # width="fit-content", height=430, 
                                filters=True)

    @output
    @render.ui
    async def top10_bar():
        if not input.byear():  # guard against empty
            return
        year = int(input.byear())
        data = await my_data.get_top_happiest_countries(year, 10)
        plot, descript = myplots.build_top10_bar(data, current_theme(), year)
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def happiness_map():
        if not input.mapyear():
            return
        year = int(input.mapyear())
        data = await my_data.get_data_by_year(year)
        plot, descript = myplots.build_happiness_map(data, current_theme(), year)
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def pietop3():
        if not input.ddpieyear():
            return
        # 
        
        year = int(input.ddpieyear())
        data = await my_data.get_top_happiest_countries(year=year, top=3)
        plot, descript = myplots.build_pietop3(data, current_theme(), year, 3)
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def scatterplot():
        if my_data.happiness_data is None:  # guard until data loaded
            return
        data = await my_data.get_clean_data_for_scatter()
        plot, descript = myplots.build_scatterplot(data, current_theme())
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

    @output
    @render.ui
    async def linecountry():
        if not input.ddCountry():
            return
        selected_country = input.ddCountry()
        data = await my_data.get_data_by_country(selected_country)
        plot, descript = myplots.build_linecountry(data, current_theme(), selected_country)
        return ui.tags.div(ui.HTML(plot), aria_label=descript, role="img")

app = App(app_ui, server, static_assets={"/www": get_my_www_folder()})
