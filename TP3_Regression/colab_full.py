"""Notebook Colab complet (code + réponses en cellules texte) -> .ipynb exécuté + PDF au look Colab."""
import os, html, nbformat, markdown
from nbclient import NotebookClient
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Number, Operator
from playwright.sync_api import sync_playwright
from cells import KHALIL

class ColabStyle(Style):
    background_color = "#f7f7f7"
    styles = {Keyword: "#af00db", Keyword.Constant: "#0000ff", Name.Builtin: "#795e26",
              Name.Function: "#795e26", Comment: "#008000", String: "#a31515",
              Number: "#098658", Operator: "#000000", Keyword.Namespace: "#af00db"}

C = dict(KHALIL)
M = []  # (kind, content)
def md(t): M.append(("md", t.strip()))
def code(tag): M.append(("code", C[tag]))

md("""# TP3 · Régression linéaire multiple
**Trinôme :** Khalil ZEFFANA – Younes KHALFI – Walid Abdellah KHEIRI

Objectif : estimer le prix d'une maison à partir de ses caractéristiques avec `LinearRegression` puis `SGDRegressor`, comparer les deux modèles et étudier le rôle de la standardisation et du taux d'apprentissage.""")
code("imports")
md("## I. Chargement et préparation des données\n### Q1 · Charger et explorer les données")
for t in ["Q1a","Q1b","Q1c","Q1d"]: code(t)
md("""**Réponse :**
- Le jeu de données contient **200 maisons** (lignes) et **6 colonnes** : `prix`, `surface`, `nb_chambres`, `age`, `dist_centre`, `garage`.
- Toutes les colonnes sont numériques : `prix` et `dist_centre` en `float64`, les autres en `int64` (`garage` est une variable binaire 0/1).
- `describe()` montre un prix moyen d'environ **229,9 milliers** (écart-type 64), une surface moyenne de **105,8 m²** (de 40 à 182 m²), des maisons de 0 à 60 ans situées entre 0,6 et 24,8 km du centre ; 60 % des maisons ont un garage.
- Il n'y a **aucune valeur manquante** : aucun nettoyage n'est nécessaire.""")
md("### Q2 · Définir les variables explicatives et la cible")
code("Q2")
md("""**Réponse :** `X` a pour dimensions **(200, 5)** et `y` **(200,)**. Chaque ligne de `X` représente **une maison**, décrite par ses 5 caractéristiques (surface, nombre de chambres, âge, distance au centre, garage) ; la valeur correspondante de `y` est son prix.""")
md("### Q3 · Découper et standardiser")
code("Q3")
md("""**Réponse :** on obtient **160 maisons pour l'entraînement** et **40 pour le test**.

Intérêt de la standardisation : les variables ont des échelles très différentes (surface ≈ 100, garage = 0 ou 1). `StandardScaler` ramène chaque variable à une moyenne 0 et un écart-type 1, ce qui :
- rend la descente de gradient stable et rapide (un même pas `eta0` convient à toutes les variables) ;
- rend les coefficients comparables entre eux.

Le scaler est ajusté (`fit`) **uniquement sur l'entraînement**, puis appliqué au test avec `transform`, pour éviter toute fuite d'information du test vers le modèle.""")
md("## II. Régression par moindres carrés avec LinearRegression\n### Q4 · Entraîner le premier modèle")
code("Q4")
md("""**Réponse :** on obtient **5 coefficients** (un par variable explicative) et **1 constante**.
- `intercept_` = 230,39 : comme les variables sont centrées, c'est le prix moyen des maisons d'entraînement.
- La **surface** a l'effet le plus fort (+48,3 par écart-type), suivie de la distance au centre (−25,4) et de l'âge (−17,9) qui font baisser le prix ; le garage (+10,5) et le nombre de chambres (+8,7) l'augmentent.""")
md("### Q5 · Prédire et évaluer")
code("Q5")
md("""**Réponse :** les cinq premiers prix prédits sont proches des prix réels (ex. 268,8 → 271,1).
- **MAE = 11,60** : en moyenne, le modèle se trompe d'environ 11,6 milliers d'unités monétaires.
- **RMSE = 14,16** : un peu plus grande que la MAE car elle pénalise davantage les grosses erreurs ; l'écart reste faible, donc peu d'erreurs extrêmes.
- **R² = 0,949** : le modèle explique environ **95 %** de la variance des prix du test, c'est un très bon ajustement.""")
md("## III. Régression par descente de gradient avec SGDRegressor\n### Q6 · Entraîner le second modèle")
code("Q6")
md("""**Réponse :** `intercept_` = 230,84 et les coefficients sont très proches de ceux de `LinearRegression` (surface 48,45 contre 48,33 ; distance −25,96 contre −25,35…). `n_iter_ = 2000` : comme `tol=None`, il n'y a pas d'arrêt anticipé et le modèle effectue toutes les époques demandées.""")
md("### Q7 · Prédire et évaluer")
code("Q7")
md("""**Réponse :** SGDRegressor obtient **MAE = 12,09**, **RMSE = 14,57** et **R² = 0,946**. Ces résultats sont **très proches** de ceux de LinearRegression (écart de R² de 0,003), légèrement moins bons.""")
md("## IV. Comparaison et visualisation\n### Q8 · Comparer les deux modèles")
code("Q8"); code("Q8b")
md("""**Réponse :** **LinearRegression** obtient les meilleures performances sur le test pour les trois métriques (MAE, RMSE plus faibles et R² plus élevé), mais l'écart est faible.

Les coefficients diffèrent légèrement car :
- `LinearRegression` calcule la **solution exacte** des moindres carrés ;
- `SGDRegressor` approche cette solution de façon **itérative et stochastique** (mise à jour maison par maison, dans un ordre aléatoire) avec un **pas constant** `eta0 = 0.01` : il oscille autour du minimum sans s'y arrêter exactement.""")
md("### Q9 · Visualiser les prédictions")
code("Q9")
md("""**Réponse :** les points des deux modèles sont presque superposés et restent **regroupés autour de la droite y_prédit = y_réel**, ce qui confirme la bonne qualité des prédictions. Plus un point est proche de la droite, plus l'erreur est petite ; un point au-dessus correspond à une surestimation, un point en dessous à une sous-estimation. Quelques maisons isolées présentent des écarts d'environ 25 milliers.""")
md("## V. Expérimentations\n### Q10 · Étudier le taux d'apprentissage de SGDRegressor")
code("Q10")
md("""**Réponse :**

| eta0 | MAE | RMSE | R² |
|---|---|---|---|
| 0.0001 | 11,5964 | **14,1589** | 0,9489 |
| 0.001 | 11,6138 | 14,1744 | 0,9488 |
| 0.01 | 12,0906 | 14,5710 | 0,9459 |

Le taux d'apprentissage `eta0` fixe la **taille des pas** de la descente de gradient. Avec 2000 époques, les trois valeurs convergent ; le plus petit pas (0.0001) donne la meilleure RMSE, quasiment identique à LinearRegression. Avec un pas plus grand (0.01), le modèle oscille davantage autour du minimum, d'où une erreur légèrement plus élevée. Un pas trop petit avec peu d'époques ralentirait au contraire l'apprentissage.""")
md("### Q11 · Tester l'effet de la standardisation")
code("Q11a"); code("Q11b")
md("""**Réponse :** sans standardisation et avec `eta0 = 0.01`, l'apprentissage **diverge** : RMSE ≈ **3,05·10¹³**, les poids explosent car les variables de grande échelle (surface, âge) produisent des gradients énormes.

Avec `eta0 = 0.00001`, les pas deviennent assez petits pour éviter la divergence : le modèle converge vers **RMSE = 23,40** et **R² = 0,86**, mais reste nettement moins bon qu'avec les données standardisées (RMSE 14,57), car un seul pas ne convient pas à des variables d'échelles si différentes. La standardisation est donc indispensable pour SGD.""")
md("### Q12 · Suivre l'apprentissage du modèle")
code("Q12")
md("""**Réponse :** la MSE d'entraînement **diminue très fortement** dès les premières époques (2316 après la 1ʳᵉ époque), puis **se stabilise** autour de **192** jusqu'à la 100ᵉ époque, avec de très petites fluctuations. Le modèle apprend rapidement et a convergé après quelques époques : continuer l'entraînement n'apporte plus d'amélioration.""")
md("### Q13 · Prédire le prix d'une nouvelle maison")
code("Q13")
md("""**Réponse :** la nouvelle maison (125 m², 3 chambres, 15 ans, 7,5 km, garage) est standardisée avec `scaler.transform` (le scaler déjà ajusté). Prix estimés : **307,64 milliers** avec LinearRegression et **309,18 milliers** avec SGDRegressor, soit un écart d'environ 1,5 milliers seulement.""")
md("""## VI. Compte rendu

**1. Données utilisées —** 160 maisons pour l'entraînement et 40 pour le test (80 % / 20 %). Le modèle utilise **5 variables explicatives**.

**2. Paramètres du modèle —** LinearRegression donne **5 coefficients et 1 constante** : un coefficient pour chacune des 5 variables, plus l'ordonnée à l'origine (230,39).

**3. Qualité des prédictions —**

| Modèle | MAE | RMSE | R² |
|---|---|---|---|
| LinearRegression | 11,596 | 14,158 | 0,9489 |
| SGDRegressor | 12,091 | 14,571 | 0,9459 |

Avec LinearRegression, la MAE de 11,6 signifie qu'on se trompe en moyenne d'environ 11,6 milliers sur le prix, et le R² de 0,949 indique que le modèle explique près de 95 % de la variabilité des prix.

**4. Comparaison —** LinearRegression donne les meilleures prédictions : RMSE de 14,158 contre 14,571 pour SGDRegressor (et R² 0,9489 contre 0,9459).

**5. Lecture du graphique —** la droite pointillée représente y_prédit = y_réel (prédiction parfaite). Un point situé **au-dessus** de cette droite indique une **surestimation** du prix.

FIG9

**6. Taux d'apprentissage —** eta0 = **0.0001** donne la plus faible RMSE. RMSE obtenues : 14,1589 (0.0001) ; 14,1744 (0.001) ; 14,5710 (0.01).

**7. Standardisation —** sans standardisation, avec eta0 = 0.01, SGDRegressor diverge (RMSE ≈ 3,05·10¹³). Avec eta0 = 0.00001 il converge mais reste moins précis (RMSE = 23,40 ; R² = 0,86).

**8. Évolution de l'erreur —** l'erreur **diminue** fortement puis **se stabilise** autour de 192 : le modèle a convergé rapidement.

FIG12

**9. Nouvelle maison —** LinearRegression : **307,64** milliers d'unités monétaires ; SGDRegressor : **309,18** milliers. Les deux prédictions sont très proches.""")

