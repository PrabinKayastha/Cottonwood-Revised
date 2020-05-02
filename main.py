from UtilityFunctions import *
from colorama import Fore
from pprint import pprint

all_asc_files = []
data_file_location_lookup = {}  # stores datafile names and its file location
data_file_objects_lookup = {}  # lookup of AscData class objects of all input data files

while True:
    print(Fore.RED + "Hit 'Enter' to quit." + Fore.RESET)
    path = input(Fore.YELLOW + "Input the folder locations if any ::: " + Fore.RESET)
    if path:
        all_asc_file_paths = get_list_of_asc_input_file_paths(path)
        # Evaluate input asc data
        all_data_file_paths = [file for file in all_asc_file_paths if "topo.asc" not in file]
        if all_data_file_paths:
            print(str(len(all_data_file_paths)) + " data files found!!!")

            # Maintain lookup for filename and file path
            data_file_location_lookup = {extract_filename_from_filepath(file_path): file_path for file_path in
                                         all_data_file_paths}
            pprint(data_file_location_lookup)

            # Maintain lookup for filename and AscData objects
            data_file_objects_lookup = {extract_filename_from_filepath(file_path): create_asc_data_obj(file_path)
                                        for file_path in all_data_file_paths}

            asc_data_objects = export_topo_adjusted_data(all_data_file_paths)
        else:
            print("WARNING ::: No asc data files found!!!!!")
    else:
        print("Failed!!!!!!!!!!")
        break

