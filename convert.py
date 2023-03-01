import os
import sys
import glob
import pandas as pd
import paramiko
from datetime import datetime
from __main__ import *

tag=input("Identifiying tag")
base_path=os.path.abspath(__file__ + "/../../")
save_path=f"{base_path}/data/raw/{tag}/test.zip"

def ssh_extract():
    ip=input("Device IP Address")
    ssh_username=input("Login Username")
    ssh_password=input("Login Password")
    command="/export"
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
                    ip, 
                    username=ssh_username, 
                    password=ssh_password
                    )
    except PermissionError as e:
        print("Could not connect, try again")
        ssh_extract()
    _stdin, _stdout,_stderr=client.exec_command(command)    
    with open('file', 'w') as sys.stdout:
        print(_stdout.read().decode())
    client.close()

def rsclist():
    global rsc_list
    rsc_file=glob.glob(save_path + '\\*.rsc')   
    rsc_list = []
    str1 = ''
    with open(rsc_file) as rsc:
        for line in rsc:
            if line.startswith('add '):
                str1 = line.replace('list=CountryIPBlocks\n',
                                    'list=CountryIPBlocks ')
                rsc_list.append(str1)
    return (rsc_list)


def rsczip(rsc_list):
    global df_rsc
    df_rscr = pd.DataFrame(rsc_list)
    df_rscn = df_rscr.drop(0)
    newrow = df_rscn.DataFrame(dts, index=[0])
    df_rsc = df_rscn.concat([newrow, df_rscn.loc[:]]).reset_index(drop=True)
    df_rsc.to_csv(df_rsc, index=False, compression="zip")
    return (df_rsc)


def main():
    global inputdir
    global rsc_files
    global rsc_file
    global df_rsc
    global rsc_list
    global dts
    n = datetime.now()
    dts = n.strftime("%d/%m/%Y %H:%M:%S")
    rsc_list = rsclist(rsc_file)
    print("[Convert] Start")
    os.chdir(save_path)
    print("[Convert] setting up ssh tunnel to device")
    ssh_extract()
    print("[Convert] extraction succesful")
    print("[Convert] converting to .zip")
    rsclist()
    rsczip(rsc_list)
    print("Save successful")
    print(f"[Convert] End")

main()
