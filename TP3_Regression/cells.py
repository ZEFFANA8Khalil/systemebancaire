# Code cells for each student's notebook. Each entry: (question_tag, code)
KHALIL = [
("imports", """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score"""),
("Q1a", """df = pd.read_csv("prix_maisons.csv")
df.head()"""),
("Q1b", """print("Dimensions :", df.shape)
df.info()"""),
("Q1c", """df.describe().round(2)"""),
("Q1d", """print("Valeurs manquantes :")
print(df.isna().sum())"""),
("Q2", """variables = ["surface", "nb_chambres", "age", "dist_centre", "garage"]
X = df[variables]
y = df["prix"]
print("Dimensions de X :", X.shape)
print("Dimensions de y :", y.shape)"""),
("Q3", """X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)   # fit uniquement sur le train
X_test_std = scaler.transform(X_test)

print("Entraînement :", X_train_std.shape)
print("Test :", X_test_std.shape)"""),
("Q4", """modele_lr = LinearRegression()
modele_lr.fit(X_train_std, y_train)

print("Constante :", modele_lr.intercept_)
print("Coefficients :")
print(pd.Series(modele_lr.coef_, index=variables))"""),
("Q5", """pred_lr = modele_lr.predict(X_test_std)
print(pd.DataFrame({
    "Prix réel": y_test.iloc[:5].to_numpy(),
    "Prix prédit": pred_lr[:5]
}).round(2))

mae_lr = mean_absolute_error(y_test, pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, pred_lr))
r2_lr = r2_score(y_test, pred_lr)
print("\\nMAE :", round(mae_lr, 3))
print("RMSE :", round(rmse_lr, 3))
print("R² :", round(r2_lr, 4))"""),
("Q6", """modele_sgd = SGDRegressor(
    loss="squared_error", penalty=None,
    learning_rate="constant", eta0=0.01,
    max_iter=2000, tol=None, random_state=42
)
modele_sgd.fit(X_train_std, y_train)

print("Constante :", modele_sgd.intercept_)
print("Coefficients :")
print(pd.Series(modele_sgd.coef_, index=variables))
print("Nombre d'époques :", modele_sgd.n_iter_)"""),
("Q7", """pred_sgd = modele_sgd.predict(X_test_std)
mae_sgd = mean_absolute_error(y_test, pred_sgd)
rmse_sgd = np.sqrt(mean_squared_error(y_test, pred_sgd))
r2_sgd = r2_score(y_test, pred_sgd)
print("MAE :", round(mae_sgd, 3))
print("RMSE :", round(rmse_sgd, 3))
print("R² :", round(r2_sgd, 4))"""),
("Q8", """comparaison = pd.DataFrame({
    "Modèle": ["LinearRegression", "SGDRegressor"],
    "MAE": [mae_lr, mae_sgd],
    "RMSE": [rmse_lr, rmse_sgd],
    "R²": [r2_lr, r2_sgd]
})
comparaison.round(4)"""),
("Q8b", """pd.DataFrame({"LinearRegression": modele_lr.coef_,
              "SGDRegressor": modele_sgd.coef_}, index=variables).round(3)"""),
("Q9", """plt.figure(figsize=(7, 5))
plt.scatter(y_test, pred_lr, label="LinearRegression", alpha=0.75)
plt.scatter(y_test, pred_sgd, label="SGDRegressor", marker="x")

borne_min = min(y_test.min(), pred_lr.min(), pred_sgd.min())
borne_max = max(y_test.max(), pred_lr.max(), pred_sgd.max())
plt.plot([borne_min, borne_max], [borne_min, borne_max],
         "k--", label="Prédiction parfaite")
plt.xlabel("Prix réel (milliers d'unités monétaires)")
plt.ylabel("Prix prédit (milliers d'unités monétaires)")
plt.title("Comparaison des prédictions sur le test")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()"""),
("Q10", """essais = []
for eta in [0.0001, 0.001, 0.01]:
    modele = SGDRegressor(
        loss="squared_error", penalty=None,
        learning_rate="constant", eta0=eta,
        max_iter=2000, tol=None, random_state=42
    )
    modele.fit(X_train_std, y_train)
    pred = modele.predict(X_test_std)
    essais.append({
        "eta0": eta,
        "MAE": mean_absolute_error(y_test, pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, pred)),
        "R²": r2_score(y_test, pred)
    })
print(pd.DataFrame(essais).round(4))"""),
("Q11a", """modele_brut = SGDRegressor(
    loss="squared_error", penalty=None,
    learning_rate="constant", eta0=0.01,
    max_iter=2000, tol=None, random_state=42
)
modele_brut.fit(X_train, y_train)  # données non standardisées
pred_brut = modele_brut.predict(X_test)
print("RMSE sans standardisation :",
      np.sqrt(mean_squared_error(y_test, pred_brut)))"""),
("Q11b", """modele_brut2 = SGDRegressor(
    loss="squared_error", penalty=None,
    learning_rate="constant", eta0=0.00001,
    max_iter=2000, tol=None, random_state=42
)
modele_brut2.fit(X_train, y_train)
pred_brut2 = modele_brut2.predict(X_test)
print("eta0=0.00001 -> RMSE :", round(np.sqrt(mean_squared_error(y_test, pred_brut2)), 3))
print("               R²   :", round(r2_score(y_test, pred_brut2), 4))"""),
("Q12", """modele_suivi = SGDRegressor(
    loss="squared_error", penalty=None,
    learning_rate="constant", eta0=0.01,
    random_state=42
)
mse_history = []
for epoque in range(100):
    modele_suivi.partial_fit(X_train_std, y_train)
    pred_train = modele_suivi.predict(X_train_std)
    mse_history.append(mean_squared_error(y_train, pred_train))

plt.plot(range(1, 101), mse_history)
plt.xlabel("Nombre d'époques")
plt.ylabel("MSE d'entraînement")
plt.title("Évolution de l'erreur pendant l'apprentissage")
plt.grid(alpha=0.3)
plt.show()
print("MSE époque 1 :", round(mse_history[0], 2), "| époque 100 :", round(mse_history[-1], 2))"""),
("Q13", """nouvelle_maison = pd.DataFrame([{
    "surface": 125, "nb_chambres": 3, "age": 15,
    "dist_centre": 7.5, "garage": 1
}])
nouvelle_std = scaler.transform(nouvelle_maison[variables])
prix_lr = modele_lr.predict(nouvelle_std)[0]
prix_sgd = modele_sgd.predict(nouvelle_std)[0]
print("LinearRegression :", round(prix_lr, 2))
print("SGDRegressor :", round(prix_sgd, 2))"""),
]

