import os;import csv;import tempfile;from zipfile import ZipFile;import requests; from convert import inputdir

base_path=os.path.abspath(__file__ + "/../../")

# START 
source_zip=inputdir+"/example.zip"
#path to save the .zip file // curently set up for my comp
source_path=f"{base_path}/data/source/downloaded_at=2023-02-14/test.zip"
#path to extract the .csv/ / curently set up for my comp
raw_path=f"{base_path}/data/raw/downloaded_at=2023-02-14/test.csv"
# END 

def create_folder(path):
    """
    creates a new folder if one dosent exist
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def download_file():
    """
    download file from the source
    """
    create_folder(source_path)
    with open(source_path, "wb") as s:
        response=requests.get(source_zip, verify=False)
        s.write(response.content)

def save_new_raw_data():
    """
    save the raw data from the new file
    """

    create_folder(raw_path)#!!!!multithread it!!!
    with tempfile.TemporaryDirectory() as dirpath:
        with ZipFile(source_path,"r",) as zipfile:
            name_list=zipfile.namelist()
            csv_file_path=zipfile.extract(name_list[0], path=dirpath)
            with open(csv_file_path, mode="r", encoding="UTF-8") as csv_file:
                reader=csv.DictReader(csv_file)
                with open(raw_path,mode="w",encoding="UTF-8",) as csv_file:
                    writer=csv.DictWriter(csv_file)
                    for row in reader:
                        writer.writerow(row)


def main():
    print("[Extract] Start")
    print("[Extract] Downloading file")
    download_file()
    print(f"[Extract] Saving data from '{source_path}' to '{raw_path}'")
    save_new_raw_data()
    print(f"[Extract] End")