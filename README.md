# shiny_python_demo
Shiny is available in Python (Ref [https://shiny.posit.co/py/](https://)) and you can find some examples there.

This project is using some specific packages versions. More detail in requirements.txt file.

This example focusses on shiny core. There is another way to create controls (shiny.express) but it is not part of this example.

This example uses the happiness data. Check WHR2024.csv in data folder

There are some Plotly chart examples like bar, area and cloropleth

## Run in VS Code or Positron
- Previous steps to prepare your VS Code/Positron for Python here: https://github.com/Public-Health-Scotland/vscode_prep
- Clone this repo
- Create your Python virtual environment. I recommend UV since it is a modern Python package manager, more details here https://github.com/Public-Health-Scotland/vscode_prep/tree/main/Python
- Don't forget to activate your environment to run this example
- Don't forget to install the required packages using requirements.txt file
- This example requires an extra step to work with an encrypted DuckDB file. You have to create a .env file (dot included). Add this value in your .env file:
```
DUCKDB_KEY=type_a_strong_password_here_no_need_to_add_quotations_marks
```
- Next step will be creating the DuckDB file. You have to run this command in terminal: `python tools/csv_to_encrypted_duckdb.py` 
- You will see a file called encrypted_data.duckdb inside data folder
- Now, you will be able to run this project, you only need to run this command in terminal: `shiny run app.py`

Advanced way to run: You can run this Shiny app and make it visible in your local network but it may be blocked for some VPN/proxy setting: `shiny run --host 0.0.0.0 --port 8000 app.py`. You will need to know local IP address. You can find it typing `ipconfig` in a Windows terminal. Then you can access your app from another device using this link in a browser: `http://192.168.X.X:8000/`

## Deployment

If you want to publish to shinyapps.io/internal Posit connect or Posit connect cloud you need to install rsconnect-python or use Positron Posit Publisher extension (More details here https://github.com/Public-Health-Scotland/vscode_prep/tree/main/Deployment). You will need to run the following commands:

- Register your credentials

`rsconnect add --account <your-account-name> --name <your-account-name> --token <your-token> --secret <your-secret>`

- Deploy your app. If you are in the current app folder use ".", otherwise you should type the app_path

`rsconnect deploy shiny -n <your-accout-name> --title "My Shiny Python" .`

## Comment
- Python shiny natively support async functions
- Python shiny has a native ui.input_dark_mode (not in R shiny)
- Python shiny has a ui.card (You have to install BSLIB in R)

## Performance notes
If you want a faster Plotly render, there are some adjustments to consider:
- Set fig.to_html(full_html=False, include_plotlyjs=False), the full_html argument will avoid to create repeated html tags and include_plotlyjs won't load the plotly.js per chart.
- We will need to globally load plotly.js. The element ui.head_content will contain ui.tags.script where we add src=https://cdn.plot.ly/plotly-3.3.1.min.js or even better a local copy as a javascript file.
- This project has a client version to change theme for all the Plotly charts. Your Python code sends a json content which is managed by plotly-theme.js file.

## Resources

[PHS colours](https://public-health-scotland.github.io/phsstyles/index.html)

[External colour code palette](https://html-color.codes/)

[Python package faicons](https://github.com/posit-dev/py-faicons)

[Posit connect cloud example](https://019c6d8e-5068-bb52-18ee-505b14aa6a25.share.connect.posit.cloud/)
