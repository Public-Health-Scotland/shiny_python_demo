import pandas as pd
import plotly.express as px

from shiny import App, ui, render, reactive

# Load the dataset with the correct delimiter
file_path = 'data/WHR2024.csv'  # Ensure this is the correct path to your CSV file
happiness_data = pd.read_csv(file_path, delimiter=',')

app_ui = ui.page_navbar(
    # Top-level tabs
    ui.nav_panel("Your data", ui.h2("Welcome to the Home Page")),
    ui.nav_panel("Training", 
        ui.h2("About this App"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("World Happiness Analysis"),
                ui.input_select(
                    "year", "Select a Year:",
                    {str(year): str(year) for year in sorted(happiness_data['Year'].unique())}
                )
            ),
            ui.output_ui("happiness_map")
        )
    ),
    # Dropdown menu
    ui.nav_menu(
        "More",
        ui.nav_panel("Contact", ui.h2("Contact us")),
        ui.nav_panel("Help", ui.h2("Help Page"))
    ),
    ui.nav_spacer(), 
    ui.nav_control(ui.input_dark_mode())
    # Optional: place the navbar on the top, inverse style, etc.
    # position="static-top",
    # inverse=True
)

# Define the server logic
def server(input, output, session):
    @reactive.Calc
    def filtered_data():
        return happiness_data[happiness_data['Year'] == int(input.year())]


    @output
    @render.ui
    def happiness_map():
        data = filtered_data()
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
        fig.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0})
        fig_html = fig.to_html(full_html=False)
        return ui.HTML(fig_html)
    
    @output
    @render.ui
    def top10_bar():
        data = filtered_data().sort_values(by='Ladder score', ascending=True)
        fig = px.bar(
            data,
            x='Ladder score',
            y='Country name',
            orientation='h',
            title=f'Top 10 Happiest Countries in {input.year()}',
            labels={'Ladder score': 'Happiness Score', 'Country name': 'Country'},
            color_discrete_sequence=['#003366']
        )
        fig.update_layout(height=300, margin={"r":0,"t":40,"l":0,"b":0})
        return ui.HTML(fig.to_html(full_html=False))

app = App(app_ui, server=None)
