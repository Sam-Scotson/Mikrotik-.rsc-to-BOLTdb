import os
import csv
import requests
from datetime import datetime
from common.tables import ConfigRaw
from common.base import session
from sqlalchemy import text

base_path = os.path.abspath(__file__ + "/../../")
raw_path = f"{base_path}/data/raw/2023-02-14/testraw.csv"

def transform_case(input_string):
    """
    Lowercase string fields
    """
    return input_string.lower()

def update_date(date_input):
    """
    Update date format from DD/MM/YYYY to YYYY-MM-DD
    """
    current_format = datetime.strptime(date_input, "%d/%m/%Y")
    new_format = current_format.strftime("%Y-%m-%d")
    return new_format 

def cleanup_config(config_input):
    """
    Removes all cli tags such as 'add', 'ip', etc
    """
    f_str = ""
    with open(raw_path, "wb") as f:
        config=requests.get(raw_path, verify=False)
        f.write(config.content, f_str)
    f_str_update = f_str.replace(
        "add", ""
        ).replace(
        "/interface", ""
        ).replace(
        "/ip", ""
        ).replace(
        "/system", ""
        ).replace(
        "#", ""
        )
    with open(raw_path, "wb") as f:
        f.write(f_str_update)

def truncate_table():
    """
    Ensures that the table is in a empty state before running transformation
    """
    session.execute(
        text("TRUNCATE TABLE Config_raw;ALTER SEQUENCE Config_raw_id_seq RESTART;")
    )
    session.commit()

def transform_new_data():
    """
    Apply all transformations for each row in the .csv file before saving it into database
    """
    with open(raw_path, mode="r", encoding="windows-1252") as csv_file:
        reader = csv.DictReader(csv_file)
        config_raw_objects = []
        for row in reader:
            config_raw_objects.append(
                ConfigRaw(
                    config=cleanup_config(row["config"]),
                )
            )
        session.bulk_save_objects(config_raw_objects)
        session.commit()

def main():
    print("[Transform] Start")
    print("[Transform] Remove any old data from config_raw table")
    truncate_table()
    print("[Transform] Transform new data available in config_raw table")
    transform_new_data()
    print("[Transform] End")