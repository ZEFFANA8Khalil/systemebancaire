import sys, os, base64
from playwright.sync_api import sync_playwright
name = sys.argv[1]
S = f"shots_{name}"
def img(tag, w=100):
    b = base64.b64encode(open(f"{S}/{tag}.png","rb").read()).decode()
    return f'<img class="shot" style="width:{w}%" src="data:image/png;base64,{b}">'

if name == "khalil":
    who, outil = "Khalil ZEFFANA", "Google Colab"
    Q = [
     ("Q1 · Chargement et exploration", ["bar","imports","Q1a","Q1b","Q1c","Q1d"],
      "Le fichier contient 200 maisons et 6 colonnes, toutes numériques (int64 / float64). Aucune valeur manquante, donc pas de nettoyage à faire. Le prix moyen est d’environ 230 milliers avec un écart-type de 64."),
     ("Q2 · Variables explicatives et cible", ["Q2"],
      "X a 200 lignes et 5 colonnes, y a 200 valeurs. Chaque ligne de X correspond à une maison décrite par ses 5 caractéristiques (surface, chambres, âge, distance, garage)."),
     ("Q3 · Découpage et standardisation", ["Q3"],
      "On obtient 160 maisons pour l’entraînement et 40 pour le test. La standardisation met toutes les variables à moyenne 0 et écart-type 1 : sans elle, la surface (≈100) écraserait le garage (0/1) et la descente de gradient converge mal. Le scaler est ajusté seulement sur le train pour ne pas utiliser d’information du test."),
     ("Q4 · Modèle LinearRegression", ["Q4"],
      "On obtient 5 coefficients (un par variable) et 1 seule constante. La constante 230,39 correspond au prix moyen du train car les X sont centrés. La surface a le plus grand effet (+48,3), l’âge et la distance font baisser le prix."),
     ("Q5 · Prédiction et évaluation (LinearRegression)", ["Q5"],
      "MAE = 11,60 : en moyenne le modèle se trompe d’environ 11,6 milliers. RMSE = 14,16, un peu plus grande car elle pénalise plus les grosses erreurs. R² = 0,949 : le modèle explique environ 95 % de la variance des prix du test."),
     ("Q6 · Modèle SGDRegressor", ["Q6"],
      "Le modèle a bien fait les 2000 époques (tol=None). Les coefficients sont très proches de ceux de LinearRegression (ex. surface 48,45 contre 48,33)."),
     ("Q7 · Évaluation de SGDRegressor", ["Q7"],
      "MAE = 12,09, RMSE = 14,57 et R² = 0,946. C’est très proche de LinearRegression, légèrement moins bon."),
     ("Q8 · Comparaison des deux modèles", ["Q8","Q8b"],
      "LinearRegression est un peu meilleur sur les trois métriques. La différence vient du fait que LinearRegression calcule la solution exacte des moindres carrés, alors que SGD met à jour les poids maison par maison avec un pas constant (eta0=0.01) : il oscille autour de l’optimum sans s’y arrêter exactement."),
     ("Q9 · Prix réels vs prix prédits", ["Q9"],
      "Les points des deux modèles sont presque superposés et restent proches de la diagonale, donc les prédictions sont bonnes. Les écarts les plus visibles (±25) concernent quelques maisons isolées."),
     ("Q10 · Effet du taux d’apprentissage", ["Q10"],
      "Plus eta0 est petit, plus le résultat se rapproche de LinearRegression (RMSE 14,159 pour 0.0001). Le taux d’apprentissage règle la taille des pas : un pas trop grand fait osciller le modèle autour du minimum, un pas plus petit est plus précis mais plus lent."),
     ("Q11 · Sans standardisation", ["Q11a","Q11b"],
      "Avec eta0=0.01 sur les données brutes, l’apprentissage diverge complètement (RMSE ≈ 3·10¹³). Avec eta0=0.00001 le modèle ne diverge plus mais reste moins bon (RMSE 23,4, R² 0,86) car les variables n’ont pas la même échelle et le pas est trop petit pour certaines d’entre elles."),
     ("Q12 · Évolution de la MSE (partial_fit)", ["Q12"],
      "La MSE chute très vite (2316 à la 1ère époque) puis se stabilise vers 192 dès les premières époques. Le modèle a donc convergé rapidement, il n’y a plus de gain après ~5 époques."),
     ("Q13 · Prix d’une nouvelle maison", ["Q13"],
      "Pour 125 m², 3 chambres, 15 ans, 7,5 km et garage : 307,64 milliers avec LinearRegression et 309,18 milliers avec SGDRegressor. Les deux estimations sont très proches (écart ≈ 1,5)."),
    ]
    CR = [
     ("1. Données utilisées", "160 maisons pour l’entraînement et 40 pour le test (80 % / 20 %). Le modèle utilise 5 variables explicatives."),
     ("2. Paramètres du modèle", "LinearRegression donne 5 coefficients et 1 constante : un coefficient par variable explicative, plus l’ordonnée à l’origine (230,39)."),
     ("3. Qualité des prédictions", "TABLE La MAE de 11,60 signifie qu’on se trompe en moyenne d’environ 11,6 milliers sur le prix, et le R² de 0,949 indique que le modèle explique près de 95 % de la variabilité des prix."),
     ("4. Comparaison", "LinearRegression donne les meilleures prédictions : RMSE de 14,158 contre 14,571 pour SGDRegressor (et R² 0,9489 contre 0,9459)."),
     ("5. Lecture du graphique", "La droite pointillée représente y_prédit = y_réel, c’est-à-dire une prédiction parfaite. Un point au-dessus de la droite correspond à une surestimation du prix."),
     ("6. Taux d’apprentissage", "eta0 = 0.0001 donne la plus faible RMSE. RMSE obtenues : 14,1589 (0.0001) ; 14,1744 (0.001) ; 14,5710 (0.01)."),
     ("7. Standardisation", "Sans standardisation et avec eta0 = 0.01, le SGD diverge : RMSE ≈ 3,05·10¹³. Avec eta0 = 0.00001 il converge mais reste moins précis (RMSE = 23,40 ; R² = 0,86)."),
     ("8. Évolution de l’erreur", "L’erreur diminue fortement au début puis se stabilise autour de 192. On en déduit que le modèle converge rapidement et que les époques suivantes n’apportent plus d’amélioration."),
     ("9. Nouvelle maison", "LinearRegression : 307,64 milliers d’unités monétaires ; SGDRegressor : 309,18 milliers. Les deux prédictions sont proches."),
    ]
    style = "body{font-family:'Liberation Serif','Times New Roman',serif;}"
