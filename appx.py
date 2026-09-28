from shiny import App, Inputs, Outputs, Session, render, reactive, ui

# 1. Define the Login UI
login_ui = ui.page_fluid(
    ui.panel_well(
        ui.h2("App Login", class_="text-center mb-4"),
        ui.input_text("username", "Username", placeholder="admin"),
        ui.input_password("password", "Password", placeholder="password"),
        ui.input_action_button("login_btn", "Log In", class_="btn-primary w-100"),
        ui.output_text("login_error"),
        style="max-width: 400px; margin: 100px auto;",
    )
)

# 2. Define the Main Application UI (accepts username parameter)
def main_app_ui(username: str):
    return ui.page_navbar(
        ui.nav_panel(
            "Dashboard",
            ui.h3(f"Welcome back, {username}!"),
            ui.p("This content is personalized for your session."),
        ),
        ui.nav_panel(
            "Analytics",
            ui.h3("Analytics Page"),
            ui.p(f"Viewing analytics data as user: {username}"),
        ),
        ui.nav_panel(
            "Account",
            ui.h3("Account Details"),
            ui.p(f"Logged in as: {username}"),
            ui.input_action_button("logout_btn", "Log Out", class_="btn-danger"),
        ),
        title=f"Dashboard ({username})",
        id="main_navbar",
    )

# 3. Outer Shell Layout
app_ui = ui.page_fluid(
    ui.output_ui("dynamic_body")
)

def server(input: Inputs, output: Outputs, session: Session):
    # Reactive values to track authentication status and the logged-in user
    is_logged_in = reactive.value(False)
    logged_user = reactive.value("")
    error_msg = reactive.value("")

    # Handle Login Logic
    @reactive.effect
    @reactive.event(input.login_btn)
    def _():
        entered_user = input.username()
        entered_pass = input.password()
        
        # Replace with your actual authentication check
        if entered_user and entered_pass == "password":
            logged_user.set(entered_user)
            is_logged_in.set(True)
            error_msg.set("")
        else:
            error_msg.set("Invalid username or password.")

    # Handle Logout Logic
    @reactive.effect
    @reactive.event(input.logout_btn)
    def _():
        is_logged_in.set(False)
        logged_user.set("")

    # Render error messages on the login form
    @render.text
    def login_error():
        return error_msg()

    # Dynamically render either Login or Main App based on login status
    @render.ui
    def dynamic_body():
        if is_logged_in():
            return main_app_ui(logged_user())
        return login_ui


app = App(app_ui, server)