# shiny_python_demo
Shiny is available in Python (Ref [https://shiny.posit.co/py/](https://)) and you can find some examples there.

This project is using some specific packages versions. More detail in requirements.txt file.

This example focus on shiny core. There is another way to create controls (shiny.express).

This example uses the happiness data. Check WHR2024.csv in data folder

There are some Plotly examples like bar, area and cloropleth

Previous steps to prepare your VS Code for Python here: https://github.com/Public-Health-Scotland/vscode_prep

Don't forget to activate your environment to run this example
You only need to type on terminal shiny run app.py
![alt text](img/image.png)

## Comments
- Python shiny natively support async functions
- Python shiny has a ui.input_dark_mode (not in R shiny)
- Python shiny has a ui.card (You have to install BSLIB in R)
