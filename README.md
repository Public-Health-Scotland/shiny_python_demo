# shiny_python_demo
Shiny is available in Python (Ref [https://shiny.posit.co/py/](https://)) and you can find some examples there.

This project is using some specific packages versions. More detail in requirements.txt file.

This example focus on shiny core. There is another way to create controls (shiny.express).

This example uses the happiness data. Check WHR2024.csv in data folder

There are some Plotly examples like bar, area and cloropleth

Previous steps to prepare your VS Code for Python here: https://github.com/Public-Health-Scotland/vscode_prep

Don't forget to activate your environment to run this example
You only need to type in terminal: shiny run app.py

Note: You can run your Shiny app and make it visible in your local network: shiny run --host 0.0.0.0 --port 8000 app.py

You will beed to know your local IP address. You can find it typing ipconfig in a terminal. Then you can access your app from another device using this link: http://192.168.X.X:8000/

If you want to publish to shinyapps.io you need to install rsconnect-python in your environment
You will need to run the following commands:
- Register your credentials

`rsconnect add --account <your-account-name> --name <your-account-name> --token <your-token> --secret <your-secret>`

- Deploy your app. If you are in the current app folder use ".", otherwise you should type the app_path

`rsconnect deploy shiny -n <your-accout-name> --title "My Shiny Python" .`

## Comment
- Python shiny natively support async functions
- Python shiny has a ui.input_dark_mode (not in R shiny)
- Python shiny has a ui.card (You have to install BSLIB in R)

## Performance notes
If you want a faster Plotly render, there are some adjustments to consider:
- Set fig.to_html(full_html=False, include_plotlyjs=False), the full_html argument will avoid to create repeated html tags and include_plotlyjs won't load the plotly.js per chart.
- We will need to globally load plotly.js. The element ui.head_content will contains ui.tags.script where we add src=https://cdn.plot.ly/plotly-3.3.1.min.js or we can copy that file in static folder
- This project runs with Plotly 6.5.2 which means it works with plotly-3.3.1.min.js

## Resources

[PHS colours](https://public-health-scotland.github.io/phsstyles/index.html)

[External colour code palette](https://html-color.codes/)

[Python package faicons](https://github.com/posit-dev/py-faicons)