YOUNES = [
("imports", """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score"""),
("Q1a", """# Q1 - chargement
data = pd.read_csv('prix_maisons.csv')
data.head()"""),
("Q1b", """print('Taille du dataset :', data.shape)
print()
print(data.dtypes)"""),
("Q1c", """data.describe()"""),
("Q1d", """data.isna().sum()"""),
("Q2", """# Q2 - X et y
features = ['surface', 'nb_chambres', 'age', 'dist_centre', 'garage']
X = data[features]
y = data['prix']
print('X :', X.shape, ' | y :', y.shape)"""),
("Q3", """# Q3 - split 80/20 + standardisation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sc = StandardScaler()
X_train_s = sc.fit_transform(X_train)
X_test_s = sc.transform(X_test)

print('train :', X_train_s.shape, ' test :', X_test_s.shape)
print('moyennes apprises :', sc.mean_.round(2))"""),
("Q4", """# Q4 - LinearRegression
lr = LinearRegression()
lr.fit(X_train_s, y_train)
print('intercept_ :', round(lr.intercept_, 4))
for nom, c in zip(features, lr.coef_):
    print(f'  {nom:<12} {c:9.4f}')"""),
("Q5", """# Q5 - prediction + metriques
y_pred_lr = lr.predict(X_test_s)
print(pd.DataFrame({'reel': y_test.values[:5], 'predit': y_pred_lr[:5].round(2)}))

mae_lr  = mean_absolute_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
r2_lr   = r2_score(y_test, y_pred_lr)
print(f'\\nMAE = {mae_lr:.3f}   RMSE = {rmse_lr:.3f}   R2 = {r2_lr:.4f}')"""),
("Q6", """# Q6 - SGDRegressor
sgd = SGDRegressor(loss='squared_error', penalty=None, learning_rate='constant',
                   eta0=0.01, max_iter=2000, tol=None, random_state=42)
sgd.fit(X_train_s, y_train)
print('intercept_ :', sgd.intercept_)
for nom, c in zip(features, sgd.coef_):
    print(f'  {nom:<12} {c:9.4f}')
print('n_iter_ :', sgd.n_iter_)"""),
("Q7", """# Q7
y_pred_sgd = sgd.predict(X_test_s)
mae_sgd  = mean_absolute_error(y_test, y_pred_sgd)
rmse_sgd = np.sqrt(mean_squared_error(y_test, y_pred_sgd))
r2_sgd   = r2_score(y_test, y_pred_sgd)
print(f'MAE = {mae_sgd:.3f}   RMSE = {rmse_sgd:.3f}   R2 = {r2_sgd:.4f}')"""),
("Q8", """# Q8 - tableau comparatif
res = pd.DataFrame({'MAE': [mae_lr, mae_sgd],
                    'RMSE': [rmse_lr, rmse_sgd],
                    'R2': [r2_lr, r2_sgd]},
                   index=['LinearRegression', 'SGDRegressor'])
res.round(4)"""),
("Q8b", """# ecart entre les coefficients des deux modeles
pd.DataFrame({'LR': lr.coef_, 'SGD': sgd.coef_, 'ecart': lr.coef_ - sgd.coef_}, index=features).round(3)"""),
("Q9", """# Q9 - reel vs predit
plt.figure(figsize=(7, 5))
plt.scatter(y_test, y_pred_lr, alpha=0.7, label='LinearRegression')
plt.scatter(y_test, y_pred_sgd, marker='x', color='tab:red', label='SGDRegressor')
m = min(y_test.min(), y_pred_lr.min(), y_pred_sgd.min())
M = max(y_test.max(), y_pred_lr.max(), y_pred_sgd.max())
plt.plot([m, M], [m, M], 'k--', label='Prédiction parfaite')
plt.xlabel("Prix réel (milliers)")
plt.ylabel("Prix prédit (milliers)")
plt.title("Prix réels vs prix prédits (test)")
plt.legend()
plt.grid(alpha=0.3)
plt.show()"""),
("Q10", """# Q10 - influence de eta0
lignes = []
for eta in [0.0001, 0.001, 0.01]:
    m_eta = SGDRegressor(loss='squared_error', penalty=None, learning_rate='constant',
                         eta0=eta, max_iter=2000, tol=None, random_state=42)
    m_eta.fit(X_train_s, y_train)
    p = m_eta.predict(X_test_s)
    lignes.append([eta, mean_absolute_error(y_test, p),
                   np.sqrt(mean_squared_error(y_test, p)), r2_score(y_test, p)])
pd.DataFrame(lignes, columns=['eta0', 'MAE', 'RMSE', 'R2']).round(4)"""),
("Q11a", """# Q11 - sans standardisation, eta0 = 0.01
sgd_brut = SGDRegressor(loss='squared_error', penalty=None, learning_rate='constant',
                        eta0=0.01, max_iter=2000, tol=None, random_state=42)
sgd_brut.fit(X_train, y_train)
p_brut = sgd_brut.predict(X_test)
print('RMSE sans standardisation :', np.sqrt(mean_squared_error(y_test, p_brut)))"""),
("Q11b", """# on reessaie avec un pas beaucoup plus petit
sgd_brut2 = SGDRegressor(loss='squared_error', penalty=None, learning_rate='constant',
                         eta0=0.00001, max_iter=2000, tol=None, random_state=42)
sgd_brut2.fit(X_train, y_train)
p_brut2 = sgd_brut2.predict(X_test)
print('eta0 = 1e-5  ->  RMSE =', round(np.sqrt(mean_squared_error(y_test, p_brut2)), 3),
      ' R2 =', round(r2_score(y_test, p_brut2), 4))"""),
("Q12", """# Q12 - suivi de la MSE avec partial_fit
suivi = SGDRegressor(loss='squared_error', penalty=None, learning_rate='constant',
                     eta0=0.01, random_state=42)
mse = []
for ep in range(100):
    suivi.partial_fit(X_train_s, y_train)
    mse.append(mean_squared_error(y_train, suivi.predict(X_train_s)))

plt.figure(figsize=(7, 4))
plt.plot(range(1, 101), mse, color='tab:green')
plt.xlabel("Époque")
plt.ylabel("MSE (train)")
plt.title("MSE d'entraînement en fonction des époques")
plt.grid(alpha=0.3)
plt.show()
print('min =', round(min(mse), 2), ' max =', round(max(mse), 2), ' derniere =', round(mse[-1], 2))"""),
("Q13", """# Q13 - nouvelle maison
maison = pd.DataFrame([[125, 3, 15, 7.5, 1]], columns=features)
maison_s = sc.transform(maison)
print('LinearRegression :', round(lr.predict(maison_s)[0], 2), 'milliers')
print('SGDRegressor     :', round(sgd.predict(maison_s)[0], 2), 'milliers')"""),
]
