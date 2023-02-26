import os; import glob; import pandas as pd;import csv;from datetime import datetime;from __main__ import *

def start():
    """Starts the script, set globals and takes input for file path
     none   
    Returns:
     .zip file conversion function output to selected directory path"""
    global inputdir
    global rsc_files
    global rsc_file
    global df_rsc
    global rsc_list
    global dts
    n = datetime.now()
    dts = n.strftime("%d/%m/%Y %H:%M:%S")
    try:
        inputdir=input('enter .rsc file path --> ')
    except FileNotFoundError as e:
        print('Input directory path')
        start()
    except PermissionError as e:
        print('Input directory path')
        start()
    rsc_files=getrsc_files(inputdir)
    rsc_file=rscselect(di_rsc_files) 
    rsc_list=rsclist(rsc_file)  


def getrsc_files(inputdir):
    """change dir to .rsc file path, 
    picks up files places them in a dict
    Args:
     directory path(str)
    Returns: 
     dict"""
    global di_rsc_files
    try:
        os.chdir(inputdir)
    except FileNotFoundError as e:
        print('Input correct path directory')
        start()
    rsc_files=glob.glob(inputdir + '\\*.rsc')
    di_rsc_files={ i : rsc_files[i] for i in range(0, len(rsc_files) ) }
    return(di_rsc_files) 

def rscselect(di_rsc_files):
    """allows user to select .rsc file from dict
    Args:
     di_rsc_files=dictonary of .rsc file names  
    Returns:
     .rsc file in list object"""
    global di_rsc_file
    for key, value in di_rsc_files.items():
        print(key, ' : ', value)
    try:
        knum=input('select file key number --> ')
        i=int(knum)
        di_rsc_filer=di_rsc_files[i]
        di_rsc_file=os. rename(i, dts+i)
    except ValueError as e:
        print('Input correct key number')
        rscselect(di_rsc_files)
    except IndexError as e:
        print('Input correct key number')
        rscselect(di_rsc_files) 
    except KeyError as e:
        print('Input correct key number')
        rscselect(di_rsc_files)
    return(di_rsc_file)

def rsclist(rsc_file):
    global rsc_list
    rsc_list=[]
    str1=''
    with open(rsc_file) as rsc:
        for line in rsc:
            if line.startswith('add '):
                str1=line.replace('list=CountryIPBlocks\n', 'list=CountryIPBlocks ')
                rsc_list.append(str1)
    return(rsc_list)

def rsczip(rsc_list):
    """for use with IP-firewall-Address-List.rsc
    changes dir, creates pd-df from rsc_list, 
    converts to .zip file
    Args:
     rsc_file=path and file directory
    Returns:
     writes new .zip file to path directory"""
    global df_rsc
    df_rscr=pd.DataFrame(rsc_list)
    df_rscn=df_rscr.drop(0)
    newrow=df_rscn.DataFrame(dts, index=[0])
    df_rsc=df_rscn.concat([newrow,df_rscn.loc[:]]).reset_index(drop=True)
    df_rsc.to_csv(df_rsc, index=False, compression="zip")
    return(df_rsc)

