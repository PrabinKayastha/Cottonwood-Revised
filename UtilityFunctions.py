import os
from itertools import tee, islice
import csv
import json
import numpy as np
from colorama import Fore
import re
from ast import literal_eval as make_tuple


from AscData import AscData
# from pprint import pprint


def print_banner(message, border="*"):
    """
    Prints the 'message' within the border.
    param message: A meaningful message.
    param border: Contents of the border.
    """
    line = border * len(message)
    print(Fore.GREEN + "\n" + Fore.GREEN + line)
    print(message)
    print(line + "\n" + Fore.RESET)


def get_list_of_asc_input_file_paths(path):
    """
    Prompts for user input of a file location.
    Returns for an array containing the file locations and a dictionary for the data file name with its location for
    given user input of a file location.
    return: list of all files location.
    """
    all_asc_files = []

    for r, d, f in os.walk(path):  # r=root, d=directory F=file
        for file in f:
            if ".asc" in file:
                all_asc_files.append(os.path.join(r, file))
    return all_asc_files


def extract_filename_from_filepath(file_path):
    """
    Returns the filename from the file path.
    :param file_path : file path
    :returns filename from the filepath passed.
    """
    if "\\" in file_path:
        return file_path.split("\\")[-1]
    elif "/" in file_path:
        return file_path.split("/")[-1]


def create_asc_data_obj(file_location):
    """
    Creates an object of AscData class type for ".asc" file passed.
    param _datafile_location: File path for ".asc" file.
    returns : Object of AscData class type.
    """
    if file_location:
        message = "Creating object {} file.".format(file_location)
        print_banner(message)
        data_file_object = AscData(file_location)
        return data_file_object


def write_asc_data_file(asc_data, output_file_path):
    """
    Write asc data into the output files.
    param _asc_data: The data to be written.
    param _output_location: The output file location.
    """
    message = "Writing the results into {} file.".format(output_file_path)
    print_banner(message)
    with open(output_file_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=" ")
        writer.writerows(asc_data)


def bulk_fetch_topo_adjusted_data(data_file_objects_lookup):
    """
        Returns a dictionary of .asc filename and its corresponding AscData type object.
        Adjusts the data values in object of type AscData class with the topo.asc data.
        param data_file_objects_lookup: Root folder location for the input files.
        return: Dictionary of .asc filename and its corresponding topo adjusted data.
    """
    topo_adjusted_data_files_dict = {}
    for data_file, data_file_object in data_file_objects_lookup.items():
        topo_adjusted_data_files_dict[data_file] = data_file_object.adjust_with_topo()
    return topo_adjusted_data_files_dict


def export_topo_adjusted_data(topo_adjusted_data_lookup):
    """
    Writes adjusted data into a output file location.
    param topo_adjusted_data_lookup: lookup with the asc filename and its data.
    """
    for data_file_name, topo_adjusted_data in topo_adjusted_data_lookup.items():
        adjusted_output_location = "./Output Files/Topo Adjusted Files/adj_" + data_file_name
        write_asc_data_file(topo_adjusted_data, adjusted_output_location)
    print("The adjusted output can be found at './Output Files/Topo Adjusted Files/' in the project root folder.")


def calc_diff_asc_data(asc_minuend, asc_subtrahend):
    """
    Calculates the differences between two asc array data.
    param _asc_minuend: 'a' in (a - b)
    param _asc_subtrahend: 'b' in (a - b)
    return: The difference of two asc arrays
    """
    difference = np.subtract(asc_minuend, asc_subtrahend)
    return difference


def calc_bulk_asc_data_difference(data_file_collection):
    """
    Calculates the consecutive difference for arrays passed. Here, (2nd item - 1st item), (3rd item - 2nd item)
    and so on.
    :param data_file_collection: array of arrays
    :return: array of differences of arrays
    """
    diff_array_results = {}
    for itr in range(len(data_file_collection) - 1):
        message = "Calculating the difference for Day {} and Day {}".format(str(itr + 2), str(itr + 1))
        print_banner(message)
        diff_array_result = calc_diff_asc_data(data_file_collection['wd_day' + str(itr + 2) + '.asc'],
                                               data_file_collection['wd_day' + str(itr + 1) + '.asc'])
        diff_array_results['difference_day' + str(itr + 2) + '_minus_day' + str(itr + 1) + '_result' +
                           str(itr + 1) + '.asc'] = diff_array_result

        output_location = '.\\Output Files\\Difference Results\\difference_day' + str(itr + 2) + \
                          '_minus_day' + str(itr + 1) + '_result' + str(itr + 1) + '.asc'
        write_asc_data_file(diff_array_result, output_location)

    return diff_array_results


def generate_tuples_for_running_average(asc_data_lookup, n=3):
    """
    Initialize the running datasets of 'n' data files.
    param _data_file_objects: Dictionary of .asc filename and its corresponding AscData type object.
    param n: Size of the window. Default running window size is 3.
    return: The zipped tuples of data sets for a given window size.
    """
    sorted_asc_data_list = []
    if re.match(r'\Adifference_day', list(asc_data_lookup.keys())[0]):
        sorted_asc_data_list = sorted(asc_data_lookup.items(),
                                      key=lambda x: int(x[0][x[0].rfind("_result") + 7: x[0].rfind(".asc")]))
    elif re.match(r'\Awd_day', list(asc_data_lookup.keys())[0]):
        sorted_asc_data_list = sorted(asc_data_lookup.items(),
                                      key=lambda x: int(x[0][x[0].rfind("\\wd_day") + 7: x[0].rfind(".asc")]))
    # print(sorted_asc_data_list)
    _asc_data_dict_sorted = {}
    for i in sorted_asc_data_list:
        _asc_data_dict_sorted[i[0]] = i[1]

    iters = tee(_asc_data_dict_sorted.values(), n)

    for i, it in enumerate(iters):
        next(islice(it, i, i), None)
    return zip(*iters)


