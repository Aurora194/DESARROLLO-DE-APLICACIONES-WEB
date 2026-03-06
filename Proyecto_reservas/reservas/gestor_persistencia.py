# persisntecia de datos de archivos
import json
import csv
from pathlib import Path


DATA_DIR = Path(__file__). parent / "data"
TXT_FILE = DATA_DIR/ "datos.txt"
CSV_FILE = DATA_DIR / "datos.csv"

# ASEGURAR LA DATA
def asegurar_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

 # Persistencia TXT

 # Guardar datos txt
def guardar_txt (registro: str):
    asegurar_data_dir()
    with open(TXT_FILE, 'a', encoding="utf-8") as f:
        f.write(registro + '\n')

 # leer datos txt
def leer_txt():
    asegurar_data_dir()
    if not TXT_FILE.exists():
        return []
    with open(TXT_FILE, 'r', encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


# Persistencia JSON

# Guardar datos json
def guardar_json(dic, dict):
    asegurar_data_dir()
    data = leer_json()
    data.append(dict)
    with open(DATA_DIR/ "datos.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# leer datos json
def leer_json():
    asegurar_data_dir()
    json_file = DATA_DIR/ "datos.json"
    if not json_file.exists():
        return []
    with open(json_file, 'r', encoding="utf-8") as f:
        return json.load(f)

# Persistencia CSV

# Guardar datos cvs
def guardar_csv(dic: dict):
    asegurar_data_dir()
    existe = CSV_FILE.exists()
    with open(CSV_FILE, 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(['Campo1', 'Campo2', 'Campo3']) # Encabezados
        writer.writerow(dic)

# leer datos csv
def leer_csv():
    asegurar_data_dir()
    if not CSV_FILE.exists():
        return []
    with open (CSV_FILE, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        next (reader, None) # Saltar encabezados
        return [row for row in reader if row]