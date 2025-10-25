import pandas as pd
import requests
import sys

url = "https://apicadprev.trabalho.gov.br/DAIR_CARTEIRA"
parametros = {
    'nr_cnpj_entidade': "29131075000193",
    'sg_uf': "RJ",
    'dt_ano': 2025
}

arquivo_csv = "investimentos_marica_2025.csv"

response = requests.get(url, timeout=60, params=parametros)



if response.ok:
    data = response.json()["data"]
    df = pd.DataFrame(data)
    df.to_excel("rafael.xlsx")
    df.head()
    df.info()


else:
    print("houve um problema")