else:
    who, outil = "Younes KHALFI", "Jupyter Notebook (Anaconda)"
    Q = [
     ("Question 1 – Chargement et exploration", ["bar","imports","Q1a","Q1b","Q1c","Q1d"],
      "Le dataset a 200 lignes (maisons) et 6 colonnes. Toutes les colonnes sont numériques et il n’y a aucune valeur manquante. Les prix vont de 43,7 à 359,3 milliers."),
     ("Question 2 – Définition de X et y", ["Q2"],
      "X est de taille (200, 5) et y de taille (200,). Une ligne de X = une maison avec ses 5 caractéristiques."),
     ("Question 3 – Split et standardisation", ["Q3"],
      "Split 80/20 : 160 maisons en train, 40 en test. Le StandardScaler apprend moyenne et écart-type sur le train uniquement (sinon fuite de données vers le test). Il permet de mettre les variables à la même échelle, ce qui est indispensable pour la descente de gradient."),
     ("Question 4 – LinearRegression", ["Q4"],
      "On a 5 coefficients (un par variable) et 1 constante (intercept_ = 230,39). Les variables étant standardisées, on peut comparer les coefficients : la surface pèse le plus, la distance et l’âge ont un effet négatif."),
     ("Question 5 – Évaluation de LinearRegression", ["Q5"],
      "MAE ≈ 11,6 milliers d’erreur moyenne ; RMSE ≈ 14,2 (plus sensible aux grandes erreurs) ; R² ≈ 0,95, donc le modèle explique la grande majorité des variations de prix."),
     ("Question 6 – SGDRegressor", ["Q6"],
      "n_iter_ = 2000 : toutes les époques ont été faites puisque tol=None. Les coefficients trouvés ressemblent beaucoup à ceux de la question 4."),
     ("Question 7 – Évaluation de SGDRegressor", ["Q7"],
      "MAE = 12,09 ; RMSE = 14,57 ; R² = 0,946. Les résultats sont proches de LinearRegression mais un peu moins bons."),
     ("Question 8 – Tableau comparatif", ["Q8","Q8b"],
      "LinearRegression est légèrement meilleur. Les coefficients diffèrent un peu (écart max ≈ 0,8 sur garage) car LinearRegression donne la solution analytique exacte, alors que SGD est une méthode itérative stochastique avec un pas fixe qui ne tombe jamais exactement sur le minimum."),
     ("Question 9 – Graphique réel / prédit", ["Q9"],
      "Les points sont groupés autour de la droite y = x, et les croix (SGD) sont pratiquement sur les points (LR). Plus un point est proche de la droite, plus la prédiction est juste."),
     ("Question 10 – Taux d’apprentissage eta0", ["Q10"],
      "eta0 = 0.0001 donne la plus petite RMSE (14,1589), presque égale à LinearRegression. Avec 0.01 les pas sont plus grands et le modèle « saute » autour du minimum, d’où une erreur un peu plus élevée."),
     ("Question 11 – Sans StandardScaler", ["Q11a","Q11b"],
      "Sur les données brutes avec eta0 = 0.01 le modèle explose (RMSE de l’ordre de 10¹³). En prenant eta0 = 0.00001 les pas deviennent assez petits pour ne plus diverger, mais la RMSE (23,4) reste bien pire qu’avec standardisation."),
     ("Question 12 – Courbe de la MSE", ["Q12"],
      "La MSE passe de 2316 à environ 192 en quelques époques, puis reste stable jusqu’à la 100e. Le modèle apprend vite et converge."),
     ("Question 13 – Nouvelle maison", ["Q13"],
      "La maison est standardisée avec sc.transform (le même scaler). Prix estimé : 307,64 milliers (LR) et 309,18 milliers (SGD)."),
    ]
    CR = [
     ("1. Données utilisées", "Entraînement : 160 maisons ; test : 40 maisons. Le modèle utilise 5 variables explicatives."),
     ("2. Paramètres du modèle", "On obtient 5 coefficients et une constante, car il y a un poids pour chacune des 5 variables plus un terme constant (intercept)."),
     ("3. Qualité des prédictions", "TABLE Avec LinearRegression l’erreur moyenne est de 11,6 milliers (MAE) et R² = 0,949 : environ 95 % de la variance des prix est expliquée par le modèle."),
     ("4. Comparaison", "C’est LinearRegression qui prédit le mieux : sa MAE (11,596) et sa RMSE (14,158) sont inférieures à celles de SGDRegressor (12,091 et 14,571)."),
     ("5. Lecture du graphique", "La droite pointillée correspond aux points où le prix prédit est égal au prix réel (prédiction parfaite). Un point au-dessus signifie que le modèle surestime le prix."),
     ("6. Taux d’apprentissage", "La plus faible RMSE est obtenue avec eta0 = 0.0001. RMSE : 14,1589 pour 0.0001, 14,1744 pour 0.001 et 14,5710 pour 0.01."),
     ("7. Standardisation", "Sans standardisation, l’apprentissage devient instable : avec eta0 = 0.01 la RMSE vaut environ 3,05·10¹³ (divergence). Avec eta0 = 0.00001 le modèle converge mais RMSE = 23,40 et R² = 0,86, donc moins bon qu’avec les données standardisées."),
     ("8. Évolution de l’erreur", "La MSE diminue très rapidement puis se stabilise (≈ 192). On en déduit que le modèle a convergé dès les premières époques."),
     ("9. Nouvelle maison", "LinearRegression prédit 307,64 et SGDRegressor 309,18 milliers d’unités monétaires, soit des prix très proches (≈ 1,5 d’écart)."),
    ]
    style = "body{font-family:'Liberation Sans',Arial,sans-serif;font-size:10.6pt}"