def calc_topo_adj_asc_running_avg(asc_data_lookup, n=3):
    """
    Calculate the running average for 'n' datafiles and write them into output file location.
    param _data_file_objects: Dictionary of .asc filename and its corresponding AscData type object.
    param n: Window size for the running average. Default running window is 3.
    return: running average of the data for each iterations in a dictionary.
    """
    obj_colls_list = generate_tuples_for_running_average(asc_data_lookup, n)
    # pprint(obj_colls_list)
    running_avgs_data = {}
    for window_id, obj_coll in enumerate(obj_colls_list):
        # print(window_id, list(obj_coll), len(obj_coll))
        _running_avg_data = []
        for i in range(len(obj_coll[0])):
            _running_avg_data_cols = []
            for j in range(len(obj_coll[0][i])):
                sum_data = 0
                for obj_nth in range(n):
                    sum_data += float(obj_coll[obj_nth][i][j])
                running_avg_val = float(sum_data / n)
                _running_avg_data_cols.append(running_avg_val)
            _running_avg_data.append(_running_avg_data_cols)

        avg_data_output_location = ".\\Output Files\\Running Averages\\running_avg_iter" + str(window_id + 1) + ".asc"
        print("\nRefer location : \"" + avg_data_output_location + "\" for the running averages.")
        # for i in list(obj_coll):
        #     print(list(asc_data_lookup.keys())[list(asc_data_lookup.values()).index(i)])
        # pprint(asc_data_lookup)

        write_asc_data_file(_running_avg_data, avg_data_output_location)

        running_avgs_data["running_avg_iter" + str(window_id + 1)] = _running_avg_data[:]
    return running_avgs_data


def get_categorize_sensor_values(two_Dim_sensor_data):
    """
    Returns the catagorized data values
    param _two_Dim_sensor_data: 2d Numeric array
    returns: catagorized data values as 2d array
    """
    categorized_data = []
    for i in range(len(two_Dim_sensor_data)):
        categorized_i_data = []
        for j in range(len(two_Dim_sensor_data[i])):
            if (two_Dim_sensor_data[i][j] >= -10000) and (two_Dim_sensor_data[i][j] <= -10):
                categorized_i_data.append(3)
            elif two_Dim_sensor_data[i][j] <= 50:
                categorized_i_data.append(0)
            elif two_Dim_sensor_data[i][j] <= 100:
                categorized_i_data.append(1)
            elif two_Dim_sensor_data[i][j] <= 10000:
                categorized_i_data.append(3)
            else:
                categorized_i_data.append(None)
        categorized_data.append(categorized_i_data)
    return categorized_data


def categorize_data_values(diff_array_results):
    """
    iterates through the available array of sensor datas and catagorizes the value
    param diff_array_results: array of sensor array data
    return: dictionary of categorized sensor array data
    """
    categorized_data_results = {}
    for data_info, sensor_data in diff_array_results.items():
        categorized_data = get_categorize_sensor_values(sensor_data)
        categorized_data_results['categorized_' + data_info] = categorized_data

        output_location = '.\\Output Files\\Catagorized Files\\categorized_' + data_info + '.asc'
        write_asc_data_file(categorized_data, output_location)
    return categorized_data_results


def accumulate_iteration_values(iter_dict):
    """
    returns the dict of list of accumulated data till the last date available
    """
    accumulated_iterations = {}
    _iter_dict_keys = list(iter_dict.keys())
    while len(_iter_dict_keys) != 0:
        # print("accumulation_from_" + _iter_dict_keys[0][24:])  # len("accumulation_from_")==24
        items_to_accumulate = [np.array((iter_dict[key])) for key in _iter_dict_keys]
        # for i in items_to_accumulate:
        #     print(type(i))
        # print(sum(items_to_accumulate).tolist())
        # print(type(abc), type(items_to_accumulate[0][0][0]))
        accumulated_iterations["accumulation_from_" + _iter_dict_keys[0][24:]] = sum(items_to_accumulate).tolist()
        _iter_dict_keys.pop(0)
    return accumulated_iterations


def normalize_accululated_data(accumulated_lookup):
    """
    returns the dict with data normalized with the total accumulation
    """
    normalized_accumulated_dict = {"normalized_" + key: (np.array(value) * 100 /
                                                        (len(accumulated_lookup) + 1 - int(key[22:]))).tolist()
                                   for key, value in accumulated_lookup.items()}  # len("accumulation_from_iter") = 22
    return normalized_accumulated_dict


def categorize_normalized_acc_data(normalized_accumulated_dict):
    """Categorize data on the basis of Normalized_Categorization file in the root location and returns the same"""
    _normalized_accumulated_dict = normalized_accumulated_dict
    categorized_normalized_accumulated_dict = {}

    with open("Normalized_Categorization.json") as json_file:
        categories = json.load(json_file)
        # print(type(categories))

        for key, value in normalized_accumulated_dict.items():
            for i in range(len(value)):
                for j in range(len(value[i])):
                    for label, limit in categories.items():
                        _label = float(label)
                        _limit = make_tuple(limit)
                        if float(_limit[0]) < value[i][j] <= float(_limit[1]):
                            _normalized_accumulated_dict[key][i][j] = _label
                            break
            categorized_normalized_accumulated_dict["categorized_" + key] = _normalized_accumulated_dict[key]
    return categorized_normalized_accumulated_dict
