import json
import io

with io.open("Group_01.ipynb", "r", encoding="utf-8") as f:
    d = json.load(f)

with io.open("extract.py", "w", encoding="utf-8") as out:
    for cell in d["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell.get("source", []))
            out.write(source + "\n\n")
