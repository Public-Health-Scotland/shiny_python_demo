from shiny import App, ui

app_ui = ui.page_navbar(
    ui.nav_panel("Bar", ui.h2("Bar plot")),
    ui.nav_panel("Map", ui.h2("Cloropleth")),
    ui.nav_spacer(), 
    ui.nav_control(ui.input_dark_mode(id="dark_mode_switch")),
    title=ui.tags.a(ui.tags.img(src="logo.png", height="30px"), "", href="#")
)

app = App(app_ui, server=None)
if __name__ == '__main__':
    app.run()