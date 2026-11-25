import numpy as np, pandas as pd
rng = np.random.default_rng(7)
n = 200
surface = rng.normal(110, 32, n).clip(40, 230).round(0)
nb_ch = np.clip(np.round(surface/35 + rng.normal(0, 0.7, n)), 1, 6).astype(int)
age = rng.integers(0, 61, n)
dist = rng.uniform(0.5, 25, n).round(1)
garage = (rng.random(n) < 0.55).astype(int)
prix = 85 + 1.75*surface + 9*nb_ch - 1.1*age - 3.8*dist + 22*garage + rng.normal(0, 14, n)
df = pd.DataFrame(dict(prix=prix.round(1), surface=surface.astype(int), nb_chambres=nb_ch, age=age, dist_centre=dist, garage=garage))
df.to_csv("prix_maisons.csv", index=False)
print(df.describe().round(2))
