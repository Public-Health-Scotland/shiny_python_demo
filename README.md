# shiny_python_demo
Shiny is available in Python (Ref [https://shiny.posit.co/py/](https://)) and you can find some examples there.

This project is using some specific packages versions. More detail in requirements.txt file.

This example focus on shiny core. There is another way to create controls (shiny.express).

This example uses the happiness data. Check WHR2024.csv in data folder

There are some Plotly examples like bar, area and cloropleth

Previous steps to prepare your VS Code for Python here: https://github.com/Public-Health-Scotland/vscode_prep

Don't forget to activate your environment to run this example
You only need to type on terminal: shiny run app.py
![alt text](img/image.png)

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
