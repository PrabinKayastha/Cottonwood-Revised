from UtilityFunctions import *
from colorama import Fore

all_asc_files = []
data_file_location = {}  # stores datafile names and its file location
data_file_objects = {}  # list of AscData class objects of all input data files

while True:
    print(Fore.RED + "Hit 'Enter' to quit." + Fore.RESET)
    path = input(Fore.YELLOW + "Input the folder locations if any ::: " + Fore.RESET)
    if path:
        all_asc_files = get_list_of_asc_input_files(path)
        print(all_asc_files)
    else:
        print("Failed!!!!!!!!!!")
        break

