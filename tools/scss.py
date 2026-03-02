import sass

def compile_scss_file(input_path: str, output_path: str):
    css = sass.compile(filename=input_path)
    with open(output_path, "w") as f:
        f.write(css)

compile_scss_file("tools/_navbar.scss", "tools/_navbar.css")

