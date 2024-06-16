<p align="center">
    <img src="./rosatom-logo-brandlogos.net.png" alt="Логотип проекта" width="500" style="display: inline-block; vertical-align: middle; margin-right: 10px;"/>  <br/>
     <H2 align="center">Команда Ikanam</H2> 
    <H2 align="center">Кейс "Определение и классификация дефектов сварных швов с помощью ИИ"</H2> 
</p>


*1. Загрузите репозиторий на свой компьютер и откройте её в вашей предпочитаемой среде разработки (IDE).* 
```python
git clone https://github.com/ikanam-ai/Detection-of-welding-seams.git
```
*2. Откройте терминал в IDE и введите туда следующую команду:* 

```python
python -m venv .venv
.\.venv\Scripts\activate
```
*3. Дождитесь создание папки `.venv` затем введите следующую команду:*

```python
cd Detection-of-welding-seams/frontend/streamlit
```
*3.  Инициализация проекта:*

```python
poetry init
poetry update
poetry install
```
*4. Запустите приложение через Poetry:*

```python
poetry run streamlit run zapusk.py
```

[Screencast](https://disk.yandex.ru/d/4W-iDxXXSmnaDw) наших сервисов





## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for Detection-of-welding-seams
│                         and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── Detection-of-welding-seams                <- Source code for use in this project.
    │
    ├── __init__.py    <- Makes Detection-of-welding-seams a Python module
    │
    ├── data           <- Scripts to download or generate data
    │   └── make_dataset.py
    │
    ├── features       <- Scripts to turn raw data into features for modeling
    │   └── build_features.py
    │
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict_model.py
    │   └── train_model.py
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py
```

--------

