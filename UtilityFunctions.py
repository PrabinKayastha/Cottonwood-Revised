import os
from itertools import tee, islice
import csv
import numpy
from pip._vendor.colorama import Fore

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


def get_list_of_asc_input_files():
    """
    Prompts for user input of a file location.
    Returns for an array containing the file locations and a dictionary for the data file name with its location for
    given user input of a file location.
    return: list of all files location.
    """
    all_files = []
    print(Fore.RED + "Hit 'Enter' to quit." + Fore.RESET)

    path = input(Fore.YELLOW + "Input the folder locations if any ::: " + Fore.RESET)
    if path:
        for r, d, f in os.walk(path):  # r=root, d=directory F=file
            for file in f:
                if ".asc" in file:
                    all_files.append(os.path.join(r, file))
    return all_files


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


def create_adjusted_topos(_datafiles_location):
    """
    Returns a dictionary of .asc filename and its corresponding AscData type object.
    Adjusts the data values in object of type AscData class with the topo.asc data and
    writes the file into a output file location.
    param _datafiles_location: Root folder location for the input files.
    return: Dictionary of .asc filename and its corresponding AscData type object.
    """
    data_file_objects_dict = {}
    if _datafiles_location:
        print(str(len(_datafiles_location)) + " data files found!!!")

        for data_file_location in _datafiles_location.values():
            data_file_objects_dict[data_file_location] = create_asc_data_obj(data_file_location)

        for data_file_location, data_file_object in data_file_objects_dict.items():
            adjusted_output_location = "./Output Files/Topo Adjusted Files/adj_" + data_file_location[data_file_location.rfind("\\") + 1:]
            write_asc_data_file(data_file_object.adjust_with_topo(), adjusted_output_location)

        print("The adjusted output can be found at 'Output Files' in the project root folder.")
    else:
        print("WARNING ::: No asc files found!!!!!")
    return data_file_objects_dict

