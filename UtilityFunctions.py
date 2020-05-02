import os
from itertools import tee, islice
import csv
import numpy
from colorama import Fore

from AscData import AscData


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


def export_topo_adjusted_data(data_file_objects_lookup):
    """
    Returns a dictionary of .asc filename and its corresponding AscData type object.
    Adjusts the data values in object of type AscData class with the topo.asc data and
    writes the file into a output file location.
    param _datafiles_location: Root folder location for the input files.
    return: Dictionary of .asc filename and its corresponding AscData type object.
    """
    data_file_objects_dict = {}

    for data_file_name, data_file_object in data_file_objects_lookup.items():
        adjusted_output_location = "./Output Files/Topo Adjusted Files/adj_" + data_file_name
        write_asc_data_file(data_file_object.adjust_with_topo(), adjusted_output_location)

    print("The adjusted output can be found at './Output Files/Topo Adjusted Files/' in the project root folder.")
    return data_file_objects_dict


def init_iterable_objs_for_running_avg(_data_file_objects, n=3):
    """
    Initialize the running datasets of 'n' data files.
    param _data_file_objects: Dictionary of .asc filename and its corresponding AscData type object.
    param n: Size of the window. Default running window size is 3.
    return: The zipped tuples of data sets for a given window size.
    """
    _data_file_objects_sorted_by_day = sorted(_data_file_objects.items(), key=lambda x: int(x[0][x[0].rfind("\\wd_day") + 7: x[0].rfind(".asc")]))
    print(_data_file_objects_sorted_by_day)
    _data_obj_dict_sorted = {}
    for i in _data_file_objects_sorted_by_day:
        _data_obj_dict_sorted[i[0]] = i[1]
    iters = tee(_data_obj_dict_sorted.values(), n)
    for i, it in enumerate(iters):
        next(islice(it, i, i), None)
    return zip(*iters)


def calc_topo_adj_asc_running_avg(_data_file_objects, n=3):
    """
    Calculate the running average for 'n' datafiles and write them into output file location.
    param _data_file_objects: Dictionary of .asc filename and its corresponding AscData type object.
    param n: Window size for the running average. Default running window is 3.
    return: running average of the data for each iterations in a dictionary.
    """
    obj_colls_list = init_iterable_objs_for_running_avg(_data_file_objects, n)
    running_avgs_data = {}
    for window_id, obj_coll in enumerate(obj_colls_list):
        print(window_id, list(obj_coll), len(obj_coll))
        _running_avg_data = []
        for i in range(len(obj_coll[0].topo_adjusted_data)):
            _running_avg_data_cols = []
            for j in range(len(obj_coll[0].topo_adjusted_data[i])):
                sum_data = 0
                for obj_nth in range(n):
                    sum_data += float(obj_coll[obj_nth].topo_adjusted_data[i][j])
                running_avg_val = float(sum_data / n)
                _running_avg_data_cols.append(running_avg_val)
            _running_avg_data.append(_running_avg_data_cols)

        avg_data_output_location = ".\\Output Files\\running_avg_iter" + str(window_id + 1)
        print("\nRefer location : \"" + avg_data_output_location + "\" for the running averages of :")
        for i in list(obj_coll):
            print(list(_data_file_objects.keys())[list(_data_file_objects.values()).index(i)])

        write_asc_data_file(_running_avg_data, avg_data_output_location)

        running_avgs_data["running_avg_iter" + str(window_id + 1)] = _running_avg_data[:]
    return running_avgs_data

