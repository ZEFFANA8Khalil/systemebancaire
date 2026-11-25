"""Render executed notebook cells as Colab / Jupyter-looking screenshots (PNG)."""
import sys, html, os, nbformat
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Number, Operator, Text
from playwright.sync_api import sync_playwright

class ColabStyle(Style):
    background_color = "#f7f7f7"
    styles = {Keyword: "#af00db", Keyword.Constant: "#0000ff", Name.Builtin: "#795e26",
              Name.Function: "#795e26", Name.Namespace: "#000000", Comment: "#008000",
              String: "#a31515", Number: "#098658", Operator: "#000000",
              Keyword.Namespace: "#af00db"}

name = sys.argv[1]
theme = {"khalil": "colab", "younes": "jupyter"}[name]
nb = nbformat.read(f"TP3_{name}.ipynb", as_version=4)
outdir = f"shots_{name}"; os.makedirs(outdir, exist_ok=True)

fmt = HtmlFormatter(style=ColabStyle if theme == "colab" else "default", nowrap=True)
css_hl = fmt.get_style_defs(".hl")

def out_html(cell, n):
    parts = []
    for o in cell.outputs:
        if o.output_type == "stream":
            cls = "err" if o.name == "stderr" else ""
            parts.append(f'<pre class="txt {cls}">{html.escape(o.text.rstrip())}</pre>')
        elif "data" in o:
            d = o.data
            if "image/png" in d:
                parts.append(f'<img class="fig" src="data:image/png;base64,{d["image/png"]}">')
            elif "text/html" in d:
                parts.append(f'<div class="df">{d["text/html"]}</div>')
            else:
                parts.append(f'<pre class="txt">{html.escape(d["text/plain"])}</pre>')
            if o.output_type == "execute_result" and theme == "jupyter":
                parts[-1] = f'<div class="orow"><div class="oprompt">Out[{n}]:</div><div class="obody">{parts[-1]}</div></div>'
    return "\n".join(parts)

blocks = []
for i, c in enumerate(nb.cells, 1):
    tag = c.metadata["tag"]
    code = highlight(c.source, PythonLexer(), fmt)
    outs = out_html(c, i)
    if theme == "colab":
        blocks.append(f'''<div class="cell" id="c-{tag}">
  <div class="inrow"><div class="gutter"><span class="run">[{i}]</span></div>
    <div class="code"><pre class="hl">{code}</pre></div></div>
  {f'<div class="outrow"><div class="ogut"></div><div class="out">{outs}</div></div>' if outs else ''}
</div>''')
    else:
        blocks.append(f'''<div class="cell" id="c-{tag}">
  <div class="inrow"><div class="iprompt">In&nbsp;[{i}]:</div>
    <div class="code"><pre class="hl">{code}</pre></div></div>
  {f'<div class="outrow"><div class="out">{outs}</div></div>' if outs else ''}
</div>''')

