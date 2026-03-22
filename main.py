import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt



# # pierwszej waluty
def get_currency(currencies_dict):
    if currencies_dict:
        return list(currencies_dict.keys())[0]
    return None



#pobranie danych
url = "https://restcountries.com/v3.1/all?fields=name,capital,region,subregion,population,area,currencies"
response = requests.get(url)
response.raise_for_status()  #zamkniecie w razie gdy blad po stronie API

data = response.json()

kraje_lista = []

for kraj in data:
    nazwa = kraj.get("name", {}).get("common")

    capital_list = kraj.get("capital")
    stolica = capital_list[0] if capital_list else None

    region = kraj.get("region")
    subregion = kraj.get("subregion")
    populacja = kraj.get("population")
    powierzchnia = kraj.get("area")
    waluta = get_currency(kraj.get("currencies"))

    kraje_lista.append({
        "nazwa": nazwa,
        "stolica": stolica,
        "region": region,
        "subregion": subregion,
        "populacja": populacja,
        "powierzchnia": powierzchnia,
        "waluta": waluta,
    })



#tworzenie tabeli
kraje_df = pd.DataFrame(kraje_lista)

print("\nHEAD DataFrame:")
print(kraje_df.head())

print("\nSHAPE DataFrame:")
print(kraje_df.shape)

print("\nDTYPES DataFrame:")
print(kraje_df.dtypes)



#zapis do bazy sqlite
conn = sqlite3.connect("kraje_swiata.db")
kraje_df.to_sql("kraje", conn, if_exists="replace", index=False)
print("\nTabela 'kraje' została zapisana do bazy kraje_swiata.db")




#analiza SQL i odpowiedzi na pytania


# 1. Jaka jest łączna populacja świata?
query1 = """
SELECT SUM(populacja) AS laczna_populacja_swiata
FROM kraje;
"""
print("\n1. Łączna populacja świata:")
print(pd.read_sql_query(query1, conn))


# 2. Które 10 krajów ma największą populację?
query2 = """
SELECT nazwa, populacja
FROM kraje
ORDER BY populacja DESC
LIMIT 10;
"""
print("\n2. 10 krajów z największą populacją:")
print(pd.read_sql_query(query2, conn))


# 3. Ile krajów jest w każdym regionie i jaka jest ich średnia populacja?
query3 = """
SELECT region,
       COUNT(*) AS liczba_krajow,
       AVG(populacja) AS srednia_populacja
FROM kraje
GROUP BY region
ORDER BY liczba_krajow DESC;
"""
print("\n3. Liczba krajów w każdym regionie i średnia populacja:")
print(pd.read_sql_query(query3, conn))


# 4. Które kraje mają powierzchnię większą niż Polska (~312 679 km²)?
query4 = """
SELECT nazwa, powierzchnia
FROM kraje
WHERE powierzchnia > 312679
ORDER BY powierzchnia DESC;
"""
print("\n4. Kraje o powierzchni większej niż Polska:")
print(pd.read_sql_query(query4, conn))


# 5. Który kraj ma najwyższą gęstość zaludnienia (populacja / powierzchnia)?
query5 = """
SELECT nazwa,
       populacja,
       powierzchnia,
       (populacja * 1.0 / powierzchnia) AS gestosc_zaludnienia
FROM kraje
WHERE powierzchnia IS NOT NULL
  AND powierzchnia > 0
ORDER BY gestosc_zaludnienia DESC
LIMIT 1;
"""
print("\n5. Kraj o najwyższej gęstości zaludnienia:")
print(pd.read_sql_query(query5, conn))



#wykres z danymi
query_chart = """
SELECT region, SUM(populacja) AS laczna_populacja
FROM kraje
GROUP BY region
ORDER BY laczna_populacja DESC;
"""

wykres_df = pd.read_sql_query(query_chart, conn)


plt.figure(figsize=(10, 6))
plt.bar(wykres_df["region"], wykres_df["laczna_populacja"])
plt.title("Łączna populacja w regionach świata")
plt.xlabel("Region")
plt.ylabel("Łączna populacja")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("wykres_populacja_regionow.png")
plt.show()


print("\nWykres został zapisany jako: wykres_populacja_regionow.png")



conn.close()
