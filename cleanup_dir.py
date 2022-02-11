from os import listdir
from os import remove

def cleanup_dir():
    DIR_PATH = 'c:\\users\\repos'
    lis_files = listdir(DIR_PATH)
    
    for file in lis_files:
      if not file.startswith('centos'):
        remove(DIR_PATH + "\\" + file)

cleanup_dir() 