# ---- build & execute notebook
nb = nbformat.v4.new_notebook()
nb.metadata["colab"] = {"provenance": []}
nb.cells = [nbformat.v4.new_markdown_cell(x.replace("\nFIG9\n","\n").replace("\nFIG12\n","\n")) if k=="md" else nbformat.v4.new_code_cell(x) for k,x in M]
NotebookClient(nb, timeout=600, kernel_name="python3").execute()
nbformat.write(nb, "TP3_Regression_Multiple_Trinome.ipynb")

# ---- render Colab-like HTML
fmt = HtmlFormatter(style=ColabStyle, nowrap=True)
figs = {}
blocks = []; n = 0
for i, c in enumerate(nb.cells):
    if c.cell_type == "markdown":
        src = M[i][1]
        h = markdown.markdown(src, extensions=["tables"])
        blocks.append(("md", h))
        continue
    n += 1
    outs = []
    for o in c.outputs:
        if o.output_type == "stream":
            outs.append(f'<pre class="txt">{html.escape(o.text.rstrip())}</pre>')
        elif "data" in o:
            d = o.data
            if "image/png" in d:
                tag = f'<img class="fig" src="data:image/png;base64,{d["image/png"]}">'
                figs.setdefault("FIG9" if "FIG9" not in figs else "FIG12", d["image/png"])
                outs.append(tag)
            elif "text/html" in d: outs.append(f'<div class="df">{d["text/html"]}</div>')
            else: outs.append(f'<pre class="txt">{html.escape(d["text/plain"])}</pre>')
    code_h = highlight(c.source, PythonLexer(), fmt)
    out_h = f'<div class="outrow"><div class="ogut"></div><div class="out">{"".join(outs)}</div></div>' if outs else ""
    blocks.append(("code", f'<div class="inrow"><div class="gutter"><span class="run">[{n}]</span></div><div class="code"><pre class="hl">{code_h}</pre></div></div>{out_h}'))