table = """<table class="met"><tr><th>Modèle</th><th>MAE</th><th>RMSE</th><th>R²</th></tr>
<tr><td>LinearRegression</td><td>11,596</td><td>14,158</td><td>0,9489</td></tr>
<tr><td>SGDRegressor</td><td>12,091</td><td>14,571</td><td>0,9459</td></tr></table>"""

parts = []
for title, tags, txt in Q:
    shots = "".join(img(t) for t in tags)
    parts.append(f'<div class="q"><h3>{title}</h3>{shots}<p>{txt}</p></div>')
cr = []
for t, a in CR:
    if a.startswith("TABLE"):
        a = table + "<p>" + a[6:] + "</p>"
    else:
        a = f"<p>{a}</p>"
    if t.startswith("5."):
        a += f"<div class='fig'>{img('fig9',100)}<div class='cap'>Figure 1 – Prix réels vs prix prédits (ensemble de test)</div></div>"
    if t.startswith("8."):
        a += f"<div class='fig'>{img('fig12',100)}<div class='cap'>Figure 2 – MSE d’entraînement en fonction des époques</div></div>"
    cr.append(f"<div class='cr'><h4>{t}</h4>{a}</div>")

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page{{size:A4;margin:16mm 15mm 16mm 15mm}}
{style}
body{{color:#111;font-size:11pt;line-height:1.35}}
.head{{border-bottom:1.5px solid #333;padding-bottom:6px;margin-bottom:10px}}
.head h1{{font-size:17pt;margin:0 0 4px 0;text-align:center}}
.head .meta{{display:flex;justify-content:space-between;font-size:10.5pt}}
h2{{font-size:13pt;margin:16px 0 6px;border-bottom:1px solid #999}}
h3{{font-size:11.5pt;margin:12px 0 5px}}
h4{{font-size:11pt;margin:8px 0 2px}}
p{{margin:4px 0 6px;text-align:justify}}
img.shot{{display:block;border:1px solid #c8c8c8;margin:4px 0}}
.q{{break-inside:auto}}
.cr p{{margin:2px 0 4px}}
table.met{{border-collapse:collapse;margin:4px 0 6px;width:80%}}
table.met td,table.met th{{border:1px solid #444;padding:3px 8px;text-align:center}}
table.met th{{background:#e6e6e6}}
.fig{{width:58%;margin:4px auto 6px}} .cap{{text-align:center;font-size:9.5pt;font-style:italic}}
</style></head><body>
<div class="head"><h1>Compte rendu – TP3 : Régression linéaire multiple</h1>
<div class="meta"><span><b>Nom :</b> {who}</span><span><b>Environnement :</b> {outil}</span></div></div>

<h2>Compte rendu</h2>
{''.join(cr)}

<h2 style="break-before:page">Annexe – Travail réalisé sur {outil}</h2>
{''.join(parts)}
</body></html>"""
open(f"CR_{name}.html","w").write(html)
pdf = {"khalil":"CR_TP3_Khalil_Zeffana.pdf","younes":"CR_TP3_Younes_Khalfi.pdf"}[name]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    pg = b.new_page()
    pg.goto("file://"+os.path.abspath(f"CR_{name}.html"))
    pg.pdf(path=pdf, format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
print(pdf)
