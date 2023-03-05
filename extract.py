import os
import csv
import tempfile
import requests
from zipfile import ZipFile
from datetime import datetime
from convert import inputdir
from multiprocessing import Process

n=datetime.now()
dts=n.strftime("%d/%m/%Y")
base_path=os.path.abspath(__file__ + "/../../")
source_zip=inputdir+"/example.zip"
# path to save the .zip file // curently set up for my comp
source_path=f"{base_path}/data/source/2023-02-14/srctest.zip"
# path to extract the .csv/ / curently set up for my comp
raw_path=f"{base_path}/data/raw/{dts}"
# END


def create_folder(path):
    """
    creates a new folder if one dosent exist
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def download_file():
    """
    download file from the source folder
    """
    with open(source_path, "wb") as s:
        response=requests.get(source_zip, verify=False)
        s.write(response.content)


def save_new_raw_data():
    """
    save the raw data from the new file
    """

    create_folder(raw_path)  
    with tempfile.TemporaryDirectory() as dirpath:
        with ZipFile(source_path, "r",) as zipfile:
            name_list=zipfile.namelist()
            csv_file_path=zipfile.extract(name_list[0], path=dirpath)
            with open(csv_file_path, mode="r", encoding="UTF-8") as csv_file:
                reader=csv.DictReader(csv_file)
                with open(raw_path, mode="w", encoding="UTF-8",) as csv_file:
                    writer=csv.DictWriter(csv_file)
                    for row in reader:
                        writer.writerow(row)


def main():
    print("[Extract] Start")
    print("[Extract] Downloading file")
    download_file()
    print(f"[Extract] Saving data from '{source_path}' to '{raw_path}'")
    if __name__=='__main__':
        p=Process(target=save_new_raw_data())
        p.start()
        p.join()
    print(f"[Extract] End")
