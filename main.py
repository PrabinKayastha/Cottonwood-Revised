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
        all_data_file_paths = [file for file in all_asc_file_paths if "topo.asc" not in file and "hbfl" not in file
                               and "ss" not in file]
        if all_data_file_paths:
            print(str(len(all_data_file_paths)) + " data files found!!!")

            # Maintain lookup for filename and file path
            data_file_location_lookup = {extract_filename_from_filepath(file_path): file_path for file_path in
                                         all_data_file_paths}
            # pprint(data_file_location_lookup)

            # Maintain lookup for file name and AscData objects
            data_file_objects_lookup = {extract_filename_from_filepath(file_path): create_asc_data_obj(file_path)
                                        for file_path in all_data_file_paths}
            # pprint(data_file_objects_lookup.keys())

            # Maintain lookup for filename and AscData objects
            topo_adjusted_data_lookup = bulk_fetch_topo_adjusted_data(data_file_objects_lookup)
            # pprint(topo_adjusted_data_lookup.keys())

            # Export the adjusted data for future reference
            export_topo_adjusted_data(topo_adjusted_data_lookup)

            days_difference_lookup = calc_bulk_asc_data_difference(topo_adjusted_data_lookup)
            # pprint(days_difference_lookup.keys())

            running_averages = calc_topo_adj_asc_running_avg(days_difference_lookup)
            # pprint(running_averages.keys())

            running_averages_categorized = categorize_data_values(running_averages)
            # pprint(running_averages_categorized.keys())
            # pprint(len(running_averages_categorized))

            accumulated_data_lookup = accumulate_iteration_values(running_averages_categorized)
            # pprint(accumulated_data_lookup.keys())

            normalized_accumulated_lookup = normalize_accululated_data(accumulated_data_lookup)
            # pprint(normalized_accumulated_lookup.keys())

            categorized_normalized_acc_data = categorize_normalized_acc_data(normalized_accumulated_lookup)
            # pprint(categorized_normalized_acc_data.keys())

            # pprint(data_file_objects_lookup["wd_day1.asc"].hbfl_file_metadata)
            hbfl_topo_adjusted_data_lookup = bulk_fetch_hbfl_adjusted_data(topo_adjusted_data_lookup,
                                                                           data_file_objects_lookup)

            hbfl_categorized_data_lookup = categorize_with_hbfl_data(hbfl_topo_adjusted_data_lookup)

            export_hbfl_categorized_data(hbfl_categorized_data_lookup)

            shear_stress_classified = shear_stress_file()

            # pprint(list(categorized_normalized_acc_data.keys()))
            # pprint(list(hbfl_categorized_data_lookup.keys()))

            cottonwood_lookup = {}

            for key, value in categorized_normalized_acc_data.items():
                cottonwood_lookup[key.replace('categorized_normalized_accumulation_from_iter', 'cottonwood_data_iter')] =\
                    calc_final_val(value, hbfl_categorized_data_lookup[key.replace('categorized_normalized_accumulation_from_iter', 'classified_hbfl_wd_day') + '.asc']
                                   , shear_stress_classified["shear_stress_data"])
            # pprint(cottonwood_lookup.keys())

            categorized_cottonwood_lookup = categorize_with_cottonwood(cottonwood_lookup)
            # pprint(categorized_cottonwood_lookup.keys())

            export_cottonwood_categorized_data(categorized_cottonwood_lookup)

            export_max_cottonwood_value(list(categorized_cottonwood_lookup.values()))

            export_mean_cottonwood_value(list(categorized_cottonwood_lookup.values()))


        else:
            print("WARNING ::: No asc data files found!!!!!")
    else:
        print("Failed!!!!!!!!!!")
        break

