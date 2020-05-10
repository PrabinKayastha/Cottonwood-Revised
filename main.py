from UtilityFunctions import *
from colorama import Fore
from pprint import pprint

all_asc_files = []
data_file_location_lookup = {}  # stores datafile names and its file location
data_file_objects_lookup = {}  # lookup of AscData class objects of all input data files
data_file_analysis_details = {}

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
            # pprint(data_file_location_lookup)

            # Maintain lookup for filenpython main
            # ame and AscData objects
            data_file_objects_lookup = {extract_filename_from_filepath(file_path): create_asc_data_obj(file_path)
                                        for file_path in all_data_file_paths}
            # pprint(data_file_objects_lookup)

            # Maintain lookup for filename and AscData objects
            topo_adjusted_data_lookup = bulk_fetch_topo_adjusted_data(data_file_objects_lookup)
            # pprint(topo_adjusted_data_lookup)

            # Export the adjusted data for future reference
            export_topo_adjusted_data(topo_adjusted_data_lookup)

            days_difference_lookup = calc_bulk_asc_data_difference(topo_adjusted_data_lookup)
            pprint(days_difference_lookup.keys())

            running_averages = calc_topo_adj_asc_running_avg(days_difference_lookup)

        else:
            print("WARNING ::: No asc data files found!!!!!")
    else:
        print("Failed!!!!!!!!!!")
        break

