import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n = 500
klienci = ["Anna Kowalska", "  Jan Nowak", "Anna Kowalska", "PIOTR WIŚNIEWSKI",
           "katarzyna lewandowska", "Tomasz Zieliński ", "Marta Wójcik",
           "anna kowalska ", "Krzysztof Kamiński", " Magdalena Dąbrowska"]
produkty = ["Laptop", "Mysz", "Klawiatura", "Monitor", "laptop", "MYSZ",
            "Słuchawki", "Pendrive", "monitor", "Webcam"]
kategorie = ["Elektronika", "elektronika", "ELEKTRONIKA", "Akcesoria",
             "akcesoria", "Akcesoria "]
miasta = ["Warszawa", "Kraków", "warszawa", "Gdańsk", "WROCŁAW",
          "Poznań", "Łódź ", " Warszawa", "kraków"]

start_date = datetime(2025, 1, 1)
daty_iso = [(start_date + timedelta(days=int(d))).strftime("%Y-%m-%d")
            for d in np.random.randint(0, 300, n // 2)]
daty_pl = [(start_date + timedelta(days=int(d))).strftime("%d.%m.%Y")
           for d in np.random.randint(0, 300, n // 2)]
daty = daty_iso + daty_pl
np.random.shuffle(daty)

df = pd.DataFrame({
    "order_id": range(1001, 1001 + n),
    "klient": np.random.choice(klienci, n),
    "produkt": np.random.choice(produkty, n),
    "kategoria": np.random.choice(kategorie, n),
    "miasto": np.random.choice(miasta, n),
    "ilosc": np.random.choice([1, 2, 3, 5, -1, 0], n, p=[0.5, 0.2, 0.15, 0.1, 0.025, 0.025]),
    "cena_jednostkowa": np.random.choice(
        ["199.99", "299,99", "1 499.00", "89.50", "2999", "399.00 zł", None, "abc"],
        n
    ),
    "data_zamowienia": daty,
    "email": np.random.choice(
        ["anna@gmail.com", "JAN@WP.PL", "piotr.w@onet", "marta@gmail.com",
         "tomasz@interia.pl", None, "krzysztof.k@gmail.com", "brak"],
        n
    )
})

# Wprowadzamy braki i duplikaty
for col in ["miasto", "kategoria", "data_zamowienia"]:
    df.loc[df.sample(frac=0.05, random_state=1).index, col] = np.nan

df = pd.concat([df, df.sample(20, random_state=2)], ignore_index=True)

df.to_csv("zamowienia_messy.csv", index=False)
print(f"Wygenerowano plik 'zamowienia_messy.csv' — {len(df)} wierszy")