body = []
for k, h in blocks:
    for f, b64 in figs.items():
        cap = "Figure 1 – Prix réels vs prix prédits" if f=="FIG9" else "Figure 2 – MSE d'entraînement"
        h = h.replace(f"<p>{f}</p>", f'<p style="text-align:center"><img class="fig" style="width:360px;display:inline-block" src="data:image/png;base64,{b64}"><br><i style="font-size:12px">{cap}</i></p>')
    body.append(f'<div class="cell {k}">{h}</div>')

css = """
@page{size:A4;margin:10mm 9mm}
body{margin:0;font-family:Roboto,'Liberation Sans',Arial,sans-serif;color:#202124;background:#fff}
.bar{font-family:'Liberation Sans',Arial;border-bottom:1px solid #dadce0;padding:8px 0 6px 12px;position:relative;height:50px}
.logo{font-size:26px;letter-spacing:-3px;position:absolute;left:14px;top:12px}
.fname{position:absolute;left:62px;top:8px;font-size:17px}.star{position:absolute;left:400px;top:9px;color:#5f6368}
.menu{position:absolute;left:62px;top:33px;font-size:13px;color:#3c4043}
.share{position:absolute;right:16px;top:14px;font-size:13px;color:#1a73e8;border:1px solid #dadce0;border-radius:4px;padding:4px 10px}
.tool{font-size:12.5px;color:#3c4043;padding:6px 14px;border-bottom:1px solid #dadce0}
.tool .ram{float:right;color:#188038}
.wrap{padding:6px 6px}
.cell{margin:4px 0 8px 0;break-inside:auto}
.cell.md{padding:2px 12px 2px 52px;font-size:13.5px;line-height:1.5}
.md h1{font-size:24px;font-weight:400;margin:8px 0 6px}
.md h2{font-size:19px;font-weight:400;margin:14px 0 4px;border-bottom:none}
.md h3{font-size:15.5px;font-weight:500;margin:10px 0 2px}
.md p{margin:4px 0}.md ul{margin:3px 0;padding-left:22px}
.md code{font-family:'DejaVu Sans Mono',monospace;font-size:12px;background:#f1f3f4;padding:0 3px;border-radius:2px}
.md table{border-collapse:collapse;margin:6px 0;font-size:12.5px}
.md th,.md td{border:1px solid #dadce0;padding:4px 12px;text-align:center}
.md th{background:#f1f3f4}
.inrow{display:flex}
.gutter{width:46px;flex:none;display:flex;justify-content:center;padding-top:6px}
.run{font:12px 'DejaVu Sans Mono',monospace;color:#9aa0a6}
.code{flex:1;background:#f7f7f7;border:1px solid #f0f0f0}
pre.hl{margin:0;padding:7px 10px;font:11.6px/1.45 'DejaVu Sans Mono',monospace;white-space:pre-wrap}
.outrow{display:flex;margin-top:4px}.ogut{width:46px;flex:none}.out{flex:1;padding:2px 4px;min-width:0}
pre.txt{margin:2px 0;font:11.4px/1.4 'DejaVu Sans Mono',monospace;white-space:pre-wrap}
img.fig{width:430px;display:block;margin:4px 0}
.df table{border:none;border-collapse:collapse;font:11.5px Roboto,'Liberation Sans',Arial}
.df th,.df td{padding:4px 9px;text-align:right;border:none}
.df thead th{border-bottom:1px solid #ccc}
.df tbody tr:nth-child(odd){background:#f5f5f5}
"""
style = HtmlFormatter(style=ColabStyle).get_style_defs(".hl")
top = """<div class="bar"><span class="logo"><b style="color:#f9ab00">C</b><b style="color:#e8710a">O</b></span>
<span class="fname">TP3_Regression_Multiple_Trinome.ipynb</span><span class="star">☆</span>
<div class="menu">Fichier&nbsp;&nbsp; Modifier&nbsp;&nbsp; Affichage&nbsp;&nbsp; Insérer&nbsp;&nbsp; Exécution&nbsp;&nbsp; Outils&nbsp;&nbsp; Aide</div>
<span class="share">Partager</span></div>
<div class="tool">+ Code &nbsp;&nbsp; + Texte <span class="ram">✓ RAM ▬▬ Disque ▬</span></div>"""
page = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}{style}</style></head><body>{top}<div class="wrap">{"".join(body)}</div></body></html>'
open("TP3_Trinome_colab.html","w").write(page)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    pg = b.new_page()
    pg.goto("file://"+os.path.abspath("TP3_Trinome_colab.html"))
    pg.pdf(path="TP3_Trinome_Zeffana_Khalfi_Kheiri_Colab.pdf", format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
print("done", list(figs))
