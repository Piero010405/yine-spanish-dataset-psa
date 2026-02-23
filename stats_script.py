"""
Estadisticas generales del corpus final de Yine-Español
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# config
plt.rcParams.update({
    "font.size": 12,
    "figure.figsize": (8,5),
})

# Cargar corpus final
df = pd.read_csv(
    "data/processed/merged/full_corpus.csv",
    sep=";",
    encoding="utf-8-sig",
    engine="python"
)

print("=== ESTADISTICAS GENERALES ===")
print(f"Total pares: {len(df)}")

# Longitud en tokens
df["len_yine"] = df["yine"].str.split().apply(len)
df["len_spanish"] = df["spanish"].str.split().apply(len)

def describe_column(col):
    """
    Describe estadísticamente una columna numérica, devolviendo media, mediana, desviación estándar, 
    mínimo y máximo.
    """
    return {
        "mean": np.mean(col),
        "median": np.median(col),
        "std": np.std(col),
        "min": np.min(col),
        "max": np.max(col)
    }

stats_yine = describe_column(df["len_yine"])
stats_spanish = describe_column(df["len_spanish"])

print("\n=== YINE ===")
print(stats_yine)

print("\n=== SPANISH ===")
print(stats_spanish)

# Pares por fuente
print("\n=== DISTRIBUCION POR FUENTE ===")
print(df["source"].value_counts())

"""
Histogramas de longitud de oraciones
"""

plt.figure()
plt.hist(df["len_yine"], bins=50)
plt.title("Distribución longitud de oraciones - Yine")
plt.xlabel("Número de tokens")
plt.ylabel("Frecuencia")
plt.savefig("plots/hist_yine.png")
plt.savefig("plots/hist_yine.pdf", format="pdf", bbox_inches="tight")
plt.close()

plt.figure()
plt.hist(df["len_spanish"], bins=50)
plt.title("Distribución longitud de oraciones - Español")
plt.xlabel("Número de tokens")
plt.ylabel("Frecuencia")
plt.savefig("plots/hist_spanish.png")
plt.savefig("plots/hist_spanish.pdf", format="pdf", bbox_inches="tight")
plt.close()

"""
Box Comparison
"""
plt.figure()
plt.boxplot([df["len_yine"], df["len_spanish"]])
plt.xticks([1, 2], ["Yine", "Español"])
plt.title("Comparación de longitudes")
plt.ylabel("Número de tokens")
plt.savefig("plots/boxplot_lengths.png")
plt.savefig("plots/boxplot_lengths.pdf", format="pdf", bbox_inches="tight")
plt.close()

"""
Pares por fuente
"""
counts = df["source"].value_counts()

plt.figure()
plt.bar(counts.index, counts.values)
plt.title("Número de pares por fuente")
plt.xlabel("Fuente")
plt.ylabel("Cantidad")
plt.savefig("plots/pairs_by_source.png")
plt.savefig("plots/pairs_by_source.pdf", format="pdf", bbox_inches="tight")

plt.close()
