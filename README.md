# Yine–Spanish Parallel Corpus Builder 🇵🇪📖

Pipeline reproducible para la construcción de un corpus paralelo **Yine–Español** a partir de múltiples fuentes:

* 📘 **Diccionario Virtual Yine** (Ministerio de Cultura del Perú)
* 📖 **Biblia Yine** (ebible.org)
* 📗 **Biblia Español** (ebible.org)

## El proyecto permite

* **Scraping estructurado** de fuentes web.
* **Normalización y limpieza robusta** de texto.
* **Alineamiento** versículo por versículo.
* **Fusión** de múltiples fuentes.
* **Generación de dataset final** listo para NMT (Neural Machine Translation).

## 📂 Estructura del Proyecto

```text
YINE-SPANISH-DATASET-PSA/
│
├── config/
│   ├── constants.py
│   └── settings.py
│
├── lib/
│   └── books_dict.py
│
├── pipelines/
│   ├── scrape_dictionary.py
│   ├── scrape_bible.py
│   └── build_full_corpus.py
│
├── scraper_dictionary/
│   ├── extractor.py
│   ├── fetcher.py
│   ├── normalizer.py
│   ├── paginator.py
│   └── parser.py
│
├── scraper_bible/
│   ├── scraper.py
│   ├── processor.py
│   ├── aligner.py
│   └── dataset_builder.py
│
├── utils/
│   ├── io.py
│   └── logger.py
│
├── data/
│   ├── raw/
│   └── processed/
│
└── requirements.txt
```

## 🎯 Objetivo

Construir un corpus paralelo Yine–Español combinando:

1. **Ejemplos del diccionario Yine**
2. **Versículos alineados de la Biblia**
3. **Dataset consolidado final**

El resultado es un archivo listo para:

* **Fine-tuning de NMT** (Neural Machine Translation)
* **Evaluación lingüística**
* **Estudios morfológicos**
* **Publicación académica**

## ⚙️ Requisitos

* Python 3.9+
* Instalar dependencias:

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
`requests`, `beautifulsoup4`, `lxml`, `pandas`, `ftfy`, `tqdm`.

## 🚀 Orden de Ejecución

El pipeline completo consta de 3 pasos:

### 1️⃣ Scrape del Diccionario

Extrae ejemplos paralelos Yine–Español desde: [http://diccionariovirtualyine.culturacusco.gob.pe](http://diccionariovirtualyine.culturacusco.gob.pe)

```bash
python -m pipelines.scrape_dictionary
```

**Salida:** `data/processed/parallel_sentences.csv`

**Incluye:**

* Normalización UTF robusta.
* Eliminar corchetes [ ].
* Preservación correcta de puntuación.
* Exportación compatible con Excel.

### 2️⃣ Scrape y Alineamiento de la Biblia

Descarga versículos Yine y Español desde [ebible.org](https://ebible.org/) y los alinea versículo por versículo.

```bash
python -m pipelines.scrape_bible
```

**Salida:** `data/processed/merged/yine_spanish.csv`

**Características:**

* Alineamiento basado en <span class="verse">.
* Soporte para div.p, div.q, div.q1, div.q2.
* Exclusión de subtítulos (div.s).
* Reparación automática de encoding.
* Guardado de HTML crudo para trazabilidad.

### 3️⃣ Merge Final del Corpus

Fusiona el Diccionario y la Biblia generando un único dataset consolidado.

```bash
python -m pipelines.build_full_corpus
```

**Salida final:** `data/processed/final/yine_spanish_full_corpus.csv`

**Incluye columna `source` para trazabilidad:**

* dictionary
* bible

## 🧪 Validación y Robustez

Este proyecto incluye:
* Corrección robusta de encoding **UTF-8**.
* Reparación de *mojibake*.
* Manejo seguro de HTML malformado.
* Exportación CSV compatible con Excel.
* Guardado de HTML crudo para auditoría.
* Alineamiento conservador (no heurístico agresivo).

## 📚 Estándares Académicos

En investigaciones de Machine Translation:

* Es válido combinar múltiples fuentes.
* Debe documentarse claramente el origen.
* Se recomienda mantener la columna `source`.
* Puede reportarse por separado en análisis experimental.

## 🔬 Uso en Investigación

Este corpus puede emplearse para:

* Entrenamiento NMT low-resource.
* Evaluación BLEU / chrF++.
* Análisis morfológico.
* Estudios tipológicos.
* Evaluación humana posterior.

## 📝 Licencia y Consideraciones

Antes de uso público:

1. Verificar términos de uso del diccionario virtual.
2. Verificar licencia de `ebible.org`.
3. Citar adecuadamente las fuentes.

## 👨‍💻 Autor

Proyecto desarrollado como parte de investigación en:

**Low-Resource Neural Machine Translation / Lenguas indígenas del Perú**
