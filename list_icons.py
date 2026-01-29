# This scripts list all icons included in faicons Python package
from faicons import metadata

icons = metadata()

print(f"total number of icons {len(icons)}")
# all icon names
with open("list_faicons_icons.txt", "w", encoding="utf-8") as f:
    for name in icons.keys():
        f.write(f"{name}\n")
