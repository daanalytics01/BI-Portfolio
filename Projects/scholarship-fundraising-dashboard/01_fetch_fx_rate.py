import pandas as pd
import requests
from io import StringIO

CSV_URL = "https://infra.datos.gob.ar/catalog/sspm/dataset/175/distribution/175.1/download/tipos-de-cambio-historicos.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

if __name__ == "__main__":
    resp = requests.get(CSV_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    df = pd.read_csv(StringIO(resp.text))
    df["indice_tiempo"] = pd.to_datetime(df["indice_tiempo"])

    df_filtrado = df[df["indice_tiempo"] >= "2020-01-01"][["indice_tiempo", "dolar_estadounidense"]]
    df_filtrado.columns = ["fecha", "usd_ars_oficial"]
    df_filtrado = df_filtrado.dropna()

    df_filtrado.to_csv("data/tipo_cambio_oficial.csv", index=False)
    print(f"Guardadas {len(df_filtrado)} filas en data/tipo_cambio_oficial.csv")
    print(df_filtrado.tail())