if theme == "colab":
    css = """
body{margin:0;background:#fff;font-family:Roboto,'Liberation Sans',Arial,sans-serif;}
.wrap{width:820px;padding:6px 10px;background:#fff}
.cell{margin:6px 0 10px 0;}
.inrow{display:flex;}
.gutter{width:46px;flex:none;display:flex;justify-content:center;padding-top:6px}
.run{font:12px 'DejaVu Sans Mono',monospace;color:#9aa0a6}
.code{flex:1;background:#f7f7f7;border:1px solid #f0f0f0;border-radius:2px}
pre.hl{margin:0;padding:7px 10px;font:12.4px/1.45 'DejaVu Sans Mono',monospace;color:#000;white-space:pre}
.outrow{display:flex;margin-top:4px}
.ogut{width:46px;flex:none}
.out{flex:1;padding:2px 4px}
pre.txt{margin:2px 0;font:12.2px/1.4 'DejaVu Sans Mono',monospace;color:#212121;white-space:pre}
img.fig{width:470px;display:block;margin:4px 0}
.df table{border-collapse:collapse;font:12px Roboto,'Liberation Sans',Arial;border:none}
.df th,.df td{padding:5px 9px;text-align:right;border:none}
.df thead th{border-bottom:1px solid #ccc;font-weight:bold}
.df tbody tr:nth-child(odd){background:#f5f5f5}
.df tbody th{font-weight:bold}
"""
    topbar = """<div class="bar"><span class="logo"><b style="color:#f9ab00">C</b><b style="color:#e8710a">O</b></span>
<span class="fname">TP3_Regression_Multiple.ipynb</span><span class="star">☆</span>
<div class="menu">Fichier&nbsp;&nbsp; Modifier&nbsp;&nbsp; Affichage&nbsp;&nbsp; Insérer&nbsp;&nbsp; Exécution&nbsp;&nbsp; Outils&nbsp;&nbsp; Aide</div>
<div class="tb">+ Code &nbsp;&nbsp; + Texte <span class="ram">✓ RAM ▬ Disque ▬</span></div></div>"""
    css += """.bar{width:840px;font-family:'Liberation Sans',Arial;border-bottom:1px solid #ddd;padding:8px 0 4px 12px;position:relative;height:50px;background:#fff}
.logo{font-size:26px;letter-spacing:-3px;position:absolute;left:14px;top:12px}
.fname{position:absolute;left:62px;top:8px;font-size:17px;color:#202124}.star{position:absolute;left:330px;top:9px;color:#5f6368}
.menu{position:absolute;left:62px;top:33px;font-size:13px;color:#3c4043}
.tb{position:absolute;left:14px;top:58px;font-size:12.5px;color:#3c4043;display:none}
.ram{position:absolute;left:640px;color:#188038}"""
else:
    css_hl += "\n.hl .k,.hl .kn,.hl .ow{color:#008000;font-weight:bold}"
    css = """
body{margin:0;background:#fff;font-family:'Liberation Sans',Helvetica,Arial,sans-serif}
.wrap{width:860px;padding:6px 10px;background:#fff}
.cell{margin:4px 0 12px 0;padding:4px}
.inrow{display:flex}
.iprompt{width:84px;flex:none;color:#303f9f;font:12.5px 'DejaVu Sans Mono',monospace;text-align:right;padding:6px 8px 0 0}
.code{flex:1;background:#f7f7f7;border:1px solid #cfcfcf;border-radius:2px}
pre.hl{margin:0;padding:6px 8px;font:12.5px/1.35 'DejaVu Sans Mono',monospace;white-space:pre}
.outrow{margin-top:4px;padding-left:92px}
.orow{display:flex;margin-left:-92px}
.oprompt{width:84px;flex:none;color:#d84315;font:12.5px 'DejaVu Sans Mono',monospace;text-align:right;padding:4px 8px 0 0}
.obody{flex:1}
pre.txt{margin:2px 0;font:12.3px/1.35 'DejaVu Sans Mono',monospace;color:#000;white-space:pre}
pre.err{background:#fdd}
img.fig{width:480px;display:block;margin:2px 0}
.df table{border-collapse:collapse;font:12px 'Liberation Sans',Arial;border:none;margin:2px 0}
.df th,.df td{padding:4px 9px;text-align:right;border:none}
.df thead th{border-bottom:1px solid #000;font-weight:bold;vertical-align:bottom}
.df tbody tr:nth-child(odd){background:#f5f5f5}
.df tbody th{font-weight:bold}
"""
    topbar = """<div class="bar"><span class="jlogo">jupyter</span> <span class="fname">TP3_Regression_Multiple</span>
<span class="saved">Dernière sauvegarde : il y a quelques secondes</span>
<div class="menu">File &nbsp; Edit &nbsp; View &nbsp; Insert &nbsp; Cell &nbsp; Kernel &nbsp; Widgets &nbsp; Help <span class="kern">Python 3 (ipykernel) ○</span></div></div>"""
    css += """.bar{width:880px;font-family:'Liberation Sans',Arial;border-bottom:1px solid #e7e7e7;padding:8px 0 6px 14px;background:#fff}
.jlogo{font-size:22px;color:#f37626;font-family:'Liberation Sans';letter-spacing:.5px}.fname{font-size:19px;margin-left:12px;color:#333}
.saved{font-size:12px;color:#777;margin-left:10px}.menu{font-size:13px;color:#333;margin-top:8px;padding:5px 0;border-top:1px solid #eee}
.kern{float:right;margin-right:20px;color:#555}"""

page = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}{css_hl}</style></head>
<body>{topbar}<div class="wrap">{''.join(blocks)}</div></body></html>"""
open(f"{outdir}/notebook.html", "w").write(page)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    pg = b.new_page(device_scale_factor=2, viewport={"width": 900, "height": 900})
    pg.goto("file://" + os.path.abspath(f"{outdir}/notebook.html"))
    pg.locator(".bar").screenshot(path=f"{outdir}/bar.png")
    for c in nb.cells:
        tag = c.metadata["tag"]
        pg.locator(f"#c-{tag}").screenshot(path=f"{outdir}/{tag}.png")
    pg.locator("#c-Q9 img.fig").screenshot(path=f"{outdir}/fig9.png")
    pg.locator("#c-Q12 img.fig").screenshot(path=f"{outdir}/fig12.png")
    b.close()
print("ok", len(nb.cells))
