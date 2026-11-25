import sys, nbformat, json
from nbclient import NotebookClient
from cells import KHALIL, YOUNES
name = sys.argv[1]
cells = {"khalil": KHALIL, "younes": YOUNES}[name]
nb = nbformat.v4.new_notebook()
nb.cells = [nbformat.v4.new_code_cell(c, metadata={"tag": t}) for t, c in cells]
NotebookClient(nb, timeout=600, kernel_name="python3").execute()
nbformat.write(nb, f"TP3_{name}.ipynb")
for c in nb.cells:
    print("=====", c.metadata["tag"])
    for o in c.outputs:
        if o.output_type == "stream": print(o.text)
        elif "data" in o:
            print(o.data.get("text/plain", ""), "[img]" if "image/png" in o.data else "")
        elif o.output_type == "error": print("ERR", o.ename, o.evalue)
