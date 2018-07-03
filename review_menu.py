from function_file import *
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
current_dir = os.path.dirname("__file__")
current_dir = current_dir if current_dir is not '' else '.'
# directory to scan for any txt files
data_dir_path = current_dir + '/Information_user'



def main():
    # f = open(data_dir_path + "id_menu.txt", 'r')
    with open(data_dir_path + "/known.json",'r', encoding = 'utf8') as lst:
        b = json.load(lst)
    print(b)

if __name__ == "__main__":
    main()
    
    
